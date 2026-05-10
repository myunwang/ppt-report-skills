---
name: report-deck
description: 把数据汇报做成 16:9 网页版 PPT（设计稿 1600×900，浏览器自适应缩放），分页拆分源码 + 数据物理分离 + 多主题可切换 + ECharts 图表。当用户要"做月度/季度汇报"、"做工作汇报 PPT"、"把数据做成网页/PDF 形式的演示稿"，或希望复用一套"每页一个文件、数据单独存放、主题可换"的 PPT 模板时，**务必使用本 skill**。即使用户没说"PPT"二字，只要任务是把"多组数据 + 结论"产出为可演示/可分享的网页报告，也按本 skill 的工作流走。
---

# Report Deck — 网页版 PPT 模板

把"多组业务数据 + 阶段性结论"产出成一份 16:9 的、可在浏览器全屏播放、可一键导出 PDF 的网页版 PPT。

## 核心承诺（设计目标）

1. **每页 PPT = 三个文件**：`slides/slide-N.html` + `scripts/slide-N.js` + `styles/slide-N.css`，由 `build.py` 合成单一 HTML。改一页只动一页，**省 token、省冲突**。
2. **数据与渲染物理分离**：所有图表/表格的数据放在 `data/slide-N.json`（或顶部 `const DATA = {...}`），渲染代码只负责从数据生成 DOM/Chart。**下次更新只换数据**。
3. **图表选型有规则**：每种数据形态对应一种图表类型（见 `references/chart-mapping.md`），**不要随心情画图**。默认使用 **ECharts**。
4. **信息层次有硬规则**：标签 / 大标题 / 副标题（结论）/ 区块标题 / 卡片标题 / 正文 / 注释 / 辅助文字 8 级，每级字号、字重、颜色都固定（见 `references/design-system.md`）。
5. **多主题可切换**：5 套预设主题（modern-light / dark-tech / warm-business / brand-blue / minimal-mono），通过 `data-theme` 属性切换（见 `references/themes.md`）。

## 何时启用本 skill

触发条件（任意一条命中即用）：

- 用户说："做一份月度/季度/项目汇报"、"做工作汇报"、"做数据汇报 PPT"、"把数据做成可演示的网页"
- 用户给了一份原始数据（xlsx / 多个表格 / 一段文字描述结论）并希望产出"汇报"
- 用户已有一份这种结构的项目（`src/slides/`、`build.py`、`shell.html`）想新增一页或换主题
- 用户想"把这个 PPT 沉淀下来下次复用"

## 工作流（标准步骤）

### Step 1 — 理解输入与产出

- 问清楚（如果不知道）：**几页？每页讲什么？关键数据在哪？目标读者是谁？要不要 PDF？**
- 不要直接动手画图。先把每页的 **(label, title, subtitle/结论, 主体类型)** 列出来给用户确认。

### Step 2 — 选模板（每页）

打开 `assets/slides-templates/`，按页面"主体类型"挑一个起点：

| 主体类型 | 模板 | 用法 |
|---|---|---|
| 月度交付总览（多板块 × 多卡片） | `kpi-overview.html` | 第 1 页类汇总页 |
| 两个对象左右对照（如两国数据） | `two-country.html` | KPI 行 + 双卡片 metric 表 |
| 三阶段闭环 + 多个图表 | `three-phase.html` | 时间线 + 多 chart-card |
| 多对象时间趋势 | `multi-trend.html` | 4 国 / 4 渠道 折线图 + 里程碑标记 |
| 分类条形 + 趋势折线组合 | `supply-bars.html` | 物料/品类 mini-bar + 总趋势 |

模板是骨架，**复制后改文案、改数据、改 ID** 即可。

### Step 3 — 数据放进 `data/slide-N.json`

**这一步最重要**。每页的数据写成独立 JSON：

```json
{
  "kpis": [{ "num": "{value}", "label": "{指标名}", "sub": "{口径说明}" }],
  "trend": { "labels": ["W1", "W2", "..."], "series": [{ "name": "对象 A", "data": [/* numbers */] }] }
}
```

`scripts/slide-N.js` 通过 `fetch('./data/slide-N.json')` 或在 build 时内联读取。下次更新数据**只改 JSON**，不动渲染代码。

### Step 4 — 选图表（看 `references/chart-mapping.md`）

不要直接选自己想画的图。根据数据形态查决策表：

- 时间序列 → 折线（带里程碑竖线 plugin）
- 对照实验前后对比 → 100% 堆叠条形
- 对象排名（Top 20） → 横向 mini-bar（自定义 div，不用 chart 库）
- 多对象单期对比 → 分组条形
- 占比/构成 → **不要饼图**，用 100% 堆叠条形或矩形树图

### Step 5 — 信息层次（看 `references/design-system.md`）

每段文字必须能回答"我是哪一级"。slide-label / slide-title / slide-subtitle 三件套是**强制顶部结构**。结论里的关键数字必须包 `<strong>` 或 `<span class="pos|neg|warn">` 高亮。

### Step 6 — 构建与预览

```
python3 build.py            # 合成最终 HTML（文件名可在 build.py 顶部 CONFIG 改）
open *.html                 # 浏览器打开，按 ←/→ 翻页
python3 export_pdf.py       # （可选）导出 PDF
```

### Step 7 — 主题切换（可选）

如果用户想换风格，**不要重写 CSS**。在 `<body data-theme="dark-tech">` 上改 attribute 即可。详见 `references/themes.md`。

## 黄金规则（违反会被 review 打回）

1. **不要把数据写死在渲染代码里**。数据进 `data/slide-N.json` 或顶部 const 变量，渲染函数只接受参数。
2. **不要让一页 HTML 超过 200 行**。超了就拆子组件或挪到 JS 渲染。
3. **不要堆字号自由发挥**。只用 `--fs-label / --fs-title / --fs-subtitle / --fs-h2 / --fs-h3 / --fs-body / --fs-caption / --fs-mini` 8 个级别。
4. **不要用饼图展示 5 项以上的占比**。改用 100% 堆叠条形。
5. **不要硬编码颜色**。用 `var(--accent)`、`var(--accent2)` 等主题变量，确保切主题不崩。
6. **每页都要有 `slide-label`、`slide-title`、`slide-subtitle`** 三件套。subtitle 必须是**一句结论**，含关键数字。
7. **设计稿固定 1600×900**。所有元素按这个像素来定，浏览器自适应由 `transform: scale(--fit)` 自动处理。**不要用 vw/vh**。
8. **不要在 build 产物里手动改东西**。永远改 `src/`，再 `python3 build.py`。
9. **每页只回答一个问题，只有一个视觉锚点**。一页超过 12 个主体元素 = 拆两页（详见 `references/layout-principles.md` 第 6/10 节）。
10. **整份 deck 要有节奏**。不要 6 页全是高密度数据页，中间插"总览/呼吸/收尾"低密度页（详见 `layout-principles.md` 第 11 节"故事曲线"）。
11. **卡片边界必须严格对齐**：同行卡片底边齐、同列卡片左右边齐。靠 grid `1fr 1fr` + 子项 `flex:1 1 0; min-height:0` + 弹性占位（如 phase-arrow-v）补差，**不要写死 height**（详见 `layout-principles.md` 第 7b 节）。

## 详细参考文档

读取顺序按需：

- [`references/architecture.md`](references/architecture.md) — 拆分架构、build.py 工作原理、自适应缩放
- [`references/design-system.md`](references/design-system.md) — 字号 / 字重 / 颜色 / 间距硬规则（**字怎么写**）
- [`references/layout-principles.md`](references/layout-principles.md) — 经典汇报 PPT 布局法则：金字塔结构、F/Z 阅读路径、三分法、视觉锚点、信息密度、故事曲线（**东西怎么摆**）
- [`references/chart-mapping.md`](references/chart-mapping.md) — 数据形态 ↔ 图表选型决策表（ECharts 配置范本）
- [`references/components.md`](references/components.md) — 通用组件库（KPI / 卡片 / Phase / Timeline / Mini-bar / Metric-row）
- [`references/themes.md`](references/themes.md) — 5 套预设主题 + 自定义主题方法

## 资产清单

`assets/` 下都是**可直接拷贝**的成品文件：

- `shell.html` — HTML 骨架（含 `{{STYLES}}` `{{SLIDES}}` `{{SCRIPTS}}` 占位符）
- `build.py` — 合成脚本（按页号顺序拼接）
- `export_pdf.py` — PDF 导出（playwright + img2pdf）
- `styles/common.css` — 全局样式 + 5 套主题变量
- `styles/components.css` — 通用组件
- `scripts/common.js` — 自适应、导航、ECharts helper
- `scripts/theme-switcher.js` — 主题切换 UI
- `data/slide-N.json` — 数据样例
- `slides-templates/*.html` — 5 套页面模板

## 初始化新项目（推荐流程）

```bash
mkdir my-report && cd my-report
# 1. 拷贝 assets 整个目录到当前项目作为 src/
cp -r <skill_path>/assets src
# 2. 拷贝 build.py / export_pdf.py 到项目根
cp <skill_path>/assets/build.py <skill_path>/assets/export_pdf.py .
# 3. 按需挑模板，重命名为 slide-1.html / slide-2.html ...
# 4. 写数据 → 改文案 → build → 预览
```
