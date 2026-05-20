---
name: ppt-report-generator
description: 汇报 PPT 生成器 / 数据报告演示稿生成工具——把数据汇报做成 16:9 网页版 PPT（设计稿 1600×900，浏览器自适应缩放），可全屏播放、一键导出 PDF。分页拆分源码 + 数据物理分离 + 多主题可切换 + ECharts 图表。当用户要"做月度/季度汇报"、"做工作汇报 PPT"、"把数据做成网页/PDF 形式的演示稿"，或希望复用一套"每页一个文件、数据单独存放、主题可换"的 PPT 模板时，**务必使用本 skill**。即使用户没说"PPT"二字，只要任务是把"多组数据 + 结论"产出为可演示/可分享的网页报告，也按本 skill 的工作流走。
---

# PPT Report Generator — 汇报 PPT 生成器（网页版 PPT 模板）

把"多组业务数据 + 阶段性结论"产出成一份 16:9 的、可在浏览器全屏播放、可一键导出 PDF 的网页版 PPT。

## 核心承诺（设计目标）

1. **每页 PPT = 三个文件**：`slides/slide-N.html` + `scripts/slide-N.js` + `styles/slide-N.css`，由 `build.py` 合成单一 HTML。改一页只动一页，**省 token、省冲突**。
2. **数据与渲染物理分离**：所有图表/表格的数据放在 `data/slide-N.{xlsx,csv,json}`，build 时自动转 JSON 注入。**日常用 Excel 改数据**，渲染代码完全不动。
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
| 产业图谱 / 竞品全景 / 客户分层（一个领域/生态的完整图谱） | `landscape-map.html` | **⚠ 用前必读 [`references/landscape-skeleton.md`](references/landscape-skeleton.md) 选骨架** —— 这套三层 tier 只适合 AI/SaaS 软件分层栈；实体产业/航天/能源等用价值流横轴；银行用客户矩阵；创新药用研发管线。选错骨架 = 八股套用,会被一眼识破 |

模板是骨架，**复制后改文案、改数据、改 ID** 即可。

### Step 3 — 数据放进 `src/data/slide-N.{xlsx,csv,json}`

**这一步最重要**。日常推荐用 Excel/CSV，build 时自动转 JSON 注入到 `window.__DATA_N__`。

**三种格式都支持**（优先级 .json > .xlsx > .csv，同名只取一个）：

| 格式 | 适用场景 | 转换结果 |
|---|---|---|
| `.xlsx` | 日常推荐 — 数据本来就在 Excel 里 | 多 sheet 时：每个 sheet 名 → JSON 顶层一个 key |
| `.csv` | 单表数据，从某处导出 | 整份 → JSON 顶层一个 array |
| `.json` | 机器生成 / 复杂嵌套结构 | 直接读取 |

**约定**（详见 `references/architecture.md` 的"数据格式"小节）：
- 每个 sheet / csv 第 1 行是表头，后续每行 → 一个对象（`[{col: val}, ...]`）
- sheet 名 / 列名以 `_` 开头会被跳过（用作备注、辅助计算）
- 数字单元格自动转 number，其他保留 string

**xlsx 示例**：`src/data/slide-3.xlsx` 含 2 个 sheet 「kpis」「trend」 → JS 里访问：

```js
function initSlide3() {
  const D = window.__DATA_3__;
  // D.kpis  = [{label: 'DAU', value: 12.4, unit: '万'}, ...]
  // D.trend = [{week: 'W1', na: 12.1, eu: 8.4}, ...]
}
```

**下次更新数据**：直接在 Excel 里改完保存，重跑 `python3 build.py` — 渲染代码完全不动。

**独立调试**：`python3 xlsx2json.py src/data/slide-3.xlsx` 可单独跑转换看 JSON 输出。

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
python3 build.py            # 合成最终 HTML → 输出到 dist/（目录/文件名可在 build.py 顶部 CONFIG 改）
open dist/*.html            # 浏览器打开，按 ←/→ 翻页
python3 export_pdf.py       # （可选）导出 PDF（自动找 dist/，输出 dist/*.pdf）
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
12. **结构图/图谱类（landscape-map）的小块（chip）排版：内容在数据层规范，渲染层用固定尺寸 + 紧凑居中，绝不写 JS 去测尺寸反推字号"自适应铺满"**。
    - 数据层（最关键）：每个 chip 一个短词（≤ 4~5 字 / 一个英文术语）；「A / B」「A + B」合并项拆成多个独立 chip（同类就多放几个）；英文用业内简写（DSSM / MMoE / ANN）。PPT 文案本就不该超长——从源头杜绝截断。
    - 渲染层：chip 用 CSS 固定字号（`landscape-map` 模板里是 15px / 嵌套 13px），整图按内容自然高度、在 slide 剩余空间垂直居中，**不强求铺满**（咨询报告风：克制紧凑 + 居中 = 专业；硬撑铺满反而廉价且会引入截断/重叠）。
    - **严禁**：写 JS 逐卡或全局测量卡片尺寸去反推 chip 字号做"铺满自适应"——这条路（cqh / 二分逼近 / 等宽 / 全局系数 / logo 异步重算）已被反复验证为死结，且自动检测在本项目嵌套 flex/grid + 异步 logo 结构下与肉眼系统性不一致，会误判。
    - 生成第一版后用 LLM 看截图复查；若某 chip 文字超出（规范文案不会发生）→ 精简文案 / 拆 chip 重跑，**不要去改渲染逻辑**。
13. **"产业全景图" / "行业图谱"类页面，先选骨架,再写 chip**。不要见到"全景图"就反射式套 `landscape-map` 三层 tier 模板 —— **那只是 AI / SaaS 软件分层栈的专用骨架,不适用所有行业**。
    - 实体产业 / 航天 / 能源 / 制造 → **价值流横轴**(原料→生产→流通→服务)
    - 银行 / 保险 / 券商 / 咨询 → **客户矩阵**(纵轴客户分层 × 横轴产品 / 渠道)
    - 生物医药 / 新药研发 → **研发管线时间轴**(已上市 → III 期 → II 期 → I 期 → 临床前)
    - 平台型 / 生态型(微信 / 阿里) → **生态网络图**(中心节点 + 放射状外围)
    - 通用 AI / 软件分层栈 → **landscape-map 三层 tier** ✓
    - **强制流程:** 任何"产业全景图"类任务,先读 [`references/landscape-skeleton.md`](references/landscape-skeleton.md) 选定骨架,在 slide 顶部 HTML 注释里写下"骨架 + 理由",再开始动手。选错骨架会被一眼识破"参考案例呆板"——这条规矩是 SpaceX IPO Deck 那次教训沉淀的。

## 详细参考文档

读取顺序按需：

- [`references/architecture.md`](references/architecture.md) — 拆分架构、build.py 工作原理、自适应缩放
- [`references/design-system.md`](references/design-system.md) — 字号 / 字重 / 颜色 / 间距硬规则（**字怎么写**）
- [`references/layout-principles.md`](references/layout-principles.md) — 经典汇报 PPT 布局法则：金字塔结构、F/Z 阅读路径、三分法、视觉锚点、信息密度、故事曲线（**东西怎么摆**）
- [`references/chart-mapping.md`](references/chart-mapping.md) — 数据形态 ↔ 图表选型决策表（ECharts 配置范本）
- [`references/components.md`](references/components.md) — 通用组件库（KPI / 卡片 / Phase / Timeline / Mini-bar / Metric-row）
- [`references/themes.md`](references/themes.md) — 5 套预设主题 + 自定义主题方法
- [`references/landscape-skeleton.md`](references/landscape-skeleton.md) — **「产业全景图」骨架选择强制流程**(5 种骨架: 分层栈 / 价值流横轴 / 客户矩阵 / 研发管线 / 生态网络)。做全景图前**先读这个**,选定骨架再开工,避免见到"全景图"就套 landscape-map 八股
- [`references/landscape-qa.md`](references/landscape-qa.md) — landscape-map / 结构图类页面生成后的质量自检与优化清单（踩坑黑名单 · 数据规范 · 渲染自检 · LLM 二次复查），生成此类页面后**逐条对照**(注:仅在选定骨架是「A 分层栈」后才用本清单;其他骨架不适用)

## 资产清单

`assets/` 下都是**可直接拷贝**的成品文件：

- `shell.html` — HTML 骨架（含 `{{STYLES}}` `{{SLIDES}}` `{{SCRIPTS}}` 占位符）
- `build.py` — 合成脚本（按页号顺序拼接；同时把 src/assets/ 拷进 dist/）
- `export_pdf.py` — PDF 导出（playwright + img2pdf）
- `fetch_logos.py` — 可选：把在线 logo 下载缓存到本项目 src/assets/logos/ 供离线/存档（landscape-map 默认在线引用 logo，不跑此脚本也能显示，跑了则断网也不丢）
- `styles/common.css` — 全局样式 + 5 套主题变量
- `styles/components.css` — 通用组件
- `scripts/common.js` — 自适应、导航、ECharts helper
- `scripts/theme-switcher.js` — 主题切换 UI
- `data/slide-N.json` — 数据样例
- `slides-templates/*.html` — 6 套页面模板（含 landscape-map 产业图谱）

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
