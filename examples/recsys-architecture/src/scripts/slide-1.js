// 全页 chip 统一同宽：所有 .lc-body 的 chip 取同一个宽（全页最宽，
// 但不超过最窄那一列的可用宽，保证不溢出）；.ls-body 嵌套小格因尺度更小，
// 单独取一组统一宽。字号是 CSS 固定 15px，这里【只统一宽度，绝不碰字号】。
function initSlide1() {
  const root = document.getElementById('s1');
  if (!root) return;

  // 动态列数：chip 数 ≤ 3 且卡片本身较窄（--span < 4）→ 单列；其他保持 2 列。
  // 解决"3 chip 在窄卡里 2 列布局第二列空挂"的问题。
  function setColumns() {
    root.querySelectorAll('.lc-body').forEach((body) => {
      const chips = body.querySelectorAll(':scope > .lm-item').length;
      if (!chips) return;
      const col = body.closest('.lm-col');
      const span = parseInt((col && col.style.getPropertyValue('--span')) || '3', 10);
      const cols = (chips <= 3 && span < 4) ? 1 : 2;
      body.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
    });
  }
  setColumns();

  function equalize(sel) {
    const boxes = [...root.querySelectorAll(sel)];
    const allChips = [];
    let minColCap = Infinity;
    boxes.forEach((box) => {
      const chips = [...box.querySelectorAll(':scope > .lm-item')];
      if (!chips.length) return;
      chips.forEach((c) => { c.style.width = 'auto'; });   // 先复位量自然宽
      allChips.push(...chips);
      minColCap = Math.min(minColCap, box.clientWidth);     // 最窄列的安全上限
    });
    if (!allChips.length) return;
    // 全页最宽 chip 的自然宽
    let maxW = 0;
    allChips.forEach((c) => { maxW = Math.max(maxW, c.getBoundingClientRect().width); });
    // 统一宽 = 全页最宽，但不超过最窄列可用宽（否则窄列会溢出）
    const w = Math.min(maxW, minColCap);
    allChips.forEach((c) => { c.style.width = w.toFixed(1) + 'px'; });
  }

  equalize('.lc-body');   // 主层：全页统一一个宽
  equalize('.ls-body');   // 嵌套小格：单独统一一个宽（尺度更小）

  let raf;
  window.addEventListener('resize', () => {
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(() => initSlide1());
  });
}
