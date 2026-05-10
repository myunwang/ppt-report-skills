# 多主题切换

## 设计原则

1. **CSS 变量驱动**：所有颜色 / 字体 / 间距用 `--*` 变量，主题只覆写变量，不动 class 结构
2. **`data-theme` 属性切换**：`<body data-theme="dark-tech">`，CSS `[data-theme="..."]` 选择器覆写 `:root`
3. **JS 同步更新 ECharts 配色**：切主题后调用 `applyTheme(name)`，重新读取 var() 值并 setOption

## 5 套预设主题

### 1. `modern-light`（默认）— 浅色商务

```css
[data-theme="modern-light"], :root {
  --bg: #f4f6fb;
  --surface: #ffffff;
  --surface2: #f1f4fa;
  --border: rgba(15, 23, 42, 0.08);
  --accent:  #2563eb;  /* 蓝 */
  --accent2: #0891b2;  /* 青 */
  --accent3: #059669;  /* 绿 */
  --warn:    #d97706;
  --danger:  #dc2626;
  --text:    #0f172a;
  --text2:   #475569;
  --text3:   #94a3b8;
  --font-sans: 'Noto Sans SC', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

适用：内部汇报、产品月报。柔和、信息密度高、印 PDF 友好。

### 2. `dark-tech` — 深色科技感

```css
[data-theme="dark-tech"] {
  --bg: #0a0e1a;
  --surface: #131826;
  --surface2: #1c2233;
  --border: rgba(255, 255, 255, 0.08);
  --accent:  #3b82f6;
  --accent2: #06b6d4;
  --accent3: #10b981;
  --warn:    #f59e0b;
  --danger:  #ef4444;
  --text:    #e2e8f0;
  --text2:   #94a3b8;
  --text3:   #64748b;
}
```

适用：技术评审、AI/数据团队对外。**注意**：去掉 box-shadow，用 border 区分层次。

### 3. `warm-business` — 暖色商业感

```css
[data-theme="warm-business"] {
  --bg: #fdf8f3;
  --surface: #ffffff;
  --surface2: #f9f1e8;
  --border: rgba(120, 53, 15, 0.10);
  --accent:  #c2410c;  /* 砖红 */
  --accent2: #b45309;  /* 焦糖 */
  --accent3: #15803d;
  --warn:    #ca8a04;
  --danger:  #b91c1c;
  --text:    #1c1917;
  --text2:   #57534e;
  --text3:   #a8a29e;
  --font-sans: 'Noto Serif SC', 'Noto Sans SC', sans-serif;
}
```

适用：年度回顾、业务总结、对外品牌报告。字号稍大、行距更舒展。

### 4. `brand-blue` — 品牌深蓝（金融/咨询）

```css
[data-theme="brand-blue"] {
  --bg: #f0f4f9;
  --surface: #ffffff;
  --surface2: #e6edf6;
  --border: rgba(30, 58, 138, 0.12);
  --accent:  #1e3a8a;  /* 深蓝 */
  --accent2: #2563eb;
  --accent3: #0891b2;
  --warn:    #b45309;
  --danger:  #b91c1c;
  --text:    #0c1a3a;
  --text2:   #334155;
  --text3:   #64748b;
}
```

适用：投资人汇报、董事会、咨询交付。庄重、克制。

### 5. `minimal-mono` — 极简单色

```css
[data-theme="minimal-mono"] {
  --bg: #fafafa;
  --surface: #ffffff;
  --surface2: #f5f5f5;
  --border: rgba(0, 0, 0, 0.10);
  --accent:  #18181b;  /* 黑 */
  --accent2: #404040;
  --accent3: #16a34a;  /* 仅状态色保留 */
  --warn:    #ca8a04;
  --danger:  #dc2626;
  --text:    #18181b;
  --text2:   #52525b;
  --text3:   #a1a1aa;
  --font-sans: 'Inter', 'Noto Sans SC', sans-serif;
}
```

适用：极简偏好、设计感、PR 文章。色彩约束到极致，靠层次和留白。

## 主题切换 UI

`scripts/theme-switcher.js` 提供右上角小开关：

```js
const THEMES = ['modern-light', 'dark-tech', 'warm-business', 'brand-blue', 'minimal-mono'];

function applyTheme(name) {
  document.body.setAttribute('data-theme', name);
  localStorage.setItem('report-theme', name);
  // ECharts 重渲染
  Object.values(window.__charts || {}).forEach(c => c.setOption(rebuildOption(c.getOption())));
}

function initThemeSwitcher() {
  const saved = localStorage.getItem('report-theme') || 'modern-light';
  applyTheme(saved);
  // 渲染右上角 switcher
  const sw = document.createElement('div');
  sw.className = 'theme-switcher';
  sw.innerHTML = THEMES.map(t => `<button data-theme-btn="${t}">${t}</button>`).join('');
  sw.addEventListener('click', e => {
    const t = e.target.dataset.themeBtn;
    if (t) applyTheme(t);
  });
  document.body.appendChild(sw);
}
```

```css
.theme-switcher {
  position: fixed; top: 16px; right: 16px; z-index: 200;
  display: flex; gap: 4px;
  background: rgba(255,255,255,0.85); padding: 4px; border-radius: 100px;
  backdrop-filter: blur(8px); border: 1px solid var(--border);
}
.theme-switcher button {
  font-family: var(--font-mono); font-size: 10px;
  padding: 4px 10px; border: none; border-radius: 100px;
  background: transparent; cursor: pointer; color: var(--text2);
}
.theme-switcher button:hover { background: var(--surface2); }
```

## 自定义主题

新增主题只需添加一段 `[data-theme="my-name"] { --... }`，并把 `'my-name'` push 到 `THEMES` 数组。**禁止**：不要在某一页的 slide-N.css 里硬写颜色 — 那样切主题切不动。

## 主题与图表

ECharts 不支持原生 `var(--*)`，所以 `common.js` 在初始化前调一次 `resolveCssVars()` 把 `'var(--accent)'` 字符串替换为 `getComputedStyle(...).getPropertyValue('--accent')`。切主题后必须**重建** option 才会生效（不只是 setOption merge）。

## 何时建议主题

- 用户没说 → 默认 `modern-light`
- 用户说"商务/正式" → `brand-blue`
- 用户说"科技/酷一点" → `dark-tech`
- 用户说"年度/回顾/温暖" → `warm-business`
- 用户说"极简/性冷淡" → `minimal-mono`
- 不确定 → **询问用户**或同时给两套截图让选
