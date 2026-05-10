# report-deck assets

把这个 `assets/` 目录拷贝到新项目作为 `src/`：

```bash
cp -r .claude/skills/report-deck/assets my-report/src
cp .claude/skills/report-deck/assets/build.py     my-report/build.py
cp .claude/skills/report-deck/assets/export_pdf.py my-report/export_pdf.py
cd my-report
```

## 目录

```
src/
├── shell.html              # HTML 骨架（含 {{TITLE}} {{STYLES}} {{SLIDES}} {{DATA}} {{SCRIPTS}} 占位）
├── styles/
│   ├── common.css          # 5 套主题变量 + 自适应缩放 + 顶部三件套
│   ├── components.css      # 通用组件库
│   └── slide-N.css         # 各页特殊样式
├── scripts/
│   ├── common.js           # 自适应 + 导航 + ECharts helper（含 4 个范本图函数）
│   ├── theme-switcher.js   # 主题切换
│   └── slide-N.js          # 每页一个 initSlideN()
├── data/
│   └── slide-N.json        # 每页数据，build.py 自动注入为 window.__DATA_N__
└── slides-templates/       # 5 套页面模板（拷贝 → 改名为 slide-N.html）
    ├── kpi-overview.html       # 月度交付总览（多板块 × 多卡片）
    ├── two-country.html        # 两个对象左右对照（KPI + metric 表）
    ├── three-phase.html        # 三阶段时间线 + 多图表
    ├── multi-trend.html        # 4 国/4 渠道日级趋势
    └── supply-bars.html        # 分类条形 + 趋势折线
```

## 添加一页

```bash
# 1. 选模板
cp src/slides-templates/two-country.html src/slides/slide-2.html

# 2. 写数据
echo '{"a": ..., "b": ...}' > src/data/slide-2.json

# 3. 写图表初始化（如有图表）
cat > src/scripts/slide-2.js <<'EOF'
function initSlide2() {
  const D = window.__DATA_2__;
  // ... 调用 renderXxx() 函数
}
EOF

# 4. 改文案、build
python3 build.py
open *.html
```

## 已包含的图表函数（在 common.js）

- `renderDailyDual(elId, labels, dur, vids, marks)` — 日级双 y 轴折线 + 里程碑竖线
- `renderShare100(elId, [前后两类], 系列名数组, preData, postData)` — 100% 堆叠条形
- `renderMultiTrend(elId, labels, {对象A: data, 对象B: data}, colorMap)` — 多对象趋势折线
- `renderMiniBars(containerId, [[name, val], ...], color)` — 横向 Top-N mini-bar（不用 chart 库）
- `renderKpiGrid(containerId, kpis)` — KPI 网格

## 主题切换

页面右上角自带切换按钮（5 套主题）。也可直接 `applyTheme('dark-tech')` 在控制台调用。

## 导出 PDF

```bash
pip install playwright img2pdf
playwright install chromium
python3 export_pdf.py
```
