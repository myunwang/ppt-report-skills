# 数据形态 ↔ 图表选型决策表（ECharts）

**第一原则**：图表是回答"读者一眼想知道什么"的工具。**先想读者要看出什么**，再选图表。

## 决策表

| 数据形态 / 读者问题 | 推荐图表 | 反模式（不要用） |
|---|---|---|
| 多对象单期对比（N 个对象，每个 1 个值） | **横向条形** | 多列柱状（轴拥挤） |
| 单对象时间趋势（一条时间序列） | **折线图**（带里程碑竖线） | 柱状 |
| 多对象时间趋势（≤5 条线） | **多色折线图** | 堆叠面积（看不清单线） |
| 同对象前后两期对比（实验 vs 对照） | **左右双柱 + Δ delta** 或 **metric-row 表格** | 双 y 轴折线 |
| 占比/构成（5 项以内） | **100% 堆叠条形**（横向更省空间） | **饼图（强烈反对）** |
| 占比/构成（5 项以上，有长尾） | **横向条形 + Top N + Other** 或 **mini-bar 列表** | 饼图 / 嵌套饼 |
| 排名（Top 20） | **横向 mini-bar**（自定义 div，不用 chart 库） | 散点 / 词云 |
| 双指标同步看（同时间序列下两个不同量纲） | **双 y 轴折线** | 双柱状（数量级差异看不出） |
| 单数字大特写（一个核心 KPI） | **大数字 metric-card**（不用图） | — |
| 矩阵 / 二维分布（A 维 × B 维） | **heatmap** | 多组柱状 |
| 漏斗（多步转化链路） | **漏斗图** 或 **横向递减条形** | 饼图 |
| 状态总览（项目/任务多状态） | **状态卡片网格 + dot/tag** | 任何 chart |

## 黄金禁令

1. **5 项以上不用饼图**（人眼分辨不出 30% vs 25%）
2. **不用 3D 图表**（透视会扭曲数据）
3. **双 y 轴时左右量纲必须有逻辑关系**（不要硬塞）
4. **超过 7 条线的折线图必须能切换/筛选**，否则砍掉
5. **柱状图 y 轴必须从 0 开始**（除非同 KPI 维度变化极小，需放大）
6. **不要用渐变色填充柱子**（影响精度判断）

## ECharts 全局基线配置

`scripts/common.js` 里维护一份默认 option，所有图表 `merge` 它：

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

> 注意：ECharts 不直接支持 CSS 变量。`common.js` 里有一个 `resolveCssVars(option)` 函数把变量替换为实际值，**切主题时重新调用一次** rerender。

## 范本一：双 y 轴时间序列折线（主指标 + 副指标）

适用场景：同一时间序列下两个不同量纲的指标（如"销量 + 单价"、"DAU + ARPU"、"流量 + 转化率"）。

```js
function renderDailyDual(elId, labels, leftData, rightData, marks, cfg = {}) {
  const leftName  = cfg.leftName  || '主指标';
  const rightName = cfg.rightName || '副指标';
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
  // 里程碑竖线 — 通过 markLine 实现
  opt.series[0].markLine = {
    symbol: 'none',
    lineStyle: { type: 'dashed', width: 1 },
    label: { formatter: p => p.data.label, position: 'insideEndTop', fontSize: 9 },
    data: marks.map(m => ({ xAxis: m.x, label: { color: m.color }, lineStyle: { color: m.color } })),
  };
  echarts.init(document.getElementById(elId)).setOption(opt);
}
```

数据形状（在 `data/slide-N.json` 里）：

```json
{
  "labels": ["W1","W2", "..."],
  "a":  { "metric1": [/* N numbers */], "metric2": [/* N */] },
  "marks": [
    { "x": "W3",  "color": "#06b6d4", "label": "里程碑 1" },
    { "x": "W7", "color": "#f59e0b", "label": "里程碑 2" }
  ]
}
```

## 范本二：100% 堆叠条形（前后占比对比）

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
    yAxis: { type: 'category', data: labels },  // ['前','后']
    xAxis: { type: 'value', max: 100, axisLabel: { formatter: '{value}%' } },
    series,
  }));
}
```

## 范本三：横向 Top-20 mini-bar（不用 chart 库）

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

数据形状：

```json
{ "a": [["{label 1}", 10000], ["{label 2}", 8000], "..."] }
```

## 范本四：多对象趋势对比（多色折线）

```js
function renderMultiTrend(elId, labels, seriesData /* {a:[...], b:[...], c:[...], d:[...]} */) {
  const colors = { a: '#06b6d4', b: '#f59e0b', c: '#10b981', d: '#ef4444' };
  const names  = { a: '对象 A', b: '对象 B', c: '对象 C', d: '对象 D' };
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

## 数据存放规范

每页一个 `data/slide-N.json`。结构示例：

```json
{
  "title": "{页面主题}",
  "subtitle": "{一句结论 — 含关键数字}",
  "kpis": [
    { "key": "a", "value": 6.6, "color": "var(--accent2)" },
    { "key": "b", "value": 4.5, "color": "var(--warn)" }
  ],
  "category_bars": {
    "a": [["{品类 1}", 10000], ["{品类 2}", 8000]]
  },
  "trend": {
    "labels": ["W1", "W2", "W3"],
    "series": { "a": [10.5, 10.3, 10.2] }
  }
}
```

**约定**：
- 时间序列 labels 单独存一份，多个 series 共用
- 颜色尽量在 JSON 里写**语义** key（如 `key: 'a'`）而非具体十六进制，让 JS 查表得色，**支持主题切换**
- 大数据（N 行 × M 维 × K 指标）用紧凑数组，不要拆成 object array
