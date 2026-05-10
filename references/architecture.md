# 架构与构建机制

## 项目布局

```
my-report/
├── 我的汇报.html              ← 最终产物（build.py 生成）
├── 我的汇报.pdf               ← export_pdf.py 生成（可选）
├── build.py                   ← 合并脚本
├── export_pdf.py              ← PDF 导出脚本
└── src/
    ├── shell.html             ← HTML 骨架，含 {{STYLES}} {{SLIDES}} {{SCRIPTS}} 占位
    ├── styles/
    │   ├── common.css         ← 全局样式（含主题变量、组件库）
    │   ├── slide-1.css        ← 第 1 页特殊样式（可空）
    │   └── slide-N.css
    ├── slides/
    │   ├── slide-1.html       ← 第 1 页 .slide div 内容（不含 <html>/<body>）
    │   └── slide-N.html
    ├── scripts/
    │   ├── common.js          ← 自适应 + 导航 + ECharts helper
    │   ├── slide-1.js         ← 必须导出 initSlide1() 函数
    │   └── slide-N.js
    └── data/
        ├── slide-1.json       ← 该页所需数据（可选）
        └── slide-N.json
```

## build.py 工作原理

```python
# 1. 把所有 styles/*.css 拼接 → {{STYLES}}
# 2. 把所有 slides/*.html 拼接 → {{SLIDES}}（自动加 <!-- SLIDE N --> 注释）
# 3. 把所有 scripts/*.js 拼接 → {{SCRIPTS}}
# 4. 写入 shell.html 的占位符 → 输出最终 HTML
```

**为什么这么做？**
- 单页改动只动 1~3 个小文件，单文件 ≤ 200 行 → 编辑器/Claude 上下文友好、token 省
- 最终是单 HTML（无外部依赖、可直接邮件/IM 分享）
- 多人协作时按页分工不冲突

## 数据分离机制（v2 — 新做法）

旧做法（4 月汇报里的）：数据写在 `scripts/slide-N.js` 顶部的 `const XXX_DATA = {...}`。
新做法：把 `XXX_DATA` 抽成 `data/slide-N.json`。两种衔接方式：

### 方式 A · build 时内联（推荐，单文件可分享）

`build.py` 在拼接 JS 前，先读取 `data/*.json`，在每个 slide-N.js 前注入：

```python
data_path = SRC / 'data' / f'slide-{i}.json'
if data_path.exists():
    data_json = data_path.read_text(encoding='utf-8')
    script_parts.append(f'window.__DATA_{i}__ = {data_json};')
```

`scripts/slide-N.js` 通过 `window.__DATA_N__` 读取。

### 方式 B · 运行时 fetch（适合数据频繁变动 + 服务器托管）

```js
async function initSlide5() {
  const data = await fetch('./data/slide-5.json').then(r => r.json());
  renderTrendChart('chart-ph', data.ph);
}
```

注意：本地用 `file://` 打开时 `fetch()` 会被 CORS 拦截，所以**默认方式 A**。需要 fetch 时启动一个本地静态服务器（`python3 -m http.server`）。

## 自适应缩放（核心约束）

**所有元素按设计稿 1600×900 像素来定**。浏览器窗口大小变化时，整个 canvas 通过 CSS `transform: scale(--fit)` 等比缩放，永远完整可见、不裁剪。

```css
:root {
  --design-w: 1600px;
  --design-h: 900px;
  --fit: 1; /* JS 计算后写入 */
  --nav-reserve: 88px; /* 底部导航条预留 */
}
.canvas {
  position: absolute; top: 50%; left: 50%;
  width: var(--design-w);
  height: var(--design-h);
  transform: translate(-50%, -50%) scale(var(--fit));
  transform-origin: center center;
}
```

```js
function fitCanvas() {
  const w = window.innerWidth;
  const h = Math.max(0, window.innerHeight - 88);
  const scale = Math.min(w / 1600, h / 900);
  document.documentElement.style.setProperty('--fit', scale.toFixed(4));
}
window.addEventListener('resize', fitCanvas);
window.addEventListener('DOMContentLoaded', fitCanvas);
```

**这条约束的副作用（必须遵守）**：
- ❌ **不要用** `vw / vh / %` 来定字号或间距 → 会跟整体 scale 双重缩放
- ✅ 全部用 `px`，按 1600×900 设计稿来量
- ✅ 字号也用 `px`（已经在 `--fs-*` 变量里）
- ✅ Chart 的 `font.size`、`borderWidth` 也按 px 设计稿值

## 导航与图表初始化

`common.js` 提供：
- `goTo(idx)` / `go(±1)` — 切页
- 键盘 ←/→/↑/↓ 翻页
- 底部圆点 + "1 / 6" 计数器
- `initCharts(idx)` 自动调用 `window.initSlide{N}()`，每页只初始化一次

每页 JS 必须导出 `function initSlide{N}() { ... }`（即使页面没图表也要有空函数，否则 PDF 导出会找不到）。

## PDF 导出（export_pdf.py）

- 用 Playwright headless Chromium，viewport = 1600×900，device_scale_factor=2（@2x，文字锐利）
- 注入 CSS override：`--fit:1` + 隐藏 nav bar
- 关闭 Chart.js 动画 → 截图前 chart 已完整渲染
- 逐页激活 → 等 chart canvas 有像素 → 截 PNG
- `img2pdf` 合并为 13.33×7.5 inch（标准 16:9 演示文稿尺寸）的 PDF

## 字体加载

`shell.html` 引入：
- **Noto Sans SC** — 正文中文（300/400/500/700/900）
- **JetBrains Mono** — 数字 / 代码 / 标签
- **Bebas Neue** — 大数字（可选，仅总览页那种"5 个" 64px 大数字时用）

切主题时如果换字体，在该主题的 CSS 段里 import 即可。
