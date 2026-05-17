# Common Component Library

All classes are predefined in `assets/styles/common.css` — use them directly.

## Top Trio (required on every slide)

```html
<div class="slide-label">Monthly Overview</div>
<div class="slide-title">April Delivery Overview</div>
<div class="slide-subtitle">
  <strong>All 5</strong> strategy requirements shipped · Dashboards <span class="pos">1 live</span> + 2 offline
</div>
```

## KPI Big-Number Grid

```html
<div class="kpi-grid">    <!-- grid-template-columns: repeat(3, 1fr); -->
  <div class="kpi-card blue">       <!-- color: blue / cyan / green / amber / red / purple -->
    <div class="kpi-icon">🎯</div>
    <div class="kpi-num">{core metric value}</div>
    <div class="kpi-label">{metric name}</div>
    <div class="kpi-desc">{definition note}</div>
  </div>
</div>
```

## Compact metric-up-card (4–5 per row)

```html
<div class="metric-up-grid">
  <div class="metric-up-card">
    <div class="metric-up-num">{value}</div>
    <div class="metric-up-label">{label}</div>
    <div class="metric-up-sub">{supplementary note}</div>
  </div>
</div>
```

## Card

```html
<div class="card card-accent-left">  <!-- pick any of accent-left/green/warn/danger -->
  <div class="metric-row">
    <span class="metric-name">{metric name}</span>
    <div class="metric-vals">
      <span class="metric-before">{previous value}</span>
      <span class="metric-after">{new value}</span>
      <span class="metric-delta delta-pos">{+x%}</span>
    </div>
  </div>
</div>
```

## Timeline (horizontal)

```html
<div class="timeline-bar">
  <div class="tl-node">
    <div class="tl-dot"></div>
    <div class="tl-date">{date}</div>
    <div class="tl-label">{milestone}</div>
  </div>
  <div class="tl-line"></div>
  <div class="tl-node">...</div>
</div>
```

## Phase Timeline (vertical + three phases)

```html
<div class="phase-layout">              <!-- left phase column + right charts area -->
  <div class="phase-timeline-v">
    <div class="phase-box" style="border-top:2px solid var(--accent);">
      <div class="phase-date">PHASE 01 · {date}</div>
      <div class="phase-title">{phase title}</div>
      <div class="phase-item">
        <div class="phase-item-dot"></div>
        <div class="phase-item-text">{phase action description}</div>
      </div>
    </div>
    <div class="phase-arrow-v">↓</div>
    <div class="phase-box" style="border-top:2px solid var(--warn);">...</div>
  </div>
  <div class="phase-charts">
    <div class="chart-card">
      <div class="chart-card-header">
        <div class="chart-card-title">{object A}</div>
        <div class="chart-card-note">{subtitle}</div>
      </div>
      <div class="chart-card-body"><div id="chart-a" style="width:100%;height:100%;"></div></div>
    </div>
  </div>
</div>
```

## Two-Object Side-by-Side Comparison (two-col + card metric table)

```html
<div class="country-row">                   <!-- grid 1fr 1fr -->
  <div class="card">
    <div class="country-card-head">
      <span class="country-name a">{object A name}</span>
      <span class="country-tag a-tag">{label / status}</span>
    </div>
    <div class="metric-row"><span class="metric-name">{metric 1}</span><span class="metric-after">{value}</span></div>
    <div class="metric-row"><span class="metric-name">{metric 2}</span><span class="metric-after" style="color:var(--accent3);font-weight:700;">{value}</span></div>
  </div>
  <div class="card">...</div>
</div>
```

## Tags

```html
<span class="tag tag-p0">P0</span>           <!-- red -->
<span class="tag tag-p1">P1</span>           <!-- yellow -->
<span class="tag tag-done">✓ Live</span>        <!-- green -->
<span class="tag tag-wip">⟳ In Progress</span> <!-- cyan -->
<span class="tag tag-offline">⊞ Offline</span>  <!-- purple -->
```

## Status Dot

```html
<span class="dot ok"></span>      <!-- green, done -->
<span class="dot wip"></span>     <!-- orange, in progress -->
<span class="dot wait"></span>    <!-- gray, to do -->
<span class="dot offline"></span> <!-- gray, offline -->
```

## Chart Container (mandatory)

```html
<div class="chart-card">
  <div class="chart-card-header">
    <div class="chart-card-title">{object name}</div>
    <div class="chart-card-note">{time range / subtitle}</div>
  </div>
  <div class="chart-card-body">
    <div id="chart-a" style="width:100%;height:100%;"></div>
  </div>
</div>
```

> **Important**: When using ECharts the container must be given an **explicit height** (`height:100%` inside chart-card-body, and `min-height: 0` on the outer grid), otherwise the chart will collapse to 0 height.

## Common Grids

```css
.kpi-grid    { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; flex: 1; }
.two-col     { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; flex: 1; min-height: 0; }
.three-col   { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; flex: 1; min-height: 0; }
```

**Pitfall**: Every full-height grid/flex container **must add `min-height: 0`**, otherwise a grid item that can't shrink will overflow.

## Dividers and Bottom Conclusion

```html
<div class="divider"></div>                                    <!-- 1px horizontal line -->
<div class="card-conclusion">{summary for this card, 1–2 lines}</div>
<div class="footer-conclusion">{summary for this slide, 1–2 lines}</div>
```

## insight-box (explainer / principle note)

```html
<div class="insight-box" style="border-left:3px solid var(--accent);">
  <div class="insight-title">{the question to explain, a rhetorical question works better}</div>
  <div class="insight-text">
    {2–4 paragraphs of explanation, highlight <strong>key concepts</strong> with strong}
  </div>
</div>
```

## Anti-Patterns

- ❌ Using `<table>` instead of `metric-row` divs
- ❌ A chart using a bare `<canvas>` not wrapped in chart-card (no title, no margins)
- ❌ Custom colors not going through theme variables
- ❌ KPI big numbers not using the `var(--mono)` monospace font
