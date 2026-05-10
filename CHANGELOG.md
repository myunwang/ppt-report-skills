# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] — 初次发布

### Added

- **6 份参考文档**（~1300 行）：
  - `references/architecture.md` — 拆分架构 + build.py 工作原理 + 自适应缩放
  - `references/design-system.md` — 8 级字号 / 字重 / 颜色 / 间距硬规则
  - `references/layout-principles.md` — 14 条经典 PPT 布局法则（含卡片边界对齐）
  - `references/chart-mapping.md` — 数据形态 ↔ 图表选型决策表 + ECharts 配置范本
  - `references/components.md` — 通用组件库
  - `references/themes.md` — 5 套预设主题 + 自定义方法
- **5 套页面模板**：kpi-overview / two-country / three-phase / multi-trend / supply-bars
- **5 套预设主题**：modern-light / dark-tech / warm-business / brand-blue / minimal-mono
- **核心脚本**：
  - `build.py` — 自动检测 N 个 slides，合成单 HTML
  - `export_pdf.py` — playwright + img2pdf，输出 13.33×7.5 inch 标准 16:9 PDF
  - `quickstart.sh` — 一键初始化新项目
- **ECharts 范本函数**：`renderDailyDual` / `renderShare100` / `renderMultiTrend` / `renderMiniBars` / `renderKpiGrid`
- 主题切换：右上角 5 按钮 + localStorage 持久化
- 11 条黄金规则（在 `SKILL.md` 顶部）

### 设计目标

工程化解决数据汇报 PPT 的 4 个老大难：

1. 改一个数字要重画整张图 → 数据进 JSON
2. 上下页字号不一致、卡片对不齐 → 8 级字号 + 卡片对齐规则
3. 想换风格要逐页重做 → CSS 变量 + 5 套预设
4. AI 协作 token 爆炸 → 每页 ≤ 200 行小文件
