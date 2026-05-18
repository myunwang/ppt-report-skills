"""
将 src/ 下的拆分文件合并成最终 HTML。

修改任意一页只需要编辑：
  - src/slides/slide-N.html   (HTML 片段)
  - src/scripts/slide-N.js    (该页图表初始化逻辑)
  - src/styles/slide-N.css    (该页特殊样式，可空)
  - src/data/slide-N.{xlsx,csv,json}  (该页数据，可选；存在则注入为 window.__DATA_N__)

数据文件支持三种格式（优先级 .json > .xlsx > .csv）：
  - .xlsx  推荐日常用 — 每个 sheet → JSON 顶层一个 key
  - .csv   单表数据 — 整份 → JSON 顶层一个 array
  - .json  原生格式 — 直接读取（机器生成 / 复杂结构时用）

详见 xlsx2json.py 顶部的转换约定。

然后运行 `python3 build.py` 即可。

通用样式/逻辑放在 src/styles/common.css、src/scripts/common.js。
配置项见文件顶部的 CONFIG。
"""
from pathlib import Path
import json
import re
import sys

# 同目录的 xlsx2json 提供 Excel / CSV 读取能力
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
try:
    import xlsx2json
except ImportError:
    xlsx2json = None

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'src'

# ── CONFIG ────────────────────────────────────────────────
TITLE = '推荐系统分层架构'
OUT_NAME = 'recsys-architecture.html'
# 自动检测 slides 数量；也可手动指定
NUM_SLIDES = None  # None = auto detect
# 构建产物输出目录（相对项目根）。源文件始终在 src/，产物单独归到此处，
# 便于用户管理「一个 PPT 用到的所有东西」：src/ 是料，dist/ 是成品。
OUT_DIR = 'dist'
# ──────────────────────────────────────────────────────────

OUT = ROOT / OUT_DIR / OUT_NAME


def read(p: Path) -> str:
    return p.read_text(encoding='utf-8') if p.exists() else ''


def _load_slide_data(data_dir: Path, n: int):
    """查找 slide-N.{json,xlsx,csv} 并返回 (obj, source_filename) 或 (None, None)。

    优先级：.json > .xlsx > .csv
    """
    if not data_dir.exists():
        return None, None
    candidates = [
        ('.json', data_dir / f'slide-{n}.json'),
        ('.xlsx', data_dir / f'slide-{n}.xlsx'),
        ('.csv',  data_dir / f'slide-{n}.csv'),
    ]
    for ext, path in candidates:
        if not path.exists():
            continue
        try:
            if ext == '.json':
                obj = json.loads(path.read_text(encoding='utf-8'))
            elif ext == '.xlsx':
                if xlsx2json is None:
                    print(f'⚠ {path.name} 需要 xlsx2json.py（同目录）+ openpyxl')
                    continue
                obj = xlsx2json.xlsx_to_dict(path)
            elif ext == '.csv':
                if xlsx2json is None:
                    print(f'⚠ {path.name} 需要 xlsx2json.py（同目录）')
                    continue
                obj = xlsx2json.csv_to_list(path)
            else:
                continue
            return obj, path.name
        except Exception as e:
            print(f'⚠ {path.name}: {e}')
    return None, None


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

    # ── 3. 拼装 DATA (xlsx/csv/json → window.__DATA_N__) ──
    # 同一 slide 编号下，优先级：.json > .xlsx > .csv
    data_dir = SRC / 'data'
    data_parts = []
    for i in range(1, n + 1):
        obj, src_name = _load_slide_data(data_dir, i)
        if obj is None:
            continue
        data_parts.append(
            f'window.__DATA_{i}__ = {json.dumps(obj, ensure_ascii=False)};  // <- {src_name}'
        )
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
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(final, encoding='utf-8')
    print(f'✓ Built: {OUT.relative_to(ROOT)}  ({len(final):,} chars, {final.count(chr(10)) + 1} lines, {n} slides)')


if __name__ == '__main__':
    main()
