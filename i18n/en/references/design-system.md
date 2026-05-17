# Design System: Hard Rules for Information Hierarchy

**Core principle**: every piece of text must be able to answer "what level am I". When readers scan a slide, they should be able to work out the hierarchy from font size / font weight / color alone.

## 8-Level Text Hierarchy

| Level | Use | CSS Variable | Default | Font Weight | Color |
|---|---|---|---|---|---|
| L0 | top small label ("Monthly Overview") | `--fs-label` | 13px | 600 | `var(--accent2)` uppercase + letter-spacing 0.18em |
| L1 | slide main title | `--fs-title` | 36px | 800 | `var(--text)` |
| L2 | subtitle / one-sentence conclusion (includes key numbers) | `--fs-subtitle` | 18px | 500 | `var(--text2)`, key numbers `<strong>` `var(--accent)` |
| L3 | section/column title | `--fs-h2` | 18px | 700 | `var(--text)` |
| L4 | card title, metric big number | `--fs-h3` | 15px | 600 | `var(--text)` |
| L5 | body text, metric name | `--fs-body` | 13px | 400-500 | `var(--text2)` |
| L6 | meta info, notes, card-conclusion | `--fs-caption` | 12px | 400 | `var(--text3)` |
| L7 | auxiliary small text, tag, chart footnote | `--fs-mini` | 11px | 400-600 | `var(--text3)` |

> Font sizes are in the 1600×900 design-canvas coordinate system. The whole slide scales with the window, **do not scale font size separately**.

## Color Scheme (Semantics Before Aesthetics)

Theme variables use the unified prefixes `--accent*` and `--text*`. **All slides and components use variables**, making it easy to switch themes.

| Variable | Default | Meaning |
|---|---|---|
| `--bg` | `#f4f6fb` | full-slide background |
| `--surface` | `#ffffff` | card/panel base color |
| `--surface2` | `#f1f4fa` | nested cards/input boxes and other secondary surfaces |
| `--border` | `rgba(15,23,42,0.08)` | stroke |
| `--accent` | `#2563eb` | primary brand color (blue) — title highlight, buttons, key numbers |
| `--accent2` | `#0891b2` | secondary color (cyan) — secondary emphasis |
| `--accent3` | `#059669` | positive / up / completed (green) |
| `--warn` | `#d97706` | caution / neutral-leaning-weak (orange) |
| `--danger` | `#dc2626` | risk / down (red) |
| `--text` | `#0f172a` | primary text |
| `--text2` | `#475569` | secondary text |
| `--text3` | `#94a3b8` | de-emphasized text |

## Increase/Decrease Semantic Colors (Mandatory Rule)

The thing most often abused in data reports is color. **Convention**:

- **Green (`--accent3`)** = positive change / completed / treatment group outperforms control group (**note**: this is the opposite of the `data-report` skill's "green = down" convention; this skill uses "green = positive", because in business a KPI going up is usually a good thing)
- **Red (`--danger`)** = negative change / failure / risk
- **Orange (`--warn`)** = neutral / below expectations / needs attention but not P0

In JSX/HTML, inside conclusion text:

```html
<span class="pos">+30.5%</span>     <!-- green, positive -->
<span class="neg">-2.7%</span>      <!-- red, negative -->
<span class="warn">only 2.8%</span> <!-- orange, needs attention -->
<strong>key number</strong>         <!-- blue, primary brand color highlight -->
```

## Spacing System (Multiples of 4)

Use only the following spacing values (px, 1600×900 design canvas):

| token | px | Use |
|---|---|---|
| xs | 4 | extremely tight inline elements on the same row |
| sm | 8 | tag / dot and label |
| md | 12 | line spacing inside a card |
| lg | 16 | section spacing, grid gap |
| xl | 20-24 | card padding |
| 2xl | 32-40 | top whitespace, large section spacing |
| 3xl | 48-64 | slide outer margin (slide padding defaults to 48 64) |

```css
.slide { padding: 48px 64px; }      /* top 48 / left-right 64 */
.kpi-grid { gap: 16px; }             /* lg */
.card { padding: 20px 24px; }        /* xl */
```

## Border Radius

- small elements (tag, dot wrapper): 4px
- cards: 10–12px
- large panels: 16px
- fully rounded / pill: 100px

## Shadows (Soft)

```css
--shadow-card:    0 1px 3px rgba(15,23,42,0.04), 0 1px 2px rgba(15,23,42,0.03);
--shadow-card-lg: 0 4px 12px rgba(15,23,42,0.06), 0 2px 4px rgba(15,23,42,0.04);
```

Use shadows only in light themes. In dark themes, use `border` + `--surface2` to distinguish hierarchy.

## Mandatory Top Trio

Every slide **must** have:

```html
<div class="slide-label">Monthly Overview</div>   <!-- L0 label -->
<div class="slide-title">April Delivery Overview</div>   <!-- L1 title -->
<div class="slide-subtitle">
  <strong>All 5</strong> strategy requirements shipped ... — core monthly delivery complete
</div>   <!-- L2 one-sentence conclusion, must include key numbers -->
```

`slide-subtitle` is the "central conclusion" of this slide. The reader can know the slide's main point by **reading the subtitle only**.

## Font Weight Reference

Font weight is not decoration, it is hierarchy. **Do not use more than 4 font weights on the same slide**:

- 900 → big numbers (KPI, col-num style)
- 700-800 → large titles, column headers, emphasis
- 600 → card titles, tag, status
- 400-500 → body text, metric names

## Anti-patterns (Forbidden)

- ❌ Having 2 or more ad-hoc sizes outside the font-size system on the same slide (e.g. `font-size: 14px`, should use `var(--fs-body)`)
- ❌ Using italics for emphasis (Chinese does not work with it)
- ❌ Using underline for emphasis (looks like a hyperlink)
- ❌ Using `text-shadow` for decoration
- ❌ Red-green color-blind-unfriendly highly saturated primary colors (`#ff0000`, `#00ff00`)
- ❌ Not using a monospace font for numbers (causes jitter) — numbers must use `font-family: var(--mono)`
