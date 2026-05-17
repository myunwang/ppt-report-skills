# Classic Layout Principles for Report Slides

The design system governs "how text is written and how colors are used"; this document governs "how things are arranged on a single slide."

## 0. Top-Level Mindset: One Story Per Slide

**One slide = one conclusion + supporting evidence**. The order in which the reader scans the slide should be:

1. Look at `slide-title` to grasp the **topic** (3 seconds)
2. Look at `slide-subtitle` to grasp the **conclusion** (5 seconds)
3. Look at the 1–3 pieces of evidence in the body to **confirm the conclusion** (15 seconds)
4. (Optional) Look at the footnote / card-conclusion to **dig into details**

If your reader can close the document and head into the meeting after the first two steps, this slide has won. **Each slide answers only one question**; if you can't write down the question, this slide shouldn't exist.

## 1. Pyramid Structure (Within Each Slide)

Each slide is an inverted pyramid:

```
┌─────────────────────────────────────┐
│ LABEL (small label)                  │  ← context anchor
│ TITLE topic (largest font size)      │  ← topic
│ SUBTITLE conclusion (medium size, with key numbers) │  ← conclusion ★★★
├─────────────────────────────────────┤
│                                     │
│      supporting evidence (chart / table / card)  │  ← evidence
│                                     │
├─────────────────────────────────────┤
│ FOOTER footnote / data source / notes (small)    │  ← metadata
└─────────────────────────────────────┘
```

**Proportion reference**: the title area takes up 15-20% of the slide height, the body 70-75%, and the footer ≤10%. In a 1600×900 design canvas this is ≈ title 150-180px / body 630-680px / footer not enforced.

## 2. F-Pattern / Z-Pattern Reading Path

The path the reader's eyes follow after entering the slide should be **guided by the layout** rather than left to chance:

- **F-pattern**: information-dense slides (multiple cards, multiple tables) — the gaze goes from top-left → scans across → moves down and scans across again. Put important information toward the left and top.
- **Z-pattern**: argument slides (few elements, with a conclusion) — the gaze goes from top-left → top-right → bottom-left → bottom-right. Put the CTA / key numbers at the bottom-right "landing point."

**Application**:
- In a row of N KPI cards, put the most important metric **furthest left**
- In a side-by-side comparison slide (A vs B), put **the side with the stronger conclusion on the left** (the reader sees the positive data first and is more willing to keep reading)
- Counterexample: putting the "Top 1 ranking" at the bottom-right and the "product iteration timeline" at the top-left → the gaze hits the secondary information first

## 3. Rule of Thirds

Divide the slide into thirds both horizontally and vertically, and **place key elements at the intersections**:

```
┌────┬────┬────┐
│    │  ●│    │
├────┼────┼────┤
│    │    │    │  ●
├────┼────┼────┤
│●   │    │    │
└────┴────┴────┘
```

KPI big numbers, the main element of the hero image, and the main subject of a face / screenshot should be placed at the intersections. **Don't center a single chart so it fills the whole slide**; leave a sense of air.

## 4. Grid — The Implicit Grid of 1600×900

The implicit grid of this system:

- **Horizontal**: 12 columns, 16px gutter, column width ≈ 117px
- **Vertical**: 8 rows, 16px gutter, row height ≈ 100px
- **slide padding**: 48px top / 64px left and right

**The width and height of every element are some number of columns out of the 12 columns**. `.kpi-grid` = 4×3 columns / `.two-col` = 6+6 columns / `.three-col` = 4+4+4 columns / `.phase-layout` = 3+5+4 columns.

**Never "eyeball alignment."** Either use a grid, or use flex `gap`; don't use `position: absolute` + `left: 327px`.

## 5. Negative Space

Whitespace is not waste; it is a **hierarchy tool**. Rules:

- Elements in the same group → small spacing (8-12px)
- Elements in different groups → medium spacing (16-24px)
- Different sections → large spacing (32-48px)

**80% of "the slides look messy" problems are rooted in spacing without hierarchy** — every gap is 8px, or every gap is 32px.

## 6. Visual Anchor

Each slide should have **one** most prominent element that grabs the eye:

- Overview slide → "5" 64px big number (col-num)
- Data slide → KPI big number (36px, 900 weight)
- Trend slide → the multi-color line chart itself
- Story slide → one bold conclusion sentence

**There can be only one anchor.** If two things both shout "look at me," nobody looks at either. Secondary elements must be downgraded (color `--text2` instead of `--text`, weight 500 instead of 700).

## 7. Alignment

- **Vertical alignment**: primarily left-aligned, with numbers right-aligned (monospace font)
- **Horizontal alignment**: pick one of baseline alignment / top alignment / center-line alignment, and **don't mix them**
- **Number alignment**: `metric-after` always right-aligned + `font-family: var(--font-mono)`
- Counterexample: the title is 800 weight 36px, and the subtitle below it is indented 4px to the left (the eye will notice "it shifted a bit")

## 7b. Card Boundary Alignment (One of the Most Important Engineering Rules)

**When a slide uses multiple cards to partition the display area, the card boundaries must be strictly aligned** — cards in the same row have consistent top/bottom edges, and cards in the same column have consistent left/right edges. This is the dividing line between a professional feel and a chaotic feel.

### Three Hard Rules

1. **Cards in the same row have the same height**: the left card has 8 rows of metric, the right card has 6 rows of metric — **the bottom edges must be flush** — compensate for the difference by stretching the child elements, don't let the card itself grow taller or shorter.
2. **Cards in the same column have the same width**: use grid `1fr 1fr` or `repeat(N, 1fr)`; don't use `auto` / don't size to content.
3. **Internal whitespace within cards is aligned**: all cards use the same `padding`, and the baseline of the first internal row (title / metric / chart-header) lines up in the horizontal direction.

### Implementation Patterns

**A. N cards in the same row at the same height**

```css
.country-row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px;
               flex: 1; min-height: 0; }   /* parent container needs flex:1 + min-height:0 */
.country-row > .card { display: flex; flex-direction: column;
                       height: 100%; margin: 0; min-height: 0; overflow: hidden; }
```

Key point: `grid-template-columns: 1fr 1fr` makes the widths strictly equal; the parent container's `align-items` defaults to `stretch` → child cards automatically become the same height.

**B. N rows of metric within a card share the height equally (filling to the bottom)**

```css
.country-row > .card > .metric-row { flex: 1 1 0; min-height: 0;
                                     padding: 0; border-bottom: 1px solid var(--border); }
.country-row > .card > .metric-row:last-child { border-bottom: none; }
```

Key point: `flex: 1 1 0` makes each row share the remaining height equally. **When the left card has 8 rows / the right card has 6 rows, each row has a different height but the bottom edges align.**

**C. Use "elastic spacers" to compensate for heterogeneous content (phase-arrow pattern)**

The left side has 3 phase-boxes (with varying amounts of content), the right side has 2 equal-height chart-cards — stretching directly would blow the phase-boxes up to an oversized height. Solution:

```css
.phase-timeline-v { display: flex; flex-direction: column;
                    min-height: 0; overflow: hidden; }
.phase-timeline-v .phase-box   { flex: 0 0 auto; height: auto; }  /* natural height */
.phase-timeline-v .phase-arrow-v { flex: 1 1 0; }                  /* spacer that stretches */
```

`phase-arrow-v` is the ↓ arrow between phase-boxes — letting the arrow absorb the remaining space makes **the bottom edge of the last phase-box** align with the bottom edge of the chart-card on the right.

### `min-height: 0` — The Lifeline of Fill-to-Container flex/grid Layouts

flex/grid children default to `min-height: auto`, which means "I am as big as my content." When the parent container wants it to be "only 100% in height," and the child's content overflows → it blows out the parent container. **For every container with `flex: 1` or `align-items: stretch`, the children must explicitly write `min-height: 0`** (or `min-width: 0` for horizontal fill).

```css
.parent  { display: flex; flex-direction: column; height: 600px; }
.child   { flex: 1; min-height: 0; overflow: hidden; }   /* ← omit it and it overflows */
```

90% of "why don't my card bottom edges align / why is the chart mysteriously taller / why did a scrollbar appear" problems are rooted in not writing this line.

### Alignment Self-Check (After Writing the CSS)

- [ ] Do the bottom edges of cards in the same row form a single straight line? (Use the browser dev tools to drag a horizontal line onto them)
- [ ] Do the left/right edges of cards in the same column form a single straight line?
- [ ] Do the "title" baselines within the cards line up in the horizontal direction?
- [ ] Drag-resize the window — is the alignment still there? (If it breaks at some size, it's probably a missing `min-height:0`)
- [ ] If you temporarily change content length (e.g., delete a row from some metric-row), are the other cards' bottom edges still flush?

### Anti-Patterns

- ❌ Hard-coding card height with `height: 380px` — it will break with window resizing or content changes
- ❌ Using `margin-top: 12px` to "forcibly push the short card down" into alignment — it misaligns again as soon as the content changes
- ❌ Using `display: inline-block` + `vertical-align: top` for the same row — it only aligns the top edge, and the bottom edge is always ragged
- ❌ Card internal padding being 16px for one and 20px for another — visually "just a hair off"
- ❌ Omitting `min-height: 0` → content makes one card taller → the whole row gets stretched taller → other slides' bottom edges look flush but this one doesn't

## 8. Contrast

Four contrast dimensions:

| Contrast type | Implementation | Purpose |
|---|---|---|
| **Size contrast** | KPI 36px vs label 13px | Primary/secondary |
| **Weight contrast** | Title 800 vs body 400 | Primary/secondary |
| **Light/dark contrast** | text 0f172a vs text3 94a3b8 | Primary/secondary |
| **Color contrast** | Key number accent blue vs body text2 gray | Focus |

**Use at least 2 kinds of contrast** to make the hierarchy clear. Using only size contrast → monotonous; using only color contrast → can't tell primary from secondary.

## 9. Repetition

Visual consistency = a professional feel. Elements of the same kind **must repeat their structure**:

- All chart-card headers are a "title + footnote" pair, with the footnote always on the right
- All country-cards have a "country name + tag" header + N metric-rows
- All phase-boxes have "PHASE NN · date" + title + bullet items

**Repetition creates a reading rhythm.** The second time the reader sees a card with the same structure, they don't need to re-parse the layout and can go straight to the content.

## 10. Information Density

**6-9 elements per slide is optimal.** Fewer than 4 → too much whitespace, looks empty; more than 12 → information overload.

Empirical values:

| Slide type | Number of body elements | Composition example |
|---|---|---|
| Overview slide | 8-10 | 3 sections × 2-5 cards |
| KPI + side-by-side comparison | 4 KPI + 2 cards = 6 | Top metric row + side-by-side comparison table |
| Three phases + multiple charts | 3 phase + 4 chart = 7 | Phase timeline + multiple chart-cards |
| Multi-object trend | 4 chart = 4 | Multi-object facet |
| Categories + trend | 4 mini-bar + 1 chart + 1 insight = 6 | Category ranking + overall trend + explanation box |

**More than 12 = split into two slides.** Don't cram.

## 11. Story Curve (Across Slides)

The whole deck should have rhythm; don't make all 6 slides the same density:

```
Climax: multi-object trend summary ━━━━━╲
                            ╲
Medium: side-by-side comparison ━━━━━━━━━━━━━━━╲━━━ ←—— information density
                              ╲
Low (breathing): cover / overview ━━━━━━━━╲
                                ╲
                  ↓ time
```

Classic rhythm:

1. **Overview** (low density, establish the framework)
2. **Key point 1 / 2 / 3** (high density, detailed data)
3. **Trend summary** (medium density, coherent story)
4. **Future plans / risks** (low density, breathing + closing)

**Two equally high-density slides in a row** → reader fatigue. Insert one low-density slide in between (a one-sentence slide / big-number slide / full-image slide).

## 12. The 8 Unspoken Rules of Data Charts

1. **Weaken axis lines**: use 0.10 alpha for `axisLine`, not pure black
2. **Keep only the y-axis gridlines**: the x-axis gridlines are 99% noise
3. **Put the legend at the bottom**, not left or right — it squeezes the plotting area
4. **legend / tooltip font size ≤ 11px**, leave space for the chart itself
5. **Line charts ≤ 5 lines**; beyond that use facets (split into multiple small charts)
6. **Bar chart gap between bars = 40% of the bar width** (`barCategoryGap: '40%'`)
7. **Use dashed vertical lines + small top labels for milestones**, don't draw them inside the chart
8. **Always annotate the data source / data extraction date** (chart-card-note or footer)

## 13. Anti-Layout Checklist

Fix these immediately:

- ❌ More than 12 KPI numbers on one slide (split the slide)
- ❌ Centered title, left-aligned body text (either center both or left-align both)
- ❌ Using `<br>` to control paragraph spacing (use margin)
- ❌ Letting a chart fill the entire slide with no title/footnote (wrap it in a chart-card)
- ❌ Key numbers in a smaller font size than the context (they should be larger, brighter, bolder)
- ❌ Body text blocks longer than 3 lines (split into bullets or a callout)
- ❌ Mixing more than 2 kinds of emoji flags + text emoji styles on one slide
- ❌ Footer that says "by Zhang San 2025-04-30" (this is git commit info, not slide info)
- ❌ Using gradient colors to decorate the background (the background must be a solid color or grid)
- ❌ Letting body text be smaller than 11px (illegible when projected)

## 14. Self-Check Checklist (Ask Yourself After Finishing a Slide)

- [ ] What is this slide's "one-sentence conclusion"? Did you write it in the subtitle?
- [ ] Are the key numbers bolded + color-highlighted?
- [ ] Which one is the visual anchor? (There should be only one)
- [ ] Projected 50 meters away, is the most important text legible?
- [ ] If you print the slide in black and white, is the hierarchy still there? (Distinguishing primary/secondary by color alone = failure)
- [ ] Would the slide be worse if you deleted one element? (If not, delete it)
- [ ] Is the data source annotated?
- [ ] Is the next slide equally high-density? Should you add a "breathing slide"?
