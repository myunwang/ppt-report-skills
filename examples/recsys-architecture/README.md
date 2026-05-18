# 范例 · 推荐系统分层架构图（landscape-map 模板实战）

`landscape-map` 模板的**可运行实战范例**。展示如何用产业图谱模板画一张
「召回 → 排序 → 重排」三层推荐系统架构图（咨询报告风，纯 CSS、不依赖 ECharts）。

## 直接看效果

```bash
open dist/recsys-architecture.html      # 已构建好的成品，右上角可切 5 套主题
```

## 自己重新构建

```bash
python3 build.py            # 合成 → dist/recsys-architecture.html
open dist/recsys-architecture.html
```

## 这个范例演示了什么

1. **landscape-map 模板的正确用法**：模板末尾的 `<style>` 块必须拆到
   `src/styles/slide-1.css`（build.py 只注入 `src/styles/slide-N.css`，
   不会解析 slide 片段内嵌的 `<style>`）—— 这是用此模板最容易踩的坑。
2. **12 栅格铁律**：每个 tier 的 `--span` 合计必须 == 12，否则 grid 折行留白。
   本例：Tier1 `3+3+3+3=12`、Tier2 `4+4+4=12`、Tier3 `6+6=12`。
3. **无 logo 场景**：item 是技术名词不是公司，所以不需要 `data-d` 和
   logo 注入脚本，`slide-1.js` 保持空 `initSlide1(){}` 即可。
4. **dist/ 输出约定**：产物统一进 `dist/`，源文件在 `src/`，互不混淆。

## 关键文件

| 文件 | 作用 |
|---|---|
| `src/slides/slide-1.html` | 三层架构 HTML 结构（12 栅格 tier） |
| `src/styles/slide-1.css`  | 从 landscape-map 模板提取的全部样式 |
| `src/scripts/slide-1.js`  | 空 init（本例无 logo） |
| `dist/recsys-architecture.html` | 构建产物（可直接打开） |
