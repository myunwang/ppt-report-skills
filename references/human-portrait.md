# Human Portrait / 人体画像 — 设计与数据规范

> 适用:`human-portrait.html` 模板 — 把"对象画像 / 能力拟人 / 风险热图"等需要**中央人体 + 周边标签 + 部位高亮**的页型。
>
> 这是真正的**异形容器**类页型(对比 2×2 矩阵那种 grid 套出来的规则页)—
> 难在 SVG 人体比例 + 部位坐标 + 标签防遮挡 + 引线连接。

## 一、什么场景适合人体画像?

✓ **对象画像** — 典型客户/用户像谁(职业/动机/场景/地域/设备)
✓ **能力拟人化** — 把抽象能力(推理/视觉/语音/工具/Agent)映射到身体部位
✓ **风险/影响热图** — 颜色深浅表示不同部位/职业受影响程度
✓ **团队 pictogram** — N 个小人代表 N×100 人,展示组织结构(变体)

✗ 不适合:数据是纯数字关系(用散点 / 矩阵)
✗ 不适合:对象本身是产品/服务(用价值流 / 流程图)
✗ 不适合:讲故事不需要"人"作为锚点

## 二、SVG 人体的三档 × 男女分身 ⭐ 关键决策(实战教训)

三轮迭代教训:
- v1 全用 OpenMoji 火柴人 → 用户反馈"丑萌"
- v2 改 Wikimedia 通用站立人剪影 → 视觉好但"姿势丑、没气质"
- v3 ⭐ 改 OpenClipart 职场男女剪影 → 真正的咨询报告级气质

**最佳实践:** 男 / 女分身 + 按主体大小选档次。

| 档次 | 用途 | 推荐素材 |
|---|---|---|
| 🥇 **职场剪影级**(主体大) | 用户画像 / 能力地图 / 风险热图 | [OpenClipart 321053 男西装提包](https://openclipart.org/detail/321053/) + [310702 女长发耸肩](https://openclipart.org/detail/310702/) |
| 🥈 通用剪影 | 中性 / 医学 / 解剖类(非职场主题) | [Wikimedia Standing Man Silhouette](https://commons.wikimedia.org/wiki/File:Silhouette_of_a_standing_man.svg) |
| 🥉 **火柴人**(主体小) | N×100 人 pictogram(团队结构) | [OpenMoji 1F9CD](https://raw.githubusercontent.com/hfg-gmuend/openmoji/master/black/svg/1F9CD.svg) |

**判断标准:**
- 单人体占 slide ≥ 1/4 面积,且 PPT 是商务主题 → **职场剪影级 + 按场景挑男 / 女**
- 中性医学主题 → 通用剪影
- 每个人 < 50px → 火柴人(剪影会糊)

**男女配对:** 一份 deck 里若有 ≥ 2 张人像页,**交替男 / 女**(避免重复) — OpenAI deck v3:
- slide-11 用户画像 → 男(西装提包,代表"知识工作者")
- slide-13 能力地图 → 女(双手摊开,适合"能力展示")
- slide-14 职业风险 → 男(同 slide-11 风格,贯穿)

详见 [`svg-aesthetics.md`](svg-aesthetics.md) 第三 + 第八节(完整方法论)。

## 三、4 种变体(按 OpenAI deck v2 实现的)

| # | 变体 | 档次 | 关键 SVG 处理 | 参考实现 |
|---|---|---|---|---|
| 1 | **用户画像** — 中央 1 人 + 5 标签四角 + 引线 | 🥇 剪影 | 剪影 + 5 部位高亮圆 + dashed path 引线 | `openai-ipo-deck/slide-11` |
| 2 | **团队 pictogram** — N 个小人按团队着色 | 🥉 火柴人 | JS 动态生成 OpenMoji 小人 | `openai-ipo-deck/slide-12` |
| 3 | **能力拟人** — 1 人 + 6 部位高亮 + 左右能力卡 | 🥇 剪影 | 剪影 + 头/眼/耳/心/手/腿 6 部位高亮 | `openai-ipo-deck/slide-13` |
| 4 | **风险热图** — 1 人 + 部位按颜色深浅 + 左右职业卡 | 🥇 剪影 | 剪影 + 红/黄/绿渐变高亮 + 底部色阶 | `openai-ipo-deck/slide-14` |

## 三、铁律 ⭐(踩坑后总结)

### 3.1 SVG 人体永远抄 OpenMoji,不要自己画

详见 `references/svg-aesthetics.md` 第三节。一句话:**自己写 path 永远会在头颈过渡踩坑**,直接用 OpenMoji 1F9CD。

```bash
curl https://raw.githubusercontent.com/hfg-gmuend/openmoji/master/black/svg/1F9CD.svg
```

### 3.2 viewBox 必须用 OpenMoji 原坐标系(72×72)⚠ 实战必踩

**反面教训:** 一开始用 `viewBox="0 0 200 340"` + 把 OpenMoji 用 `transform: scale(2.778)` 放大。
**结果:** 部位高亮圆按 200×340 坐标画,但人体只占了上半部分 → 心脏画在腿上、手画在身体外。

**正确做法:** 整个 SVG **直接用 OpenMoji 的 72×72 坐标系**(可适当扩大 viewBox 高度给底部图例,比如 72×100)。
所有内容(高亮圆/人体/图例)**全部用原始小坐标**,通过 CSS `width:100%; height:100%` 让 SVG 自动缩放到容器大小。

```svg
<!-- ✓ 正确:全部用 72×N 原坐标系 -->
<svg viewBox="0 0 72 80" preserveAspectRatio="xMidYMid meet">
  <circle cx="35.4" cy="10.65" r="8" fill="#3b82f6" fill-opacity="0.18"/>
  <!-- OpenMoji 原坐标 -->
  <circle cx="35.4039" cy="10.6511" r="2.969" .../>
  ...
</svg>

<!-- ✗ 错误:viewBox 200×340 + transform scale → 坐标系撕裂 -->
```

### 3.3 关键部位坐标表(直接抄)

#### 男职场剪影(OpenClipart 321053,viewBox 708.66 × 1066.11)⭐ 主用

姿势:背对正面 + 西装 + 提公文包 + 向前走。带肤色细节(头+手 #f2b383)。

| 部位 | (cx, cy) | 高亮形状建议 |
|---|---|---|
| 头 | (370, 170) | circle r=105 |
| 嘴喉 | (370, 250) | ellipse rx=50 ry=20 |
| 心 / 胸 | (380, 430) | ellipse rx=135 ry=100 |
| 右肩 | (480, 350) | ellipse rx=60 ry=80 |
| 左手 | (290, 640) | circle r=60 |
| 右手 / 提包 | (460, 700) | circle r=60-65 |
| 双腿 | (370, 870) | ellipse rx=80 ry=130 |
| 双脚 | (370, 1020) | ellipse rx=100 ry=30 |

#### 女职场剪影(OpenClipart 310702,viewBox 2334.69 × 1638.97)⭐ 主用

姿势:半身 + 长发 + 双手摊开耸肩。横向 viewBox(注意!)。

| 部位 | (cx, cy) | 高亮形状建议 |
|---|---|---|
| 头 | (1150, 320) | circle r=280 |
| 眼睛(双) | (1100, 290) / (1200, 290) | circle r=30 |
| 耳朵(双,头侧) | (990, 340) / (1310, 340) | circle r=32 |
| 心 / 胸 | (1150, 850) | circle r=100 |
| 左手(摊开) | (450, 700) | circle r=100 |
| 右手(摊开) | (1900, 700) | circle r=100 |
| 半身底 | (1150, 1500) | ellipse rx=160 ry=80 |

#### 通用剪影(Wikimedia,viewBox 210×297) - 旧版/备用

| 部位 | (cx, cy) | 高亮形状建议 |
|---|---|---|
| 头 | (105, 40) | circle r=35 |
| 心 / 胸 | (105, 115) | circle r=14 |
| 手(左右) | (55, 175) / (155, 175) | circle r=12 |
| 腿(左右) | (80, 240) / (130, 240) | ellipse rx=20 ry=40 |

#### 火柴人版(OpenMoji 72×72) — pictogram 用

| 部位 | (cx, cy) | 半径 |
|---|---|---|
| 头中心 | (35.4, 10.65) | ~3 |
| 眼睛(双) | (33, 10) / (37.8, 10) | 1.6 |
| 耳朵(双) | (31, 11) / (39.8, 11) | 1.4 |
| 嘴喉 | (35.4, 14.5) | rx=3 ry=1.6 |
| 心/胸 | (35.4, 25) | ~5 |
| 手 | (26.5, 38) / (44.3, 38) | ~3.5 |
| 脚 | (33.4, 62) / (37.4, 62) | ~3.5 |

每个部位画一个透明圆(`fill-opacity: 0.15-0.45`,实色 0.5-0.95),颜色对应该部位语义。

### 3.4 ⭐ 引线必须在 .hp-figure 外层 overlay,不能在剪影 SVG 内部(v4 教训)

**v3 把引线放在剪影 SVG 内部 → 引线只到 SVG 边缘就断了,标签和剪影之间留下空白**。
用户反馈:"线都没直到卡片上"。

**v4 改用 overlay 跨容器 SVG**:
- 在 `.hp-figure`(grid 容器,`position: relative`)内加一个 `position: absolute; inset: 0` 的引线 SVG
- viewBox 用 `0 0 1000 1000` + `preserveAspectRatio="none"` 拉伸贴合 figure 整体
- `vector-effect="non-scaling-stroke"` 让虚线宽度独立于拉伸不变形
- 引线坐标用百分比思维(0-1000):**x≈280 是左卡片右边缘,x≈720 是右卡片左边缘,x≈500 是剪影中线**

```html
<div class="hp-figure">  <!-- position: relative; display: grid -->
  <!-- 标签卡 5 个,grid 自动定位到 4 角 + 中左 -->
  <div class="hp-tag hp-tag-tl">...</div>
  ...

  <!-- ① Overlay 引线 SVG(覆盖整个 figure,跨容器连接卡 ↔ 剪影) -->
  <svg class="hp-leaders" viewBox="0 0 1000 1000" preserveAspectRatio="none">
    <g fill="none" stroke-linecap="round">
      <line x1="280" y1="180" x2="490" y2="180"
            stroke="#3b82f6" stroke-width="2" stroke-dasharray="6,5"
            opacity="0.75" vector-effect="non-scaling-stroke"/>
      ...
    </g>
  </svg>

  <!-- ② 中央剪影 SVG(只放剪影本体) -->
  <svg class="hp-svg silhouette-host" data-kind="man">
    <!-- 剪影由 injectSilhouette() 注入 -->
  </svg>
</div>
```

```css
.hp-figure { position: relative; ... }
.hp-leaders { position: absolute; inset: 0; pointer-events: none; z-index: 1; }
.hp-svg { position: relative; z-index: 2; }   /* 让剪影盖在引线上层 */
```

**色彩呼应规则:** 引线颜色 = 对应标签卡片的 `border-left-color`。

**起点坐标速查表**(基于 grid-template-columns: 1fr 340px 1fr):
- 左 3 标签 → 引线起点 `x≈280`
- 右 3 标签 → 引线起点 `x≈720`
- 终点 ≈ `x=490-510`(剪影中线附近,贴住身体)
- y 用每个标签的垂直中心:1/6 (180) · 1/2 (500) · 5/6 (820)

**为什么不放剪影 SVG 内?** 剪影 SVG 的 viewBox 是 708×1066(男)或 2334×1638(女),只占 figure 中央列。引线超出 SVG 边界就被 viewBox 裁掉,无法到达标签卡。Overlay 用 figure 的百分比坐标 → 引线可自由穿越整个 figure 区域。

### 3.5 标签布局:3×3 grid 让标签错落

```css
.hp-figure {
  display: grid;
  grid-template-columns: 1fr 340px 1fr;  /* 左标签 / SVG / 右标签 */
  grid-template-rows: 1fr 1fr 1fr;        /* 3 行错落 */
}
.hp-svg { grid-column: 2; grid-row: 1 / 4; }  /* SVG 占中列 3 行 */
.hp-tag-tl { grid-column: 1; grid-row: 1; justify-self: end; }  /* 左上贴 SVG */
.hp-tag-ml { grid-column: 1; grid-row: 2; justify-self: end; }  /* 左中 */
.hp-tag-bl { grid-column: 1; grid-row: 3; justify-self: end; }  /* 左下 */
.hp-tag-tr { grid-column: 3; grid-row: 1; justify-self: start; }
.hp-tag-br { grid-column: 3; grid-row: 3; justify-self: start; }
```

**为什么 5 个标签 = 左 3 + 右 2 而非左 2 + 右 3?** 阅读顺序从左到右,主标签放左侧(头/动机/地域),次标签放右侧(场景/设备)。

### 3.6 引线(可选,锦上添花)

```svg
<g stroke="var(--accent)" stroke-width="0.35" stroke-dasharray="1.2,1.2" opacity="0.45">
  <path d="M 6 11 Q 22 11 33 11" />   <!-- 左侧引线到头部 -->
</g>
```

注意 `stroke-width: 0.35` 是因为 viewBox 是 72 小单位,如果 viewBox 是 200 单位则改 1。

## 四、数据规范

每个标签卡片:

```json
{
  "num": "01",
  "title": "职业 · 知识工作者",
  "big": "68%",
  "meta": "软件 / 咨询 / 金融 / 教育 / 研究",
  "color": "blue"   // blue/green/orange/purple/pink 对应 5 个标签色
}
```

底部一句话总结:**让读者带走核心判断,含 1-3 个加粗关键数字**。

## 五、踩坑黑名单

1. **绝不自己手画 SVG 人体** → 见 [`svg-aesthetics.md`] 第三节,直接抄 OpenMoji
2. **绝不用 viewBox 200×340 + transform scale** → 高亮永远对不齐;用 OpenMoji 原 72×N 坐标系
3. **绝不让高亮盖住人体** → 高亮放 SVG 前部(z 序在底),人体放后部
4. **绝不超过 6 个标签** → 视觉过载;5 个标签是最舒服的(左 3 右 2 或左 2 右 3)
5. **绝不让标签宽度变窄** → max-width: 280-320px,内容才能完整展示;太窄文字换行多
6. **绝不忽略底部一句话总结** → 人体图本身没有结论,需要文字总结告诉读者"所以呢"
7. **变体 2 团队 pictogram 时:小人 max-width 至少 32-36px** → 否则缩成米粒看不清

## 六、配套自检

- [ ] 5 个标签卡片左右分布合理(不挤在一边)
- [ ] 部位高亮和身体对位准确(头亮在头上,不是飘在空中)
- [ ] SVG 居中,左右标签都贴近 SVG 边缘(不漂到角落)
- [ ] 引线(若有)从标签连到对应部位,虚线柔和不抢戏
- [ ] 底部一句话总结含 1-3 个加粗数字
- [ ] 截图缩小到 30% 仍能识别人体形状(剪影测试)

---

> 配套模板:`assets/slides-templates/human-portrait.html`
> 前置 skill:`references/svg-aesthetics.md`(SVG 美学 + OpenMoji 抓取)
> 参考实现:`~/personal/openai-ipo-deck/src/slides/slide-{11,12,13,14}.html`(4 种变体)
