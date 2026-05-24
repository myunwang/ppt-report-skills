# SVG 美学 — 反丑强制流程

## 一、为什么 AI 画的 SVG 丑(诊断)

> 来自 [Why Graphic Design Is Hard for LLMs](https://davidmack.medium.com/why-graphic-design-is-hard-for-large-language-models-64ee67c4309c)
> + [Chat2SVG](https://chat2svg.github.io/) 论文

LLM 默认画 SVG 的 3 个致命毛病:

1. **坐标整数化、靠拍脑袋 → 比例失调**
   AI 默认写 `M 50 50 L 100 100` 这种整数,真实设计师用 `M 49.7 50.3 L 99.5 100.2` 浮点 + 黄金比例(1.618)/ 三分律。整数坐标导致所有形状都"棱角僵硬"。

2. **只用基础形状直接堆,无层次 → 视觉单调**
   AI 习惯 `<rect>+<circle>+<line>` 堆出"火柴人"。设计师用 `<path>` 一笔连贯绘制 + 弧形过渡 → 形成"自然剪影感"。

3. **颜色用纯色 + 无对比 / 无层次 → 廉价 PPT 感**
   AI 习惯 `fill="#3b82f6"` 单色填充。设计师用 1 主色 + 1 辅色 + 1 阴影色 + 透明度变化 → 形成深度。

## 二、5 大反丑原则(写 SVG 前必看)

### 原则 1 · 坐标用浮点 + 留余白(viewBox padding)

```svg
<!-- ✗ 丑:整数,贴边 -->
<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="50" /></svg>

<!-- ✓ 好:浮点,留 10% 余白 -->
<svg viewBox="0 0 100 100"><circle cx="50" cy="48" r="42" /></svg>
```

**为什么:** viewBox 内容贴边 = 设计稿无 margin = 业余感。所有内容**至少留 8-12% padding**。

### 原则 2 · 用 path 一笔画轮廓,而非多个基础形状拼接

```svg
<!-- ✗ 丑:火柴人(头 + 身体 + 4 肢分开) -->
<circle cx="50" cy="20" r="10" />
<line x1="50" y1="30" x2="50" y2="60" />
<line x1="50" y1="40" x2="30" y2="50" />
...

<!-- ✓ 好:连贯轮廓(剪影) -->
<path d="M 50 12 C 56 12 60 16 60 22 C 60 28 56 32 50 32
         C 56 34 62 38 64 46 L 68 70 L 60 70 L 56 50
         L 56 88 L 52 88 L 50 60 L 48 88 L 44 88 L 44 50
         L 40 70 L 32 70 L 36 46 C 38 38 44 34 50 32 Z" />
```

**为什么:** 一笔连贯的 path = 完整剪影 = 专业感;基础形状堆 = 卡通 / 业余。

### 原则 3 · 1 主色 + 1 辅色 + 透明度建立层次

```svg
<!-- ✗ 丑:全部硬色 -->
<path fill="#3b82f6" d="..." />
<path fill="#3b82f6" d="..." />

<!-- ✓ 好:主色 + 同色低透明阴影层 -->
<defs>
  <linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#3b82f6" />
    <stop offset="1" stop-color="#1e40af" />
  </linearGradient>
</defs>
<path fill="url(#g1)" d="..." />
<path fill="#3b82f6" fill-opacity="0.15" d="..." /> <!-- 阴影 / 高光 -->
```

**为什么:** 设计师都用 1 主色家族(同色相不同明度)+ 透明度;LLM 一上来 4 个不同 hue 调色板 = 显得乱。

### 原则 4 · stroke 比 fill 更显高级(在轮廓类图)

```svg
<!-- ✓ 线性 / 极简风:用 stroke,无 fill -->
<path fill="none" stroke="#0f172a" stroke-width="1.8"
      stroke-linecap="round" stroke-linejoin="round" d="..." />
```

**关键属性:**
- `stroke-width: 1.5 - 2.2`(根据 viewBox 大小,统一一个值);
- `stroke-linecap: round` + `stroke-linejoin: round` → 圆滑结尾,消除"硬角";
- `fill: none` → 纯轮廓线;若要填充用浅色 `fill: rgba(...,0.06)`。

### 原则 5 · 用 g 分组 + transform 而非重复坐标

```svg
<!-- ✗ 丑:复制粘贴 4 次坐标 -->
<path d="M 10 10 L 20 20" />
<path d="M 30 10 L 40 20" />
<path d="M 50 10 L 60 20" />

<!-- ✓ 好:定义一次 + transform 复用 -->
<g id="dot"><circle r="3" /></g>
<use href="#dot" x="10" y="10" />
<use href="#dot" x="30" y="10" />
<use href="#dot" x="50" y="10" />
```

**为什么:** 不仅简洁,还保证视觉精确一致(LLM 复制时常常 typo 一两个坐标导致歪斜)。

## 三、画复杂主体(人体 / 动物 / 物件)的铁律 ⭐ 实战重要

**绝不自己徒手写 ≥ 5 段 path 的复杂主体**。我反复踩坑验证:
- AI 拼头 + 身 + 四肢的多 path 写法,**头颈过渡永远会留缝隙**(头悬在脖颈上方像戴小帽子)
- 自己定关键点坐标 → 比例失调 → 整体比例像变形儿童画

**正确做法:** 直接从 **OpenMoji**(7 万设计师社区 / GitHub:hfg-gmuend/openmoji)抓现成的 SVG path,然后改 color/scale。

```bash
# 抓 OpenMoji 黑白线条版的某个 emoji(改 unicode 即可)
# 站立人:1F9CD  跑步人:1F3C3  上班族:1F468-200D-1F4BB(组合) 
curl -fsSL "https://raw.githubusercontent.com/hfg-gmuend/openmoji/master/black/svg/1F9CD.svg" > person.svg
```

**OpenMoji 人体范式(可直接 inline,改色即用):**

```svg
<svg viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg">
  <circle cx="35.4039" cy="10.6511" r="2.969" fill="none" stroke="#0f172a" stroke-width="2"/>
  <path fill="none" stroke="#0f172a" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
    d="M40.37,23.5891l1.9,38c.055,1.1-.575,2-1.4,2a2.076,2.076,0,0,1-1.729-1.987l-2.542-22.031c-.129-1.093-.679-1.987-1.229-1.987s-1.103.894-1.229,1.987l-2.539,22.031a2.076,2.076,0,0,1-1.729,1.987c-.825,0-1.455-.9-1.4-2l1.9-38"/>
  <path fill="none" stroke="#0f172a" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
    d="M26.3729,41.5891l.792-19a5.274,5.274,0,0,1,5.208-5h6"/>
  <path fill="none" stroke="#0f172a" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
    d="M38.3,17.589a5.274,5.274,0,0,1,5.208,5l.792,19"/>
</svg>
```

**部位高亮叠加范式:** 不要用 clip-path,**用透明圆形叠加最稳**(它自然不溢出,效果柔和)。

```svg
<!-- 在主体 SVG 末尾叠加 -->
<circle cx="35.4" cy="10.65" r="7" fill="#3b82f6" fill-opacity="0.18"/> <!-- 头 -->
<circle cx="35.4" cy="28"    r="9" fill="#10b981" fill-opacity="0.18"/> <!-- 胸 -->
<circle cx="26"   cy="35"    r="5" fill="#f59e0b" fill-opacity="0.20"/> <!-- 左手 -->
<circle cx="44.8" cy="35"    r="5" fill="#f59e0b" fill-opacity="0.20"/> <!-- 右手 -->
<circle cx="36"   cy="55"    r="9" fill="#8b5cf6" fill-opacity="0.15"/> <!-- 腿 -->
```

**变色版(实心剪影):** 不写新 path,只把上面 OpenMoji 的所有 `stroke="#0f172a"` 改成你要的颜色,`stroke-width` 加大到 8 → 自动变成实心剪影。

## 四、画人体轮廓的具体范式(若必须自己写)

### 范式 A · 线性极简人(咨询报告风)

```svg
<svg viewBox="0 0 100 160" xmlns="http://www.w3.org/2000/svg">
  <!-- 头 -->
  <circle cx="50" cy="22" r="11" fill="none" stroke="#0f172a"
          stroke-width="1.8" />
  <!-- 身躯 + 四肢 一笔轮廓 -->
  <path fill="none" stroke="#0f172a" stroke-width="1.8"
        stroke-linecap="round" stroke-linejoin="round"
        d="M 50 36
           C 60 36 66 42 68 52
           L 72 90
           M 50 36
           C 40 36 34 42 32 52
           L 28 90
           M 50 36
           L 50 92
           M 50 92
           L 42 138
           M 50 92
           L 58 138" />
</svg>
```

**要点:** 头 = circle,身体 + 手臂 + 腿 = 一个 path 连贯绘制(用 M 移动笔不抬起重启)。

### 范式 B · 剪影实心人(数据可视化 / 热图风)

```svg
<svg viewBox="0 0 100 160" xmlns="http://www.w3.org/2000/svg">
  <!-- 主轮廓 path:头 + 身体 + 四肢一笔闭合 -->
  <path fill="#94a3b8" d="
    M 50 8 C 57 8 62 13 62 20 C 62 27 57 32 50 32
    C 60 34 66 40 68 50
    L 72 88 L 64 88 L 60 56
    L 60 152 L 54 152 L 50 92
    L 46 152 L 40 152 L 40 56
    L 36 88 L 28 88
    L 32 50 C 34 40 40 34 50 32 Z" />
</svg>
```

**要点:** 一个闭合 path,fill 实色;可叠加几个透明色块代表"部位高亮"。

## 五、强制流程(写任何 SVG 前必做)

1. **先画在脑子里:** 这张图是 stroke 风(线性极简)还是 fill 风(剪影)?选定一种,不要混。
2. **先定 viewBox:** 高宽比按内容自然比例(人体 = 100×160 ≈ 黄金比例的反);**预留 8-12% padding**。
3. **先定 stroke-width / 主色:** 整张图统一,**不要每个元素自己定**。
4. **画完后自检:** 截图看,有没有"贴边"、"硬角"、"颜色乱"。出现就回到 1-3 重画,不要硬补。

## 六、判断你的 SVG 是否"好看"的 5 条自检

- [ ] 内容在 viewBox 内**居中且有余白**(不贴边)
- [ ] 主体形状由 ≥ 1 条**连贯 path** 组成,而非纯基础形状堆
- [ ] 整张图**主色 ≤ 2 个 hue**,深浅靠透明度 / 渐变
- [ ] stroke 用 `linecap:round + linejoin:round`(无硬角)
- [ ] 缩放到 50px 仍能看清主体(剪影测试)

## 七、紧急救援:画完发现还是丑怎么办

按优先级排查:
1. **viewBox 贴边了?** → 把内容整体缩小到 80% + 居中
2. **颜色太多?** → 砍到 1 主色 + 1 同色阴影
3. **基础形状堆得乱?** → 全删,换成 1 个 path
4. **stroke-width 不统一?** → 全局统一为 1.8 - 2.0
5. **还是丑?** → 老老实实去 [SVGRepo](https://www.svgrepo.com/) 找一个已有的 path 改改

---

> 配套:
> - 范式 path 代码本文档已包含,可直接复制
> - 参考: [LLM4SVG 论文](https://arxiv.org/abs/2412.11102)、[Chat2SVG](https://chat2svg.github.io/)
