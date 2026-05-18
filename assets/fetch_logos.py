"""
fetch_logos.py — 扫描所有 slide-*.html 里的 data-d="域名"，
从公开服务下载公司 logo 保存到本项目本地 src/assets/logos/，离线可用。

为什么要本地化：
  - logo 跟着 PPT 项目走（和 src/data/ 一样，每个项目独立、互不污染）。
  - 下载一次后离线 / 导出 PDF 都不依赖网络，不会出现空白图标。

用法（在 PPT 项目根目录运行；需联网，仅需跑一次，或新增公司后再跑）：

    python3 fetch_logos.py

可选参数：
    python3 fetch_logos.py --force      # 已存在也重新下载
    python3 fetch_logos.py --dir src    # 指定 src 目录（默认 ./src）

输出：
    src/assets/logos/<域名>.png         # 每个域名一个文件（域名里的 . 转 _）
    src/assets/logos/_manifest.json     # 域名 → 本地文件 / 失败记录

下载不到的域名不会报错中断；HTML 里的 onerror 回退到首字母色块，
所以即使个别 logo 拉不到，页面也不会崩。
"""
from __future__ import annotations
import argparse
import json
import re
import ssl
import sys
import urllib.request
from pathlib import Path

# 与 landscape-map 模板 slide JS 用同样的两个可靠源（这里是离线缓存版）。
# 只用 Clearbit + Google favicon：查不到会干净 404，不返回占位垃圾图。
SOURCES = [
    "https://logo.clearbit.com/{d}?size=128",
    "https://www.google.com/s2/favicons?domain={d}&sz=128",
]

UA = "Mozilla/5.0 (compatible; ppt-report-generator logo fetcher)"
MIN_BYTES = 100  # 小于此字节数视为无效（占位 1x1 / 空响应）


def domains_from_slides(src: Path) -> list[str]:
    """扫描 src/slides/*.html 里所有 data-d="..." 的去重域名。"""
    slides = src / "slides"
    if not slides.exists():
        print(f"⚠ 未找到 {slides}", file=sys.stderr)
        return []
    seen: dict[str, None] = {}
    for f in sorted(slides.glob("slide-*.html")):
        for m in re.finditer(r'data-d="([^"]+)"', f.read_text(encoding="utf-8")):
            d = m.group(1).strip()
            if d:
                seen.setdefault(d, None)
    return list(seen)


def fetch(url: str) -> bytes | None:
    ctx = ssl.create_default_context()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            if r.status != 200:
                return None
            data = r.read()
            ctype = (r.headers.get("Content-Type") or "").lower()
            if len(data) < MIN_BYTES or "image" not in ctype and not data[:4] in (
                b"\x89PNG", b"\x00\x00\x01\x00", b"GIF8",
            ):
                return None
            return data
    except Exception:
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="src", help="src 目录（默认 ./src）")
    ap.add_argument("--force", action="store_true", help="已存在也重新下载")
    args = ap.parse_args()

    src = Path(args.dir).resolve()
    logos = src / "assets" / "logos"
    logos.mkdir(parents=True, exist_ok=True)

    domains = domains_from_slides(src)
    if not domains:
        print("没有发现任何 data-d 域名，无需下载。")
        return

    manifest: dict[str, str] = {}
    ok = fail = skip = 0
    for d in domains:
        safe = d.replace(".", "_") + ".png"
        out = logos / safe
        if out.exists() and not args.force:
            manifest[d] = f"assets/logos/{safe}"
            skip += 1
            continue
        data = None
        for tpl in SOURCES:
            data = fetch(tpl.format(d=d))
            if data:
                break
        if data:
            out.write_bytes(data)
            manifest[d] = f"assets/logos/{safe}"
            ok += 1
            print(f"  ✓ {d}  ({len(data):,}B)")
        else:
            manifest[d] = ""  # 空 = 下载失败，HTML 回退首字母色块
            fail += 1
            print(f"  ✗ {d}  (所有源都失败，将用首字母色块回退)")

    (logos / "_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        f"\n完成：{ok} 下载 / {skip} 已存在 / {fail} 失败 → {logos.relative_to(src.parent)}"
    )
    if fail:
        print("失败的域名会用首字母色块占位，页面不会崩；可改 data-d 后重试。")


if __name__ == "__main__":
    main()
