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

## 二、4 种变体(按 OpenAI deck 实现的)

| # | 变体 | 关键 SVG 处理 | 参考实现 |
|---|---|---|---|
| 1 | **用户画像** — 中央 1 人 + 5 标签四角分布 + 引线连接 | OpenMoji 1F9CD + 5 部位高亮圆 + dashed path 引线 | `openai-ipo-deck/slide-11` |
| 2 | **团队 pictogram** — N 个 100×100 人 排成网格 | JS 动态生成 OpenMoji 小人,按团队着色 | `openai-ipo-deck/slide-12` |
| 3 | **能力拟人** — 1 人 + 部位高亮 + 左右各 3 个能力卡片 | OpenMoji + 头/眼/耳/心/手/腿 6 部位高亮 | `openai-ipo-deck/slide-13` |
| 4 | **风险热图** — 1 人 + 部位按颜色深浅 + 左右职业卡 | OpenMoji + 红/黄/绿渐变高亮 + 底部色阶 | `openai-ipo-deck/slide-14` |

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

### 3.3 OpenMoji 人体关键点坐标(直接抄)

```
头中心   (35.4, 10.65)  半径 ~3
眼睛     (33, 10) / (37.8, 10)   半径 1.6
耳朵     (31, 11) / (39.8, 11)   半径 1.4
嘴/喉    (35.4, 14.5)  椭圆 rx=3 ry=1.6
胸/心    (35.4, 25)    半径 ~5
手       (26.5, 38) / (44.3, 38)  半径 ~3.5
脚       (33.4, 62) / (37.4, 62)  半径 ~3.5
```

每个部位画一个透明圆(`fill-opacity: 0.15-0.35`),颜色对应该部位语义。

### 3.4 部位高亮 z 序:必须在人体下面

```svg
<svg>
  <g class="highlights">...透明圆...</g>   <!-- 先画,在底 -->
  <circle cx="35.4" cy="10.65" r="2.969" .../>  <!-- 头 -->
  <path .../>                              <!-- 身体 -->
</svg>
```

否则透明高亮盖住人体描边,看起来像"皮肤"而不是"光环"。

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
