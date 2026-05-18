# ppt-report-generator assets

使用 `quickstart.sh` 一键初始化新项目（推荐），或手动拷贝：

```bash
# 推荐
./quickstart.sh ../my-report

# 或手动
cp -r assets ../my-report/src
cp assets/build.py assets/export_pdf.py assets/xlsx2json.py ../my-report/
cd ../my-report
mkdir -p src/slides src/data
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
├── data/                   # 三种格式都支持（优先级 json > xlsx > csv）
│   ├── slide-1.xlsx        # 推荐：多 sheet → JSON 顶层多 key
│   ├── slide-2.csv         # 单表数据 → JSON 数组
│   └── slide-3.json        # 复杂嵌套结构 / 机器生成
└── slides-templates/       # 5 套页面模板（拷贝 → 改名为 slide-N.html）
    ├── kpi-overview.html       # 多板块 × 多卡片总览
    ├── two-country.html        # 双对象左右对照（KPI + metric 表）
    ├── three-phase.html        # 三阶段时间线 + 多图表
    ├── multi-trend.html        # 多对象趋势对比
    └── supply-bars.html        # 分类条形 + 趋势折线
```

项目根（quickstart 自动放好）：
- `build.py` — 合成最终 HTML
- `xlsx2json.py` — Excel/CSV → JSON 转换器（被 build 调用，也可单跑）
- `export_pdf.py` — PDF 导出

## 添加一页

```bash
# 1. 选模板
cp src/slides-templates/two-country.html src/slides/slide-2.html

# 2. 写数据（在 Excel 里整理保存为 .xlsx，或直接写 csv / json）
cp ~/Downloads/我的数据.xlsx src/data/slide-2.xlsx

# 3. 写图表初始化（如有图表）
cat > src/scripts/slide-2.js <<'EOF'
function initSlide2() {
  const D = window.__DATA_2__;   // build 自动从 xlsx/csv/json 读取
  // ... 调用 renderXxx() 函数
}
EOF

# 4. 改文案、build
python3 build.py
open *.html
```

## 数据格式：xlsx / csv / json

**xlsx**（推荐日常用）：多个 sheet → `window.__DATA_N__` 顶层多个 key，每个 sheet 内容是 `[{表头: 单元格值}, ...]`。

```
slide-3.xlsx:
  sheet "kpis":  | label | value | unit |
                 | DAU   | 12.4  | 万   |
                 | ARR   | 48    | M USD|
  sheet "trend": | week | na   | eu  |
                 | W1   | 12.1 | 8.4 |
```

build 后 JS 里可以直接：

```js
function initSlide3() {
  const D = window.__DATA_3__;
  // D.kpis = [{label: 'DAU', value: 12.4, unit: '万'}, ...]
  // D.trend = [{week: 'W1', na: 12.1, eu: 8.4}, ...]
}
```

**csv**：单表 → 对象数组（=单 sheet 的 xlsx）。

**json**：原生格式，复杂嵌套时用（如带 markLine 的 ECharts marks 配置）。

约定：sheet/列名以 `_` 开头会被跳过，数字单元格自动转 number。详见 `xlsx2json.py` 顶部文档。

依赖：xlsx 需 `pip install openpyxl`（csv / json 标准库无依赖）。

## 独立调试 xlsx 转换

```bash
python3 xlsx2json.py src/data/slide-3.xlsx          # 输出到 stdout
python3 xlsx2json.py src/data/slide-3.xlsx > a.json # 写入文件
python3 xlsx2json.py src/data/                      # 整目录
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
