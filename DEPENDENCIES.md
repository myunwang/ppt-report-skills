# 依赖说明（DEPENDENCIES）

本项目的依赖**分三层**，不只是 Python 包。按你实际用到的功能装即可——大多数情况下几乎不用装东西。

## 速查表

| 你要做的事 | 需要装什么 | 命令 |
|---|---|---|
| 用 CSV / JSON 数据，构建 deck | **什么都不用装** | `python3 build.py` |
| 用 Excel(.xlsx) 数据 | `openpyxl` | `pip install -r requirements.txt` |
| 浏览器里看含图表的页面 | 联网即可（ECharts 走 CDN） | — |
| 导出 PDF | playwright + img2pdf + Chromium | 见下方「PDF 导出」 |

## 三层依赖详解

### 1. 前端：ECharts（CDN，非 pip）

图表库 **ECharts 5.5.1** 通过 CDN 引入：

```
https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.min.js
```

- **不是 pip 包，也不是 npm 工程**——无需 `npm install`，无 `package.json`。
- 代价：渲染**含图表**的页面时需要**联网**（浏览器从 CDN 拉取）。纯文字/表格页面离线也能开。
- 如需完全离线：自行把 echarts.min.js 下载到本地并改 `shell.html` 里的 `<script src>`。

### 2. Python 核心：零依赖

- `build.py`（合成 HTML）只用 Python 标准库，**不需要 pip install 任何东西**。
- Python 版本要求：**3.8+**。

### 3. Python 按需依赖

**A. Excel 数据源 —— `openpyxl`**

仅当数据源是 `.xlsx` 时需要（`xlsx2json.py` 是懒加载，用 csv/json 完全不碰它）：

```bash
pip install -r requirements.txt
```

缺失时 `xlsx2json.py` 会给出明确提示：`读取 xxx.xlsx 需要 openpyxl。安装：pip install openpyxl`。

**B. PDF 导出 —— `playwright` + `img2pdf` + Chromium 二进制**

仅当需要导出 PDF（`export_pdf.py`）时需要。**两步，缺一不可**：

```bash
pip install -r requirements-pdf.txt
playwright install chromium      # 下载 Chromium 浏览器二进制（约 150MB）
```

> ⚠️ 只 `pip install` 是不够的。playwright 还要单独下载浏览器二进制，否则 `export_pdf.py` 会报 `Executable doesn't exist`。

## 一句话总结

只用 JSON/CSV、不导 PDF 的话——**零安装**，`python3 build.py` 直接跑。其余按上表对号入座。
