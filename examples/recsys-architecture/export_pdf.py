"""
将合成的 HTML 导出为 PDF（13.33 × 7.5 inch，标准 16:9）。

依赖：
  pip install playwright img2pdf
  playwright install chromium

用法：
  python3 export_pdf.py [HTML_PATH] [OUT_PDF_PATH]
  默认根据 build.py 的 OUT_NAME 推断。
"""

import os
import sys
from playwright.sync_api import sync_playwright
import img2pdf

ROOT = os.path.dirname(os.path.abspath(__file__))

# 默认推断（可被命令行参数覆盖）
# 先找 dist/（build.py 的默认产物目录），回退项目根（兼容旧项目）
def find_html():
    for base in (os.path.join(ROOT, 'dist'), ROOT):
        if not os.path.isdir(base):
            continue
        for f in sorted(os.listdir(base)):
            if f.endswith('.html') and not f.startswith('.'):
                return os.path.join(base, f)
    raise SystemExit('No HTML found in dist/ or project root.')

HTML_PATH = sys.argv[1] if len(sys.argv) > 1 else find_html()
OUT_PDF = sys.argv[2] if len(sys.argv) > 2 else HTML_PATH.replace('.html', '.pdf')

W, H = 1600, 900
DSF = 2  # device_scale_factor — 截图分辨率倍数

OVERRIDE_CSS = """
:root { --fit: 1 !important; --nav-reserve: 0px !important; }
.nav, .theme-switcher { display: none !important; }
.stage { bottom: 0 !important; }
.canvas { transform: translate(-50%, -50%) scale(1) !important; }
"""

# 全局禁用 ECharts 动画，让 chart 一次性同步绘制
DISABLE_ANIM_JS = """
() => {
  // ECharts: 切动画 off 通过 setOption 时传 animation:false 解决，
  // 这里通过 dispose + re-init 后会重读 option，所以我们 patch 默认。
  if (window.echarts) {
    const origInit = echarts.init;
    echarts.init = function(...args) {
      const inst = origInit.apply(this, args);
      const origSetOption = inst.setOption.bind(inst);
      inst.setOption = (opt, ...rest) => origSetOption({ ...opt, animation: false }, ...rest);
      return inst;
    };
  }
  // Chart.js 兼容（如果项目还在用）
  if (window.Chart) {
    Chart.defaults.animation = false;
    Chart.defaults.animations = {};
    Object.values(Chart.instances || {}).forEach(c => c.destroy());
  }
}
"""

def main():
    if not os.path.exists(HTML_PATH):
        raise SystemExit(f'HTML not found: {HTML_PATH}')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={'width': W, 'height': H}, device_scale_factor=DSF)
        page = ctx.new_page()
        page.on('pageerror', lambda e: print('[pageerror]', e))
        page.goto('file://' + HTML_PATH)
        page.wait_for_load_state('networkidle')
        page.add_style_tag(content=OVERRIDE_CSS)
        page.evaluate(DISABLE_ANIM_JS)
        page.wait_for_timeout(300)

        # 自动检测 slide 数量
        n_slides = page.evaluate('() => document.querySelectorAll(".slide").length')
        if not n_slides:
            raise SystemExit('No .slide elements found.')

        png_paths = []
        for i in range(n_slides):
            page.evaluate(
                """(idx) => {
                    document.querySelectorAll('.slide').forEach((s, j) => {
                        s.classList.toggle('active', j === idx);
                    });
                    window.dispatchEvent(new Event('resize'));
                    if (typeof window['initSlide' + (idx + 1)] === 'function') {
                        try { window['initSlide' + (idx + 1)](); } catch (e) { console.error(e); }
                    }
                }""",
                i,
            )
            page.wait_for_timeout(500)  # 等 ECharts 完成同步绘制
            out = os.path.join(ROOT, f'_pdf_p{i+1}.png')
            page.screenshot(path=out, clip={'x': 0, 'y': 0, 'width': W, 'height': H})
            png_paths.append(out)
            print(f'  ✓ page {i+1}/{n_slides} captured')

        browser.close()

    layout = img2pdf.get_layout_fun(pagesize=(img2pdf.in_to_pt(13.333), img2pdf.in_to_pt(7.5)))
    with open(OUT_PDF, 'wb') as f:
        f.write(img2pdf.convert(png_paths, layout_fun=layout))

    if os.environ.get('KEEP_PNGS') != '1':
        for p in png_paths:
            try: os.remove(p)
            except OSError: pass

    size_kb = os.path.getsize(OUT_PDF) / 1024
    print(f'\n✓ PDF saved: {OUT_PDF}  ({size_kb:.0f} KB)')

if __name__ == '__main__':
    main()
