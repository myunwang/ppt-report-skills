# report-deck

> 把数据汇报做成 16:9 网页版 PPT 的 Claude Code skill / 独立工程模板。
> **每页一个文件 · 数据物理分离 · ECharts · 5 套主题 · 一键导出 PDF**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-7c3aed.svg)](https://docs.claude.com/en/docs/claude-code/skills)

## 这是什么

一套把"数据汇报 → 网页 PPT"工程化的模板。**两种用法**：

1. **作为 Claude Code Skill 使用** — 把这个仓库放到 `~/.claude/skills/report-deck/`，让 Claude 自动按这套规范帮你做汇报
2. **作为独立工程模板使用** — 直接把 `assets/` 拷成 `src/`，运行 `python3 build.py` 合成单 HTML

## 它解决什么问题

PPT 工具（Keynote / 飞书文档 / Google Slides）做数据汇报有几个老大难：

- ❌ 改一个数字 → 整张图重画 → 半小时没了
- ❌ 上下页字号不一致、卡片对不齐、配色乱
- ❌ 想换风格？逐页重做
- ❌ Claude / GPT 想帮你改某一页？必须把整份发它，token 爆炸

`report-deck` 用工程化方法解决：

- ✅ **每页 = 3 个小文件**（HTML + CSS + JS），改一页只动 3 个 ≤ 200 行的小文件
- ✅ **数据放 JSON**（`data/slide-N.json`），下次更新只换数据
- ✅ **5 套预设主题**，右上角一键切换 — 商务深蓝 / 科技深色 / 暖色商业 / 浅色简约 / 极简单色
- ✅ **ECharts 图表 + 数据形态决策表**，告诉你什么数据用什么图（拒绝 5 项以上饼图）
- ✅ **8 级字号 / 4 级字重 / 11 条黄金布局规则** — 卡片边界严格对齐、不再"看着乱"
- ✅ **一键导 PDF**（playwright + img2pdf，13.33×7.5 inch 16:9 标准）

## 仓库提供什么

- **5 套页面模板**（`assets/slides-templates/`）：
  - `kpi-overview` — 多板块 × 多卡片总览
  - `two-country` — 双对象左右对照（KPI + metric 表）
  - `three-phase` — 三阶段时间线 + 多图表
  - `multi-trend` — 多对象趋势对比
  - `supply-bars` — 分类条形 + 趋势折线
- **5 套预设主题**：modern-light / dark-tech / warm-business / brand-blue / minimal-mono（右上角一键切，localStorage 持久化）
- **6 份参考文档**（`references/`，~1300 行）：架构 · 设计系统 · 布局法则 · 图表选型 · 组件 · 主题
- **构建脚本**：`build.py`（合成 HTML）+ `export_pdf.py`（导出 PDF）+ `quickstart.sh`（一键初始化新项目）

## 5 分钟上手（独立工程模式）

```bash
# 1. 克隆仓库
git clone https://github.com/<your-username>/report-deck.git
cd report-deck

# 2. 一键初始化新项目
./quickstart.sh ../my-report

# 3. 进项目，开始改
cd ../my-report
# 编辑 src/slides/slide-1.html / src/data/slide-1.json ...
python3 build.py
open *.html       # 浏览器打开，← / → 翻页

# 4.（可选）导出 PDF
pip install playwright img2pdf
playwright install chromium
python3 export_pdf.py
```

## 作为 Claude Code Skill 使用

```bash
# macOS / Linux
mkdir -p ~/.claude/skills
git clone https://github.com/<your-username>/report-deck.git ~/.claude/skills/report-deck
```

之后在 Claude Code 里直接说**"做一份月度汇报"** / **"把这个数据做成 PPT"**，Claude 会自动按本 skill 的规范工作流走：选页面模板 → 写 `data/slide-N.json` → 按 8 级字号 + 11 条布局规则排版 → 调用对应 ECharts 范本函数 → `build.py` 输出。

详见 [`SKILL.md`](SKILL.md)。

## 仓库结构

```
report-deck-skill/
├── SKILL.md                    # Skill 入口（Claude Code 加载这个）
├── README.md                   # 你正在看的文件
├── LICENSE                     # MIT
├── quickstart.sh               # 一键初始化新项目
├── references/                 # 设计哲学与规则（共 6 份 ~1300 行）
│   ├── architecture.md         # 拆分架构 + build.py 工作原理 + 自适应缩放
│   ├── design-system.md        # 8 级字号 / 字重 / 颜色 / 间距硬规则
│   ├── layout-principles.md    # 14 条经典 PPT 布局法则（含卡片边界对齐）
│   ├── chart-mapping.md        # 数据形态 ↔ 图表选型决策表 + ECharts 配置范本
│   ├── components.md           # 通用组件库（KPI / Phase / Mini-bar 等）
│   └── themes.md               # 5 套预设主题 + 自定义方法
└── assets/                     # 可直接拷贝的成品文件
    ├── shell.html              # HTML 骨架（占位符）
    ├── build.py                # 合成脚本（自动检测 N 个 slides）
    ├── export_pdf.py           # PDF 导出
    ├── styles/
    │   ├── common.css          # 5 套主题变量 + 自适应缩放
    │   └── components.css      # 通用组件
    ├── scripts/
    │   ├── common.js           # 自适应 + 导航 + 4 个 ECharts 范本函数
    │   └── theme-switcher.js   # 主题切换
    └── slides-templates/       # 5 套页面模板（拷贝 → 改名 slide-N.html）
        ├── kpi-overview.html       # 多板块 × 多卡片总览
        ├── two-country.html        # 双对象左右对照
        ├── three-phase.html        # 三阶段时间线 + 多图
        ├── multi-trend.html        # 多对象趋势对比
        └── supply-bars.html        # 分类条形 + 趋势折线
```

> 数据目录 `src/data/` 由 `quickstart.sh` 在初始化时为新项目创建，不预置示例数据。

## 核心理念（"黄金 11 条"）

1. 不要把数据写死在渲染代码里 → 进 `data/slide-N.json`
2. 不要让一页 HTML 超过 200 行
3. 字号只用 8 级 `var(--fs-*)`，不要随手加新字号
4. 5 项以上不用饼图（用 100% 堆叠条形）
5. 不要硬编码颜色 → 用 `var(--accent*)` 主题变量
6. 每页必有 label / title / subtitle 三件套，subtitle 含关键数字
7. 设计稿固定 1600×900，不要用 vw/vh
8. 永远改 `src/`，不要改 build 产物
9. 每页只回答一个问题，只有一个视觉锚点
10. 整份 deck 要有节奏（高/低密度交替）
11. **卡片边界必须严格对齐**：grid `1fr 1fr` + `flex:1 1 0; min-height:0` + 弹性占位补差，不写死 height

详见 [`references/`](references/)。

## 使用场景

- ✅ 月度 / 季度业务汇报
- ✅ 数据团队对内 / 对外 deck
- ✅ 立项汇报、项目复盘
- ✅ 有大量"对照实验 / 多对象趋势 / KPI 总览"图表的场景
- ⚠️ 不太适合：纯文字密集 deck（去看 docx skill）、需要复杂动画的演讲（去看 PowerPoint）

## 兼容性

- 浏览器：Chrome / Safari / Edge / Firefox（任意现代版本）
- Python：3.8+（仅 build.py 需要，无外部依赖；export_pdf.py 需要 playwright + img2pdf）
- ECharts：5.5.x（CDN 引入）
- Claude Code：作为 skill 使用需 Claude Code CLI

## License

[MIT](LICENSE) — 随意使用、修改、分发。

## 致谢

每一条规则都从做汇报踩过的坑里长出来。

## 反馈与贡献

欢迎 issue / PR：

- 提交新的页面模板（带截图）
- 增加新主题预设
- 修正某条布局规则
- 翻译文档（目前主要是中文）

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。
