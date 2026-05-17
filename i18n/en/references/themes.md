# Multi-Theme Switching

## Design Principles

1. **CSS-variable driven**: All colors / fonts / spacing use `--*` variables; a theme only overrides variables and never touches class structure
2. **`data-theme` attribute switching**: `<body data-theme="dark-tech">`, with CSS `[data-theme="..."]` selectors overriding `:root`
3. **JS keeps ECharts colors in sync**: After switching the theme, call `applyTheme(name)` to re-read the var() values and setOption

## 5 Preset Themes

### 1. `modern-light` (default) — Light Business

```css
[data-theme="modern-light"], :root {
  --bg: #f4f6fb;
  --surface: #ffffff;
  --surface2: #f1f4fa;
  --border: rgba(15, 23, 42, 0.08);
  --accent:  #2563eb;  /* blue */
  --accent2: #0891b2;  /* cyan */
  --accent3: #059669;  /* green */
  --warn:    #d97706;
  --danger:  #dc2626;
  --text:    #0f172a;
  --text2:   #475569;
  --text3:   #94a3b8;
  --font-sans: 'Noto Sans SC', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

Use for: internal reports, monthly product reports. Soft, high information density, PDF-print friendly.

### 2. `dark-tech` — Dark Tech

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

Use for: technical reviews, AI/data team external presentations. **Note**: drop box-shadow and use border to distinguish layers.

### 3. `warm-business` — Warm Business

```css
[data-theme="warm-business"] {
  --bg: #fdf8f3;
  --surface: #ffffff;
  --surface2: #f9f1e8;
  --border: rgba(120, 53, 15, 0.10);
  --accent:  #c2410c;  /* brick red */
  --accent2: #b45309;  /* caramel */
  --accent3: #15803d;
  --warn:    #ca8a04;
  --danger:  #b91c1c;
  --text:    #1c1917;
  --text2:   #57534e;
  --text3:   #a8a29e;
  --font-sans: 'Noto Serif SC', 'Noto Sans SC', sans-serif;
}
```

Use for: annual reviews, business summaries, external brand reports. Slightly larger font size, more relaxed line spacing.

### 4. `brand-blue` — Brand Deep Blue (finance/consulting)

```css
[data-theme="brand-blue"] {
  --bg: #f0f4f9;
  --surface: #ffffff;
  --surface2: #e6edf6;
  --border: rgba(30, 58, 138, 0.12);
  --accent:  #1e3a8a;  /* deep blue */
  --accent2: #2563eb;
  --accent3: #0891b2;
  --warn:    #b45309;
  --danger:  #b91c1c;
  --text:    #0c1a3a;
  --text2:   #334155;
  --text3:   #64748b;
}
```

Use for: investor reports, board meetings, consulting deliverables. Dignified, restrained.

### 5. `minimal-mono` — Minimal Monochrome

```css
[data-theme="minimal-mono"] {
  --bg: #fafafa;
  --surface: #ffffff;
  --surface2: #f5f5f5;
  --border: rgba(0, 0, 0, 0.10);
  --accent:  #18181b;  /* black */
  --accent2: #404040;
  --accent3: #16a34a;  /* status color only, retained */
  --warn:    #ca8a04;
  --danger:  #dc2626;
  --text:    #18181b;
  --text2:   #52525b;
  --text3:   #a1a1aa;
  --font-sans: 'Inter', 'Noto Sans SC', sans-serif;
}
```

Use for: minimalist preference, design-forward, PR articles. Color constrained to the extreme, relying on hierarchy and whitespace.

## Theme Switcher UI

`scripts/theme-switcher.js` provides a small toggle in the top-right corner:

```js
const THEMES = ['modern-light', 'dark-tech', 'warm-business', 'brand-blue', 'minimal-mono'];

function applyTheme(name) {
  document.body.setAttribute('data-theme', name);
  localStorage.setItem('report-theme', name);
  // ECharts re-render
  Object.values(window.__charts || {}).forEach(c => c.setOption(rebuildOption(c.getOption())));
}

function initThemeSwitcher() {
  const saved = localStorage.getItem('report-theme') || 'modern-light';
  applyTheme(saved);
  // render top-right switcher
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

## Custom Themes

To add a new theme, simply add a `[data-theme="my-name"] { --... }` block and push `'my-name'` into the `THEMES` array. **Forbidden**: do not hard-code colors in a particular slide's slide-N.css — that breaks theme switching.

## Themes and Charts

ECharts does not support native `var(--*)`, so `common.js` calls `resolveCssVars()` once before initialization to replace the `'var(--accent)'` string with `getComputedStyle(...).getPropertyValue('--accent')`. After switching the theme you must **rebuild** the option for it to take effect (not just a setOption merge).

## When to Recommend a Theme

- User said nothing → default `modern-light`
- User said "business/formal" → `brand-blue`
- User said "tech/cooler" → `dark-tech`
- User said "annual/review/warm" → `warm-business`
- User said "minimal/austere" → `minimal-mono`
- Unsure → **ask the user** or provide screenshots of both options to choose from
