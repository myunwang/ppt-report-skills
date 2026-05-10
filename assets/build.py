"""
将 src/ 下的拆分文件合并成最终 HTML。

修改任意一页只需要编辑：
  - src/slides/slide-N.html   (HTML 片段)
  - src/scripts/slide-N.js    (该页图表初始化逻辑)
  - src/styles/slide-N.css    (该页特殊样式，可空)
  - src/data/slide-N.json     (该页数据，可选；存在则注入为 window.__DATA_N__)

然后运行 `python3 build.py` 即可。

通用样式/逻辑放在 src/styles/common.css、src/scripts/common.js。
配置项见文件顶部的 CONFIG。
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'src'

# ── CONFIG ────────────────────────────────────────────────
TITLE = '我的工作汇报'
OUT_NAME = '我的工作汇报.html'
# 自动检测 slides 数量；也可手动指定
NUM_SLIDES = None  # None = auto detect
# ──────────────────────────────────────────────────────────

OUT = ROOT / OUT_NAME


def read(p: Path) -> str:
    return p.read_text(encoding='utf-8') if p.exists() else ''


def detect_slides() -> int:
    if NUM_SLIDES is not None:
        return NUM_SLIDES
    slides_dir = SRC / 'slides'
    if not slides_dir.exists():
        return 0
    nums = []
    for f in slides_dir.glob('slide-*.html'):
        m = re.match(r'slide-(\d+)\.html', f.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums) if nums else 0


def main() -> None:
    n = detect_slides()
    if n == 0:
        raise SystemExit(f'No slides found in {SRC / "slides"}')

    # ── 1. 拼装 CSS ──
    style_parts = [read(SRC / 'styles' / 'common.css'),
                   read(SRC / 'styles' / 'components.css')]
    for i in range(1, n + 1):
        style_parts.append(read(SRC / 'styles' / f'slide-{i}.css'))
    styles = '\n'.join(s.strip() for s in style_parts if s.strip())

    # ── 2. 拼装 SLIDES (HTML 片段) ──
    slide_parts = []
    for i in range(1, n + 1):
        body = read(SRC / 'slides' / f'slide-{i}.html').rstrip('\n')
        if body:
            slide_parts.append(f'      <!-- ── SLIDE {i} ── -->\n{body}')
    slides_html = '\n\n'.join(slide_parts)

    # ── 3. 拼装 DATA (JSON → window.__DATA_N__) ──
    data_parts = []
    for i in range(1, n + 1):
        data_path = SRC / 'data' / f'slide-{i}.json'
        if data_path.exists():
            try:
                # 验证 JSON 合法
                obj = json.loads(data_path.read_text(encoding='utf-8'))
                data_parts.append(f'window.__DATA_{i}__ = {json.dumps(obj, ensure_ascii=False)};')
            except json.JSONDecodeError as e:
                print(f'⚠ slide-{i}.json invalid: {e}')
    data_block = '\n'.join(data_parts)

    # ── 4. 拼装 JS ──
    script_parts = [read(SRC / 'scripts' / 'common.js'),
                    read(SRC / 'scripts' / 'theme-switcher.js')]
    for i in range(1, n + 1):
        script_parts.append(read(SRC / 'scripts' / f'slide-{i}.js'))
    scripts = '\n\n'.join(s.strip() for s in script_parts if s.strip())

    # ── 5. 写入 shell ──
    shell = read(SRC / 'shell.html')
    final = (
        shell
        .replace('{{TITLE}}', TITLE)
        .replace('{{STYLES}}', styles)
        .replace('{{SLIDES}}', slides_html)
        .replace('{{DATA}}', data_block)
        .replace('{{SCRIPTS}}', scripts)
    )
    OUT.write_text(final, encoding='utf-8')
    print(f'✓ Built: {OUT.relative_to(ROOT)}  ({len(final):,} chars, {final.count(chr(10)) + 1} lines, {n} slides)')


if __name__ == '__main__':
    main()
