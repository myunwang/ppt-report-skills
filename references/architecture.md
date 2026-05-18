# 架构与构建机制

## 项目布局

```
my-report/
├── dist/                      ← 构建产物目录（build.py 自动创建）
│   ├── 我的汇报.html          ← 最终产物（build.py 生成）
│   └── 我的汇报.pdf           ← export_pdf.py 生成（可选）
├── build.py                   ← 合并脚本（也把 src/assets/ 拷进 dist/）
├── export_pdf.py              ← PDF 导出脚本
├── xlsx2json.py               ← Excel/CSV → JSON 转换器（被 build 自动调用，也可单跑）
├── fetch_logos.py             ← 可选：把在线 logo 缓存到 src/assets/logos/ 供离线（默认在线引用，不跑也能显示）
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
    ├── assets/                ← 本项目静态资源（build 时整体拷进 dist/assets/）
    │   └── logos/             ← 可选离线缓存：fetch_logos.py 下载的 logo（在线模式下可空）
    └── data/                  ← 三种格式自由选择，build.py 自动转 JSON 注入
        ├── slide-1.xlsx       ← 推荐：日常用 Excel 改数据
        ├── slide-2.csv        ← 单表数据
        └── slide-3.json       ← 复杂嵌套结构 / 机器生成
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

## 数据分离机制

**核心思路**：渲染代码（HTML/JS）和数据（xlsx/csv/json）完全解耦。下次更新数据，只改数据文件，重跑 `python3 build.py`，**渲染代码一行都不用动**。

### 支持的数据格式

| 格式 | 适用场景 | 转换结果 |
|---|---|---|
| `.xlsx` | **日常推荐** — 数据本来就在 Excel 里 | 每个 sheet → JSON 顶层 key，每个 sheet 内容 → `[{col: val}, ...]` |
| `.csv` | 单表数据 | 整份 → `[{col: val}, ...]` |
| `.json` | 机器生成 / 复杂嵌套结构 | 直接读取 |

**优先级**：`.json > .xlsx > .csv`（同一 slide 编号下只取一个）。

### xlsx / csv 约定

1. **第 1 行 = 表头**，后续每行 = 数据
2. **每行转一个对象**：`{表头列: 单元格值}`
3. **类型自动推断**：纯数字单元格 → number，其他保留 string
4. **过滤约定**：sheet 名 / 列名以 `_` 开头会被跳过（用于备注、辅助计算列）
5. **空行自动跳过**

举例：`src/data/slide-3.xlsx` 含两个 sheet —

| sheet `kpis` | label | value | unit |
|---|---|---|---|
| | DAU | 12.4 | 万 |
| | ARR | 48 | M USD |

| sheet `trend` | week | na | eu |
|---|---|---|---|
| | W1 | 12.1 | 8.4 |
| | W2 | 12.4 | 8.6 |

转换后 `window.__DATA_3__` 为：

```json
{
  "kpis":  [{"label": "DAU", "value": 12.4, "unit": "万"}, {"label": "ARR", "value": 48, "unit": "M USD"}],
  "trend": [{"week": "W1", "na": 12.1, "eu": 8.4}, {"week": "W2", "na": 12.4, "eu": 8.6}]
}
```

### build.py 的注入流程

```
src/data/slide-N.xlsx    ← 用户编辑
        ↓ build.py 调 xlsx2json.xlsx_to_dict(path)
{kpis: [...], trend: [...]}    ← Python dict
        ↓ json.dumps + 包装为 window.__DATA_N__ = ...;
最终 HTML 的 <script> 中：window.__DATA_N__ = {"kpis": [...], "trend": [...]};
        ↓ initSlideN() 通过 window.__DATA_N__ 读取
ECharts / DOM 渲染
```

`scripts/slide-N.js` 里只需：

```js
function initSlideN() {
  const D = window.__DATA_N__;
  // D.kpis = [...], D.trend = [...]
  // 调用 renderXxx() 或 initChart() 即可
}
```

### 独立调试

```bash
# 转单个文件（输出到 stdout）
python3 xlsx2json.py src/data/slide-3.xlsx

# 写入 JSON（这样以后 build 会优先用 JSON）
python3 xlsx2json.py src/data/slide-3.xlsx > src/data/slide-3.json

# 转整目录
python3 xlsx2json.py src/data/
```

### 何时用哪种格式

- **大部分场景用 xlsx**：业务数据本来就在 Excel 里，直接放进去就行
- **简单一维数据用 csv**：从 BI / 数据库导出的 csv 文件
- **嵌套结构 / 自动生成用 json**：比如 markLine 配置（嵌套对象）、API 拉出来的复杂结构 — 这种用 xlsx 表达不优雅，直接写 JSON 更顺手

### 运行时 fetch（可选，不推荐）

不通过 build.py 内联，而是浏览器运行时 `fetch('./data/slide-5.json')`，适合数据频繁变动 + 服务器托管。注意 `file://` 打开时 CORS 会拦截，所以默认走 build 内联。

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
