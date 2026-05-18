/* ══════════════════════════════════════════════════════════
   THEME SWITCHER — 5 套预设主题切换
   切主题后会自动用 reinitAllCharts() 重渲染所有 ECharts 实例
══════════════════════════════════════════════════════════ */

const THEMES = [
  { key: 'modern-light',   label: 'Light' },
  { key: 'dark-tech',      label: 'Dark' },
  { key: 'warm-business',  label: 'Warm' },
  { key: 'brand-blue',     label: 'Brand' },
  { key: 'minimal-mono',   label: 'Mono' },
];

function applyTheme(name) {
  document.body.setAttribute('data-theme', name);
  try { localStorage.setItem('report-theme', name); } catch (e) {}
  // 更新 switcher 按钮状态
  document.querySelectorAll('#themeSwitcher button').forEach(b => {
    b.classList.toggle('active', b.dataset.themeBtn === name);
  });
  // 重渲染 ECharts
  if (typeof reinitAllCharts === 'function') reinitAllCharts();
}

function initThemeSwitcher() {
  const sw = document.getElementById('themeSwitcher');
  if (!sw) return;
  sw.innerHTML = THEMES.map(t =>
    `<button data-theme-btn="${t.key}" title="${t.key}">${t.label}</button>`
  ).join('');
  sw.addEventListener('click', e => {
    const t = e.target.dataset.themeBtn;
    if (t) applyTheme(t);
  });
  let saved = 'modern-light';
  try { saved = localStorage.getItem('report-theme') || 'modern-light'; } catch (e) {}
  applyTheme(saved);
}

window.addEventListener('DOMContentLoaded', initThemeSwitcher);
