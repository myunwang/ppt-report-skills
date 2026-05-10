# 通用组件库

所有 class 都在 `assets/styles/common.css` 里定义好了，直接用。

## 顶部三件套（每页必有）

```html
<div class="slide-label">月度总览</div>
<div class="slide-title">4 月工作交付概览</div>
<div class="slide-subtitle">
  策略需求 <strong>5 个</strong>全部上线 · 数据看板 <span class="pos">1 上线</span> + 2 离线
</div>
```

## KPI 大数字网格

```html
<div class="kpi-grid">    <!-- grid-template-columns: repeat(3, 1fr); -->
  <div class="kpi-card blue">       <!-- 颜色：blue / cyan / green / amber / red / purple -->
    <div class="kpi-icon">🎯</div>
    <div class="kpi-num">{核心指标值}</div>
    <div class="kpi-label">{指标名}</div>
    <div class="kpi-desc">{口径说明}</div>
  </div>
</div>
```

## 紧凑型 metric-up-card（单行 4-5 个）

```html
<div class="metric-up-grid">
  <div class="metric-up-card">
    <div class="metric-up-num">{value}</div>
    <div class="metric-up-label">{label}</div>
    <div class="metric-up-sub">{补充说明}</div>
  </div>
</div>
```

## 卡片（card）

```html
<div class="card card-accent-left">  <!-- accent-left/green/warn/danger 任选 -->
  <div class="metric-row">
    <span class="metric-name">{指标名}</span>
    <div class="metric-vals">
      <span class="metric-before">{前值}</span>
      <span class="metric-after">{后值}</span>
      <span class="metric-delta delta-pos">{+x%}</span>
    </div>
  </div>
</div>
```

## 时间线（横向）

```html
<div class="timeline-bar">
  <div class="tl-node">
    <div class="tl-dot"></div>
    <div class="tl-date">{日期}</div>
    <div class="tl-label">{里程碑}</div>
  </div>
  <div class="tl-line"></div>
  <div class="tl-node">...</div>
</div>
```

## 阶段时间线（竖向 + 三阶段）

```html
<div class="phase-layout">              <!-- 左 phase 列 + 右 charts 区 -->
  <div class="phase-timeline-v">
    <div class="phase-box" style="border-top:2px solid var(--accent);">
      <div class="phase-date">PHASE 01 · {日期}</div>
      <div class="phase-title">{阶段标题}</div>
      <div class="phase-item">
        <div class="phase-item-dot"></div>
        <div class="phase-item-text">{阶段动作描述}</div>
      </div>
    </div>
    <div class="phase-arrow-v">↓</div>
    <div class="phase-box" style="border-top:2px solid var(--warn);">...</div>
  </div>
  <div class="phase-charts">
    <div class="chart-card">
      <div class="chart-card-header">
        <div class="chart-card-title">{对象 A}</div>
        <div class="chart-card-note">{副标题}</div>
      </div>
      <div class="chart-card-body"><div id="chart-a" style="width:100%;height:100%;"></div></div>
    </div>
  </div>
</div>
```

## 双对象左右对照（two-col + card 的 metric 表）

```html
<div class="country-row">                   <!-- grid 1fr 1fr -->
  <div class="card">
    <div class="country-card-head">
      <span class="country-name a">{对象 A 名称}</span>
      <span class="country-tag a-tag">{标签 / 状态}</span>
    </div>
    <div class="metric-row"><span class="metric-name">{指标 1}</span><span class="metric-after">{value}</span></div>
    <div class="metric-row"><span class="metric-name">{指标 2}</span><span class="metric-after" style="color:var(--accent3);font-weight:700;">{value}</span></div>
  </div>
  <div class="card">...</div>
</div>
```

## Tags

```html
<span class="tag tag-p0">P0</span>           <!-- 红 -->
<span class="tag tag-p1">P1</span>           <!-- 黄 -->
<span class="tag tag-done">✓ 已上线</span>   <!-- 绿 -->
<span class="tag tag-wip">⟳ 进行中</span>    <!-- 青 -->
<span class="tag tag-offline">⊞ 离线</span>  <!-- 紫 -->
```

## 状态点（dot）

```html
<span class="dot ok"></span>      <!-- 绿，完成 -->
<span class="dot wip"></span>     <!-- 橙，进行中 -->
<span class="dot wait"></span>    <!-- 灰，待办 -->
<span class="dot offline"></span> <!-- 灰，离线 -->
```

## chart 容器（必须用）

```html
<div class="chart-card">
  <div class="chart-card-header">
    <div class="chart-card-title">{对象名}</div>
    <div class="chart-card-note">{时间口径 / 副标题}</div>
  </div>
  <div class="chart-card-body">
    <div id="chart-a" style="width:100%;height:100%;"></div>
  </div>
</div>
```

> **重要**：用 ECharts 时容器必须给定**显式高度**（chart-card-body 里 `height:100%`，外层 grid 用 `min-height: 0`），否则 chart 会塌成 0 高。

## 通用网格

```css
.kpi-grid    { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; flex: 1; }
.two-col     { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; flex: 1; min-height: 0; }
.three-col   { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; flex: 1; min-height: 0; }
```

**陷阱**：所有撑满高度的 grid/flex 容器**必须加 `min-height: 0`**，否则 grid item 撑不住会溢出。

## 分隔与底部结论

```html
<div class="divider"></div>                                    <!-- 1px 横线 -->
<div class="card-conclusion">{这张卡的小结，1-2 行}</div>
<div class="footer-conclusion">{这一页的总结，1-2 行}</div>
```

## insight-box（科普 / 原理说明）

```html
<div class="insight-box" style="border-left:3px solid var(--accent);">
  <div class="insight-title">{要科普的问题，反问句更好}</div>
  <div class="insight-text">
    {2-4 段解释，把<strong>关键概念</strong>用 strong 高亮}
  </div>
</div>
```

## 反模式

- ❌ 用 `<table>` 而不是 `metric-row` div
- ❌ chart 直接 `<canvas>` 不包 chart-card（没有标题、没有边距）
- ❌ 自定义颜色不走主题变量
- ❌ KPI 大数字不用 `var(--mono)` 等宽字体
