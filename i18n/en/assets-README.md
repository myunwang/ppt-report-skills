# ppt-report-generator assets

Use `quickstart.sh` to initialize a new project in one step (recommended), or copy manually:

```bash
# recommended
./quickstart.sh ../my-report

# or manually
cp -r assets ../my-report/src
cp assets/build.py assets/export_pdf.py assets/xlsx2json.py ../my-report/
cd ../my-report
mkdir -p src/slides src/data
```

## Directory

```
src/
├── shell.html              # HTML skeleton (with {{TITLE}} {{STYLES}} {{SLIDES}} {{DATA}} {{SCRIPTS}} placeholders)
├── styles/
│   ├── common.css          # 5 theme variables + adaptive scaling + top trio
│   ├── components.css      # common component library
│   └── slide-N.css         # per-slide special styles
├── scripts/
│   ├── common.js           # adaptive + navigation + ECharts helper (includes 4 sample chart functions)
│   ├── theme-switcher.js   # theme switching
│   └── slide-N.js          # one initSlideN() per slide
├── data/                   # all three formats supported (priority json > xlsx > csv)
│   ├── slide-1.xlsx        # recommended: multiple sheets → multiple top-level JSON keys
│   ├── slide-2.csv         # single-table data → JSON array
│   └── slide-3.json        # complex nested structure / machine-generated
└── slides-templates/       # 5 slide templates (copy → rename to slide-N.html)
    ├── kpi-overview.html       # multi-section × multi-card overview
    ├── two-country.html        # two-object side-by-side comparison (KPI + metric table)
    ├── three-phase.html        # three-phase timeline + multiple charts
    ├── multi-trend.html        # multi-object trend comparison
    └── supply-bars.html        # category bars + trend line
```

Project root (quickstart places these automatically):
- `build.py` — assemble the final HTML
- `xlsx2json.py` — Excel/CSV → JSON converter (called by build, can also run standalone)
- `export_pdf.py` — PDF export

## Adding a Slide

```bash
# 1. pick a template
cp src/slides-templates/two-country.html src/slides/slide-2.html

# 2. write data (organize in Excel and save as .xlsx, or write csv / json directly)
cp ~/Downloads/my-data.xlsx src/data/slide-2.xlsx

# 3. write chart initialization (if there are charts)
cat > src/scripts/slide-2.js <<'EOF'
function initSlide2() {
  const D = window.__DATA_2__;   // build reads automatically from xlsx/csv/json
  // ... call renderXxx() functions
}
EOF

# 4. edit copy, then build
python3 build.py
open *.html
```

## Data Formats: xlsx / csv / json

**xlsx** (recommended for daily use): multiple sheets → multiple top-level keys in `window.__DATA_N__`, where each sheet's content is `[{header: cell value}, ...]`.

```
slide-3.xlsx:
  sheet "kpis":  | label | value | unit |
                 | DAU   | 12.4  | 万   |
                 | ARR   | 48    | M USD|
  sheet "trend": | week | na   | eu  |
                 | W1   | 12.1 | 8.4 |
```

After build, in JS you can directly use:

```js
function initSlide3() {
  const D = window.__DATA_3__;
  // D.kpis = [{label: 'DAU', value: 12.4, unit: '万'}, ...]
  // D.trend = [{week: 'W1', na: 12.1, eu: 8.4}, ...]
}
```

**csv**: single table → array of objects (= a single-sheet xlsx).

**json**: native format, used for complex nesting (e.g. an ECharts marks config with markLine).

Convention: sheet/column names starting with `_` are skipped, and numeric cells are auto-converted to number. See the documentation at the top of `xlsx2json.py` for details.

Dependency: xlsx requires `pip install openpyxl` (csv / json use the standard library, no dependencies).

## Standalone Debugging of xlsx Conversion

```bash
python3 xlsx2json.py src/data/slide-3.xlsx          # output to stdout
python3 xlsx2json.py src/data/slide-3.xlsx > a.json # write to file
python3 xlsx2json.py src/data/                      # whole directory
```

## Included Chart Functions (in common.js)

- `renderDailyDual(elId, labels, dur, vids, marks)` — daily dual-y-axis line + milestone vertical lines
- `renderShare100(elId, [before & after categories], series name array, preData, postData)` — 100% stacked bars
- `renderMultiTrend(elId, labels, {objectA: data, objectB: data}, colorMap)` — multi-object trend line
- `renderMiniBars(containerId, [[name, val], ...], color)` — horizontal Top-N mini-bar (no chart library)
- `renderKpiGrid(containerId, kpis)` — KPI grid

## Theme Switching

The page comes with a switch button in the top-right corner (5 themes). You can also call `applyTheme('dark-tech')` directly in the console.

## Exporting PDF

```bash
pip install playwright img2pdf
playwright install chromium
python3 export_pdf.py
```
