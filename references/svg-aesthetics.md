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

**正确做法 — 两个素材来源,按"档次"选:**

| 档次 | 用途 | 来源 | 风格 |
|---|---|---|---|
| 🥉 **火柴人级** | 团队 pictogram(多人 / N×100) · 信息密度优先 | OpenMoji 1F9CD | 线条 / 简洁 / 可识别 |
| 🥇 **剪影级** ⭐ | 用户画像 / 能力地图 / 风险热图 · 视觉冲击力优先 | Wikimedia Commons 单 path 剪影 | 实心剪影 / 专业 / 咨询报告标杆感 |

**剪影级是 PPT 标杆级别**(像麦肯锡 / BCG 报告里那种站立人剪影 + 周边气泡标签的页型) —
火柴人在 1:1 比例下显得"卡通可爱",一旦放大成主体就立刻显得**业余 / 丑萌**。
若整张页面只有 1 个人体做主角,**必须用剪影级**;若是多人 pictogram(N 个 100 人小图标)火柴人才合适。

### 火柴人版本(OpenMoji 1F9CD)

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

### 剪影版本(Wikimedia Commons 标杆级)⭐

> **何时用:** 整页主体是单个人体作主角(用户画像 / 拟人化能力 / 风险热图)时,**必须用剪影**。
> 火柴人放大后会立刻显业余。
> 实战教训:OpenAI deck 第一版用火柴人,用户反馈"丑萌";换成剪影后视觉档次直接咨询报告级。

**下载剪影**(Wikimedia Commons,CC0 / 公共域):

```bash
# 站立男(细线条 8K,推荐:姿态自然,双手下垂)
curl -fsSL -A "Mozilla/5.0" "https://upload.wikimedia.org/wikipedia/commons/8/8e/Silhouette_of_a_standing_man.svg" -o silhouette-man.svg

# 通用人体(医学解剖图风,正面对称)
curl -fsSL -A "Mozilla/5.0" "https://upload.wikimedia.org/wikipedia/commons/8/89/SVG_Human_Silhouette.svg" -o silhouette-body.svg
```

**剪影 SVG 结构(单 path,直接 inline):**

```svg
<svg viewBox="0 0 210 297" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">
  <!-- 部位高亮(在剪影下面!) -->
  <circle cx="105" cy="40" r="35" fill="#3b82f6" fill-opacity="0.30"/>     <!-- 头 -->
  <ellipse cx="105" cy="150" rx="50" ry="40" fill="#10b981" fill-opacity="0.25"/>  <!-- 胸/心 -->
  <circle cx="55" cy="170" r="22" fill="#f59e0b" fill-opacity="0.40"/>     <!-- 左手 -->
  <circle cx="155" cy="170" r="22" fill="#f59e0b" fill-opacity="0.40"/>    <!-- 右手 -->
  <ellipse cx="105" cy="260" rx="40" ry="30" fill="#8b5cf6" fill-opacity="0.30"/>  <!-- 腿 -->

  <!-- 剪影 path(用 Wikimedia 下载,长达 8K 字符,这里省略 d 内容) -->
  <path fill="#0f172a" d="..."/>
</svg>
```

**剪影坐标系(站立男 210×297):**

| 部位 | 坐标 | 高亮圆建议大小 |
|---|---|---|
| 头 | (105, 40) | r=35 |
| 颈 | (105, 65) | r=12 |
| 胸 / 心 | (105, 105) | rx=45 ry=30 |
| 腰 | (105, 150) | rx=40 ry=25 |
| 左手 | (55, 170) | r=22 |
| 右手 | (155, 170) | r=22 |
| 大腿 | (105, 215) | rx=50 ry=35 |
| 小腿 | (105, 260) | rx=40 ry=30 |
| 脚 | (88, 280) / (122, 280) | r=12 |

**path 太长?抽到 JS 共享:**

8K 的 path 字符串,若 N 个 slide 都用,**抽到 `common.js` 作为常量** + JS 注入:

```js
// common.js
window.SILHOUETTE_MAN = `M 79 284 c -0.3 ...`;
window.injectSilhouette = (svg, color = '#0f172a', opacity = 1) => {
  const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  p.setAttribute('d', window.SILHOUETTE_MAN);
  p.setAttribute('fill', color);
  p.setAttribute('fill-opacity', opacity);
  svg.appendChild(p);
};

// slide-N.js
initSlide11 = () => {
  document.querySelectorAll('#s11 .silhouette-svg').forEach(svg => {
    injectSilhouette(svg);
  });
};
```

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

## 八、🔑 「剪影是怎么画出来的」完整方法论 ⭐⭐⭐

> 这一节回答"我怎么知道用哪个剪影 + 怎么挑出来 + 怎么塞进 deck"。
> 来源:实战教训(从火柴人 → 通用剪影 → 职场男女剪影 三轮迭代沉淀)。
> 灵感参考:[OmniSVG (NeurIPS 2025)](https://github.com/OmniSVG/OmniSVG) — VLM 端到端生成 SVG;
> 它需要 17-26GB GPU,本地跑不动,但**核心思想可以照搬**:**SVG 命令 token 化,先 plan 结构再补 geometry**。
> 我们用「人工版」的同一思想 — 先选剪影骨架,再叠部位高亮/标签。

### 方法论 5 步(下次任意"人体画像"页直接套):

**Step 1 · 确定档次** (svg-aesthetics 第三节)
- 单人主体占 ≥ 1/4 slide 面积 → **剪影级**(Wikimedia/OpenClipart/UXWing)
- N×100 人 pictogram / 每人 < 50px → **火柴人**(OpenMoji)

**Step 2 · 按"职业气质"挑剪影**(本节核心)

按 PPT 主题精准搜素材库 — **不要拿通用人体冒充职场**:

| 主题气质 | 关键词 | 推荐素材 |
|---|---|---|
| 通用 / 中性医学 | standing human silhouette | [Wikimedia: Silhouette_of_a_standing_man](https://commons.wikimedia.org/wiki/File:Silhouette_of_a_standing_man.svg) |
| 男 · 职场西装精英 ⭐ | businessman briefcase silhouette | [OpenClipart 321053 Businessman Stands](https://openclipart.org/detail/321053/businessman-stands) |
| 女 · 长发职业范 ⭐ | young businesswoman silhouette | [OpenClipart 310702 Young Businesswoman](https://openclipart.org/detail/310702/) |
| 女 · 职场胸像(avatar) | business women silhouette | [UXWing business-women-silhouette](https://uxwing.com/business-women-silhouette-icon/) |
| 男 · 跑动 | running businessman | OpenClipart 216499 |
| 庆功 / 成就 | businessman trophy stars | UXWing successful-businessman |
| 头像(头肩) | businesswoman icon | UXWing businesswoman / business-women-with-tie |

**搜素材库的搜索词模式:**
```
"{形态}" {气质} silhouette svg
形态: standing / walking / sitting / running / hands-on-hips
气质: business / professional / casual / executive / fitness
```

**Step 3 · 抓 + 验证**

```bash
# OpenClipart 直接下载格式
curl -fsSL -A "Mozilla/5.0" -L "https://openclipart.org/download/${ID}/" -o "person.svg"

# UXWing 直接下载格式
curl -fsSL -A "Mozilla/5.0" "https://uxwing.com/wp-content/themes/uxwing/download/{category}/{slug}.svg" -o "person.svg"

# 验证质量(必看)
grep -c '<path' person.svg     # ≤ 3 个 path 最佳;> 10 个就是详细插画,不是剪影
grep -o 'viewBox="[^"]*"' person.svg  # 必须有 viewBox
wc -c person.svg                # 1-20K 字节最佳;> 100K 通常是详细插画
```

**Step 4 · path 抽到 common.js(若 N 个 slide 复用)**

```js
// 1. 用 Python 提取 path d (避免手动复制丢字符):
//    src = Path('person.svg').read_text()
//    d = re.search(r'<path[^>]*\sd="([^"]+)"', src, re.S).group(1)
// 2. inject 到 common.js:

window.SILHOUETTE_MAN_PATH = "..."; // 西装男(OC 321053)
window.SILHOUETTE_WOMAN_PATH = "..."; // 长发职业女(OC 310702)
window.SILHOUETTE_VIEWBOX_MAN = "0 0 708 1066";
window.SILHOUETTE_VIEWBOX_WOMAN = "0 0 2334 1638";

window.injectSilhouette = function(svgEl, kind = 'man', color, opacity) {
  if (!svgEl) return;
  const path = kind === 'woman' ? SILHOUETTE_WOMAN_PATH : SILHOUETTE_MAN_PATH;
  const vb = kind === 'woman' ? SILHOUETTE_VIEWBOX_WOMAN : SILHOUETTE_VIEWBOX_MAN;
  svgEl.setAttribute('viewBox', vb);
  const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  p.setAttribute('d', path);
  p.setAttribute('fill', color || '#0f172a');
  if (opacity != null) p.setAttribute('fill-opacity', opacity);
  svgEl.appendChild(p);
};
```

**Step 5 · 找部位锚点坐标**

每个剪影 viewBox 不同,部位坐标必须重新校准。**最快方法:画网格目测**。

```html
<svg viewBox="0 0 708 1066">
  <!-- 透明网格,只在校准时显示,完成后删掉 -->
  <g stroke="#cbd5e1" stroke-width="2" opacity="0.4">
    <line x1="0" y1="100" x2="708" y2="100"/>
    <line x1="0" y1="200" x2="708" y2="200"/>
    ...
    <line x1="350" y1="0" x2="350" y2="1066"/>
  </g>
  <text x="5" y="100" font-size="20">y=100</text>
  ...
  <!-- 剪影 -->
  <path fill="#0f172a" d="..."/>
</svg>
```

截图目测 → 记下头/胸/手/腿坐标 → 高亮圆按这些坐标画 → 删网格。

### 关键认知

1. **剪影不是 AI 画出来的,是「找 + 适配」出来的**。LLM 写 path 永远丑(除非是 OmniSVG 那种 VLM)。
2. **气质决定一切**。"通用人体"和"职场男"在视觉档次上差 10 倍 — 选对气质 > 改进 path。
3. **男女应分开剪影**。混用一个剪影代表所有用户 → 看起来像数据库 user 占位图。男版「西装提包」+ 女版「长发耸肩」是经典咨询报告搭配。
4. **OmniSVG 的启示:先 plan 结构再补 geometry**。我们的 5 步就是它的人工版 —— 先选剪影(结构),再叠高亮(geometry)。

## 九、紧急救援:画完发现还是丑怎么办

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
