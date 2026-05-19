// 同块等宽：每个卡片内所有 chip 宽度 = 该块最宽 chip 的宽。
// 字号是 CSS 固定 15px，这里【只统一宽度，绝不碰字号】——不截断的根基不动。
function initSlide1() {
  const root = document.getElementById('s1');
  if (!root) return;

  function equalize(sel) {
    root.querySelectorAll(sel).forEach((box) => {
      const chips = [...box.querySelectorAll(':scope > .lm-item')];
      if (chips.length < 2) return;
      // 先清掉可能的旧固定宽，量自然宽
      chips.forEach((c) => { c.style.width = 'auto'; });
      let maxW = 0;
      chips.forEach((c) => { maxW = Math.max(maxW, c.getBoundingClientRect().width); });
      // 同块统一为最宽值（不超过该列可用宽，避免溢出）
      const colCap = box.clientWidth;            // 单格容器宽，安全上限
      const w = Math.min(maxW, colCap);
      chips.forEach((c) => { c.style.width = w.toFixed(1) + 'px'; });
    });
  }

  equalize('.lc-body');
  equalize('.ls-body');

  let raf;
  window.addEventListener('resize', () => {
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(() => initSlide1());
  });
}
