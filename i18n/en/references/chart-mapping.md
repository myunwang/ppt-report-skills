# Data Shape ↔ Chart Selection Decision Table (ECharts)

**First principle**: a chart is a tool for answering "what does the reader want to know at a glance." **First think about what the reader needs to see**, then choose the chart.

## Decision Table

| Data shape / reader question | Recommended chart | Anti-pattern (don't use) |
|---|---|---|
| Multi-object single-period comparison (N objects, 1 value each) | **Horizontal bar** | Multi-column bar (crowded axis) |
| Single-object time trend (one time series) | **Line chart** (with milestone vertical lines) | Bar |
| Multi-object time trend (≤5 lines) | **Multi-color line chart** | Stacked area (can't see individual lines) |
| Before/after two-period comparison of the same object (experiment vs control) | **Side-by-side double bar + Δ delta** or **metric-row table** | Dual y-axis line |
| Share/composition (5 items or fewer) | **100% stacked bar** (horizontal saves more space) | **Pie chart (strongly discouraged)** |
| Share/composition (more than 5 items, with a long tail) | **Horizontal bar + Top N + Other** or **mini-bar list** | Pie chart / nested pie |
| Ranking (Top 20) | **Horizontal mini-bar** (custom div, no chart library) | Scatter / word cloud |
| Two metrics viewed in sync (two different scales over the same time series) | **Dual y-axis line** | Double bar (the order-of-magnitude difference is invisible) |
| Single number close-up (one core KPI) | **Big-number metric-card** (no chart) | — |
| Matrix / 2D distribution (dimension A × dimension B) | **heatmap** | Multi-group bar |
| Funnel (multi-step conversion chain) | **Funnel chart** or **horizontal decreasing bar** | Pie chart |
| Status overview (projects/tasks with multiple statuses) | **Status card grid + dot/tag** | Any chart |

## Golden Prohibitions

1. **Don't use a pie chart for more than 5 items** (the human eye can't tell 30% from 25%)
2. **Don't use 3D charts** (perspective distorts the data)
3. **For dual y-axes, the left and right scales must have a logical relationship** (don't force-fit them)
4. **A line chart with more than 7 lines must support switching/filtering**, otherwise cut it
5. **A bar chart's y-axis must start from 0** (unless the change within the same KPI dimension is extremely small and needs magnification)
6. **Don't use gradient color fills for bars** (it impairs precision judgment)

## ECharts Global Baseline Configuration

`scripts/common.js` maintains a default option that all charts `merge`:

```js
const ECHARTS_BASE = {
  textStyle: { fontFamily: 'Noto Sans SC, sans-serif', color: '#475569' },
  grid: { left: 40, right: 24, top: 24, bottom: 32, containLabel: true },
  legend: {
    bottom: 0, itemGap: 16, itemWidth: 12, itemHeight: 8,
    textStyle: { color: '#475569', fontSize: 11 },
  },
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(15,23,42,0.95)',
    borderWidth: 0,
    textStyle: { color: '#ffffff', fontSize: 11 },
    axisPointer: { type: 'line', lineStyle: { color: 'rgba(15,23,42,0.20)', type: 'dashed' } }
  },
  xAxis: {
    type: 'category',
    axisLine:  { lineStyle: { color: 'rgba(15,23,42,0.10)' } },
    axisTick:  { show: false },
    axisLabel: { color: '#94a3b8', fontSize: 10 },
    splitLine: { show: false },
  },
  yAxis: {
    type: 'value',
    axisLine:  { show: false },
    axisTick:  { show: false },
    axisLabel: { color: '#94a3b8', fontSize: 10 },
    splitLine: { lineStyle: { color: 'rgba(15,23,42,0.06)' } },
  },
  color: [
    'var(--accent)',  'var(--accent2)', 'var(--accent3)',
    'var(--warn)',    '#8b5cf6',        '#ef4444',
  ],
};
```

> Note: ECharts does not directly support CSS variables. `common.js` has a `resolveCssVars(option)` function that replaces variables with actual values; **call it again to rerender when switching themes**.

## Template 1: Dual y-axis Time-Series Line (Primary Metric + Secondary Metric)

Applicable scenario: two metrics with different scales over the same time series (e.g., "sales + unit price," "DAU + ARPU," "traffic + conversion rate").

```js
function renderDailyDual(elId, labels, leftData, rightData, marks, cfg = {}) {
  const leftName  = cfg.leftName  || 'Primary';
  const rightName = cfg.rightName || 'Secondary';
  const opt = mergeBase({
    legend: { data: [leftName, rightName], bottom: 4 },
    xAxis: { data: labels, axisLabel: { interval: 'auto' } },
    yAxis: [
      { type: 'value', name: cfg.leftUnit  || leftName,  nameTextStyle: { fontSize: 9 } },
      { type: 'value', name: cfg.rightUnit || rightName, nameTextStyle: { fontSize: 9 }, splitLine: { show: false } },
    ],
    series: [
      { name: leftName,  type: 'line', data: leftData,  smooth: 0.35, symbol: 'none',
        lineStyle: { width: 1.8 }, areaStyle: { opacity: 0.08 }, yAxisIndex: 0 },
      { name: rightName, type: 'line', data: rightData, smooth: 0.35, symbol: 'none',
        lineStyle: { width: 1.5, type: 'dashed' }, yAxisIndex: 1 },
    ],
  });
  // milestone vertical lines — implemented via markLine
  opt.series[0].markLine = {
    symbol: 'none',
    lineStyle: { type: 'dashed', width: 1 },
    label: { formatter: p => p.data.label, position: 'insideEndTop', fontSize: 9 },
    data: marks.map(m => ({ xAxis: m.x, label: { color: m.color }, lineStyle: { color: m.color } })),
  };
  echarts.init(document.getElementById(elId)).setOption(opt);
}
```

Data shape (in `data/slide-N.json`):

```json
{
  "labels": ["W1","W2", "..."],
  "a":  { "metric1": [/* N numbers */], "metric2": [/* N */] },
  "marks": [
    { "x": "W3",  "color": "#06b6d4", "label": "Milestone 1" },
    { "x": "W7", "color": "#f59e0b", "label": "Milestone 2" }
  ]
}
```

## Template 2: 100% Stacked Bar (Before/After Share Comparison)

```js
function renderShare100(elId, labels, pre, post, seriesNames) {
  const series = seriesNames.map((name, i) => ({
    name, type: 'bar', stack: 'pct',
    barCategoryGap: '40%',
    label: { show: true, formatter: p => p.value < 4 ? '' : p.value.toFixed(1) + '%', color: '#fff', fontSize: 10 },
    data: [pre[i], post[i]],
  }));
  echarts.init(document.getElementById(elId)).setOption(mergeBase({
    legend: { bottom: 0, data: seriesNames },
    yAxis: { type: 'category', data: labels },  // ['Before','After']
    xAxis: { type: 'value', max: 100, axisLabel: { formatter: '{value}%' } },
    series,
  }));
}
```

## Template 3: Horizontal Top-20 mini-bar (No Chart Library)

```js
function renderMiniBars(containerId, items /* [[name, val], ...] */, color) {
  const el = document.getElementById(containerId);
  el.innerHTML = '';
  const max = Math.max(...items.map(([,v]) => v));
  items.forEach(([name, val]) => {
    const pct = max ? Math.max(2, val / max * 100) : 0;
    el.insertAdjacentHTML('beforeend', `
      <div class="mini-bar-row">
        <div class="mini-bar-label">${name}</div>
        <div class="mini-bar-track"><div class="mini-bar-fill" style="width:${pct}%;background:${color};"></div></div>
        <div class="mini-bar-val">${val.toLocaleString()}</div>
      </div>`);
  });
}
```

Data shape:

```json
{ "a": [["{label 1}", 10000], ["{label 2}", 8000], "..."] }
```

## Template 4: Multi-Object Trend Comparison (Multi-Color Line)

```js
function renderMultiTrend(elId, labels, seriesData /* {a:[...], b:[...], c:[...], d:[...]} */) {
  const colors = { a: '#06b6d4', b: '#f59e0b', c: '#10b981', d: '#ef4444' };
  const names  = { a: 'Series A', b: 'Series B', c: 'Series C', d: 'Series D' };
  const series = Object.keys(seriesData).map(k => ({
    name: names[k], type: 'line', data: seriesData[k],
    smooth: 0.35, symbol: 'none', lineStyle: { width: 2, color: colors[k] },
  }));
  echarts.init(document.getElementById(elId)).setOption(mergeBase({
    legend: { data: Object.values(names), bottom: 0 },
    xAxis: { data: labels },
    yAxis: { axisLabel: { formatter: '{value}%' } },
    series,
  }));
}
```

## Data Storage Conventions

One `data/slide-N.json` per slide. Structure example:

```json
{
  "title": "{slide topic}",
  "subtitle": "{one-sentence conclusion — contains key numbers}",
  "kpis": [
    { "key": "a", "value": 6.6, "color": "var(--accent2)" },
    { "key": "b", "value": 4.5, "color": "var(--warn)" }
  ],
  "category_bars": {
    "a": [["{category 1}", 10000], ["{category 2}", 8000]]
  },
  "trend": {
    "labels": ["W1", "W2", "W3"],
    "series": { "a": [10.5, 10.3, 10.2] }
  }
}
```

**Conventions**:
- Store the time-series labels separately once, shared across multiple series
- Write **semantic** keys in the JSON for colors where possible (e.g., `key: 'a'`) rather than concrete hex values, letting JS look up the color from a table, **to support theme switching**
- For large data (N rows × M dimensions × K metrics) use compact arrays; don't break them into an object array
