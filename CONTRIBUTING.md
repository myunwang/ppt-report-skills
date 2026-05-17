# 贡献指南

感谢你对 `ppt-report-generator` 感兴趣！本指南介绍如何提交问题与改动。

## 提 Issue

适合提 issue 的几类情况：

- **🐛 Bug**：构建失败、布局崩溃、PDF 导出报错。请附：
  - 操作系统 / 浏览器版本
  - 复现步骤（最好 5 行内）
  - `python3 build.py` 的完整输出
  - 截图（特别是布局问题）
- **💡 新模板请求**：你有一种数据形态本仓库未覆盖（比如"漏斗 + 桑基图组合"），可以开 issue 描述你的数据形状和想要的视觉效果
- **📐 规则讨论**：对 `references/` 里的某条规则有不同意见 → 欢迎讨论
- **📚 文档错漏**：拼写、链接坏了、示例代码跑不通

## 提 PR

### 添加新页面模板

1. 在 `assets/slides-templates/` 加 `<your-template>.html`
2. 在 `references/components.md` 末尾说明用法（数据形状、对应 JS 渲染函数）
3. 提交一份用本模板做的截图到 `docs/screenshots/`
4. 在 `SKILL.md` 的"模板对照表"加一行
5. **PR 描述里附使用场景**：什么时候选这个模板而不是已有的 5 个

### 添加新主题

1. 在 `assets/styles/common.css` 加一段 `[data-theme="your-theme"] { --... }`
2. 在 `assets/scripts/theme-switcher.js` 的 `THEMES` 数组里 push
3. 在 `references/themes.md` 加一节描述（适用场景 + 字体偏好 + 截图）
4. **PR 必须附**：5 套主题在同一页上的并排截图

### 修改现有规则

`references/` 里的规则不是教条，是经验。如果你认为某条规则应该改：

1. PR 描述里写**反例**——什么场景下原规则失效
2. 给出**修正后的版本**，包含 "Why" 和 "How to apply"
3. 如果会导致 breaking change（比如 CSS 变量改名），说明迁移路径

## 代码风格

- HTML / CSS / JS：跟随现有文件的缩进（2 空格）和命名（kebab-case 的 class）
- Python：PEP 8，但不用为 `build.py` / `export_pdf.py` 引入新依赖（保持开箱即用）
- 注释：只解释**为什么**，不解释**做什么**（命名应能说话）
- 中文文档可以混排英文术语，不强制

## 提交信息

参考 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)：

```
feat(template): add funnel-with-sankey template
fix(build): handle empty data/ directory
docs(layout): clarify min-height: 0 rule with example
chore: bump echarts CDN to 5.5.2
```

## 本地验证

提 PR 前请确认：

```bash
# 1. 用 quickstart 起一个测试项目
./quickstart.sh /tmp/test-deck

# 2. 把模板复制成 slides 试构建
cd /tmp/test-deck
cp src/slides-templates/<your-new-template>.html src/slides/slide-1.html
python3 build.py

# 3. 浏览器打开看不崩
open *.html

# 4. JSON / Python 语法没错
python3 -m py_compile build.py export_pdf.py
```

## 行为准则

请保持友好与建设性。优先讨论想法，再讨论具体实现。
