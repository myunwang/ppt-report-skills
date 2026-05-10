/* ══════════════════════════════════════════════════════════
   COMMON — 自适应 + 导航 + ECharts helper + 主题切换桥接
   修改任意一页内容时不需要动这个文件
══════════════════════════════════════════════════════════ */

// ── 自适应：把整张 1600×900 设计稿等比缩放到当前窗口（底部预留 nav 空间） ──
function fitCanvas() {
  const baseW = 1600, baseH = 900;
  const navReserve = 88;
  const w = window.innerWidth;
  const h = Math.max(0, window.innerHeight - navReserve);
  const scale = Math.min(w / baseW, h / baseH);
  document.documentElement.style.setProperty('--fit', scale.toFixed(4));
  // 通知所有 ECharts 实例 resize（chart 内部 width/height 不随 transform scale 变，
  // 但因为 chart 容器以 px 定，所以本质不需要 resize；保留以防 chart 容器尺寸真的变）
  if (window.__charts) {
    Object.values(window.__charts).forEach(c => { try { c.resize(); } catch (e) {} });
  }
}
window.addEventListener('resize', fitCanvas);
window.addEventListener('orientationchange', fitCanvas);
window.addEventListener('DOMContentLoaded', fitCanvas);

// ── ECharts 实例注册表（用于切主题时重渲染） ──
window.__charts = window.__charts || {};
window.__chartOptions = window.__chartOptions || {};

// ── Slide 切换 ──
let __slides = null;
let __dotsEl = null;
let __cur = 0;
let __total = 0;

function __initNav() {
  __slides = document.querySelectorAll('.slide');
  __total = __slides.length;
  __dotsEl = document.getElementById('dots');
  for (let i = 0; i < __total; i++) {
    const d = document.createElement('div');
    d.className = 'dot' + (i === 0 ? ' active' : '');
    d.onclick = () => goTo(i);
    __dotsEl.appendChild(d);
  }
  document.getElementById('counter').textContent = '1 / ' + __total;
  __slides.forEach(s => s.classList.remove('active'));
  if (__slides.length) __slides[0].classList.add('active');
  __cur = 0;
}

function goTo(n) {
  __slides[__cur].classList.remove('active');
  __dotsEl.children[__cur].classList.remove('active');
  __cur = (n + __total) % __total;
  __slides[__cur].classList.add('active');
  __dotsEl.children[__cur].classList.add('active');
  document.getElementById('counter').textContent = (__cur + 1) + ' / ' + __total;
  initCharts(__cur);
}
function go(d) { goTo(__cur + d); }

document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') go(1);
  if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') go(-1);
});

// ── tab 通用切换 ──
function switchTab(group, idx) {
  document.querySelectorAll(`.stab[data-group="${group}"]`).forEach((btn, i) => {
    btn.classList.toggle('active', i === idx);
  });
  document.querySelectorAll(`.stab-panel[data-group="${group}"]`).forEach(panel => {
    panel.style.display = parseInt(panel.dataset.idx) === idx ? 'block' : 'none';
  });
}

// ── 图表初始化分发器 ──
const __chartsInited = {};
function initCharts(idx) {
  if (__chartsInited[idx]) return;
  __chartsInited[idx] = true;
  const fn = window['initSlide' + (idx + 1)];
  if (typeof fn === 'function') fn();
}

// ══════════════════════════════════════════════════════════
//  ECharts helper
// ══════════════════════════════════════════════════════════

// 把 'var(--accent)' 这种字符串解析为实际颜色值
function _cssVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}
function _resolveVars(value) {
  if (typeof value !== 'string') return value;
  return value.replace(/var\((--[\w-]+)\)/g, (_, n) => _cssVar(n));
}
function resolveCssVars(obj) {
  if (Array.isArray(obj)) return obj.map(resolveCssVars);
  if (obj && typeof obj === 'object') {
    const out = {};
    for (const k in obj) out[k] = resolveCssVars(obj[k]);
    return out;
  }
  return _resolveVars(obj);
}

// ECharts 全局基线
function getEchartsBase() {
  return {
    textStyle: { fontFamily: _cssVar('--font-sans'), color: _cssVar('--text2') },
    grid: { left: 40, right: 24, top: 24, bottom: 32, containLabel: true },
    legend: {
      bottom: 0, itemGap: 16, itemWidth: 12, itemHeight: 8,
      textStyle: { color: _cssVar('--text2'), fontSize: 11 },
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15,23,42,0.95)',
      borderWidth: 0,
      textStyle: { color: '#ffffff', fontSize: 11 },
      axisPointer: { type: 'line', lineStyle: { color: 'rgba(15,23,42,0.20)', type: 'dashed' } }
    },
    xAxis: {
      type: 'category',
      axisLine:  { lineStyle: { color: _cssVar('--border') } },
      axisTick:  { show: false },
      axisLabel: { color: _cssVar('--text3'), fontSize: 10 },
      splitLine: { show: false },
    },
    yAxis: {
      type: 'value',
      axisLine:  { show: false },
      axisTick:  { show: false },
      axisLabel: { color: _cssVar('--text3'), fontSize: 10 },
      splitLine: { lineStyle: { color: _cssVar('--border') } },
    },
    color: [
      _cssVar('--accent'),  _cssVar('--accent2'), _cssVar('--accent3'),
      _cssVar('--warn'),    '#8b5cf6',            _cssVar('--danger'),
    ],
    animation: true,
    animationDuration: 600,
  };
}

// 深合并（option 对象级，简单场景够用）
function mergeDeep(a, b) {
  if (!b) return a;
  const out = { ...a };
  for (const k in b) {
    if (b[k] && typeof b[k] === 'object' && !Array.isArray(b[k])) {
      out[k] = mergeDeep(a[k] || {}, b[k]);
    } else {
      out[k] = b[k];
    }
  }
  return out;
}

// 初始化 ECharts 并注册到 __charts
function initChart(elId, optionFactory) {
  const el = document.getElementById(elId);
  if (!el) return null;
  // 若已存在实例（切主题情况），先 dispose
  if (window.__charts[elId]) {
    try { window.__charts[elId].dispose(); } catch (e) {}
  }
  const chart = echarts.init(el);
  window.__charts[elId] = chart;
  window.__chartOptions[elId] = optionFactory;
  const opt = mergeDeep(getEchartsBase(), optionFactory());
  chart.setOption(resolveCssVars(opt));
  return chart;
}

// 切主题后调用：用每个 chart 注册的 factory 重新生成 option
function reinitAllCharts() {
  for (const [id, factory] of Object.entries(window.__chartOptions)) {
    const el = document.getElementById(id);
    if (!el) continue;
    if (window.__charts[id]) { try { window.__charts[id].dispose(); } catch (e) {} }
    const chart = echarts.init(el);
    window.__charts[id] = chart;
    const opt = mergeDeep(getEchartsBase(), factory());
    chart.setOption(resolveCssVars(opt));
  }
}

// ══════════════════════════════════════════════════════════
//  常用图表范本
// ══════════════════════════════════════════════════════════

// 1) 双 y 轴时间序列折线（主指标 + 副指标 + 里程碑竖线）
//    cfg 可选：{ leftName, rightName, leftUnit, rightUnit }
function renderDailyDual(elId, labels, leftData, rightData, marks = [], cfg = {}) {
  const leftName  = cfg.leftName  || '主指标';
  const rightName = cfg.rightName || '副指标';
  return initChart(elId, () => ({
    legend: { data: [leftName, rightName], bottom: 0 },
    xAxis: { data: labels, axisLabel: { interval: 'auto', maxTicksLimit: 15 } },
    yAxis: [
      { type: 'value', name: cfg.leftUnit  || leftName,  nameTextStyle: { fontSize: 9 }, position: 'left' },
      { type: 'value', name: cfg.rightUnit || rightName, nameTextStyle: { fontSize: 9 }, position: 'right', splitLine: { show: false } },
    ],
    series: [
      {
        name: leftName, type: 'line', data: leftData,
        smooth: 0.35, symbol: 'none',
        lineStyle: { width: 1.8 },
        areaStyle: { opacity: 0.08 },
        yAxisIndex: 0,
        markLine: marks.length ? {
          symbol: 'none',
          lineStyle: { type: 'dashed', width: 1 },
          label: { fontSize: 9, position: 'insideEndTop' },
          data: marks.map(m => ({
            xAxis: m.x,
            label: { formatter: m.label, color: m.color },
            lineStyle: { color: m.color },
          })),
        } : undefined,
      },
      {
        name: rightName, type: 'line', data: rightData,
        smooth: 0.35, symbol: 'none',
        lineStyle: { width: 1.5, type: 'dashed' },
        yAxisIndex: 1,
      },
    ],
  }));
}

// 2) 100% 堆叠条形（前后占比对比）
function renderShare100(elId, categoryLabels, seriesNames, preData, postData) {
  const series = seriesNames.map((name, i) => ({
    name, type: 'bar', stack: 'pct',
    barCategoryGap: '40%',
    label: {
      show: true,
      formatter: p => p.value < 4 ? '' : p.value.toFixed(1) + '%',
      color: '#fff', fontSize: 10, fontWeight: 600,
    },
    data: [preData[i], postData[i]],
  }));
  return initChart(elId, () => ({
    legend: { bottom: 0 },
    yAxis: { type: 'category', data: categoryLabels, axisLine: { show: false } },
    xAxis: { type: 'value', max: 100, axisLabel: { formatter: '{value}%' } },
    series,
  }));
}

// 3) 多对象趋势对比（折线）
function renderMultiTrend(elId, labels, seriesMap /* {name: data[]} */, colorMap) {
  const series = Object.keys(seriesMap).map(name => ({
    name, type: 'line', data: seriesMap[name],
    smooth: 0.35, symbol: 'none',
    lineStyle: { width: 2, color: colorMap?.[name] },
    itemStyle: { color: colorMap?.[name] },
  }));
  return initChart(elId, () => ({
    legend: { bottom: 0, data: Object.keys(seriesMap) },
    xAxis: { data: labels, axisLabel: { maxTicksLimit: 10 } },
    yAxis: { axisLabel: { formatter: '{value}%' } },
    series,
  }));
}

// 4) 横向 Top-N mini-bar（自定义 div，不用 ECharts；外层容器需有 flex 布局）
function renderMiniBars(containerId, items /* [[name, val], ...] */, color) {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = '';
  const max = Math.max(...items.map(([, v]) => v));
  items.forEach(([name, val]) => {
    const pct = max ? Math.max(2, val / max * 100) : 0;
    el.insertAdjacentHTML('beforeend', `
      <div class="mini-bar-row">
        <div class="mini-bar-label">${name}</div>
        <div class="mini-bar-track"><div class="mini-bar-fill" style="width:${pct}%;background:${color};"></div></div>
        <div class="mini-bar-val">${val.toLocaleString()}</div>
      </div>`);
  });
}

// 5) KPI 网格渲染（从数据生成）
function renderKpiGrid(containerId, kpis /* [{num, label, sub, color}] */) {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = kpis.map(k => `
    <div class="kpi-card ${k.color || 'blue'}">
      ${k.icon ? `<div class="kpi-icon">${k.icon}</div>` : ''}
      <div class="kpi-num">${k.num}</div>
      <div class="kpi-label">${k.label}</div>
      ${k.sub ? `<div class="kpi-desc">${k.sub}</div>` : ''}
    </div>
  `).join('');
}

// ── Boot ──
window.addEventListener('DOMContentLoaded', () => {
  __initNav();
  initCharts(0);
});
