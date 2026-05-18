#!/usr/bin/env bash
# quickstart.sh — 一键把 ppt-report-generator assets 初始化为新项目
#
# Usage:
#   ./quickstart.sh <target-dir>
#
# Example:
#   ./quickstart.sh ../my-monthly-report
#   cd ../my-monthly-report
#   python3 build.py
#   open dist/*.html

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <target-dir>"
  echo ""
  echo "示例：./quickstart.sh ../my-report"
  exit 1
fi

TARGET="$1"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ASSETS_DIR="$SCRIPT_DIR/assets"

if [ ! -d "$ASSETS_DIR" ]; then
  echo "❌ assets 目录不存在：$ASSETS_DIR"
  echo "请确认你在 ppt-report-generator 仓库根目录运行此脚本。"
  exit 1
fi

if [ -e "$TARGET" ]; then
  echo "❌ 目标目录已存在：$TARGET"
  echo "请指定一个不存在的路径，或先删除 / 改名。"
  exit 1
fi

echo "🚀 初始化 ppt-report-generator 项目到：$TARGET"

mkdir -p "$TARGET/src"

# 拷贝 assets 内容到 src/，根级脚本（build / export / xlsx2json）移到项目根
rsync -a --exclude='__pycache__' --exclude='.DS_Store' "$ASSETS_DIR/" "$TARGET/src/"
mv "$TARGET/src/build.py" "$TARGET/build.py"
mv "$TARGET/src/export_pdf.py" "$TARGET/export_pdf.py"
mv "$TARGET/src/xlsx2json.py" "$TARGET/xlsx2json.py"

# 创建 build.py 期望的目录
mkdir -p "$TARGET/src/slides" "$TARGET/src/data"

# 准备一个最小可运行的占位封面页（让 build 能直接跑通）
cat > "$TARGET/src/slides/slide-1.html" <<'EOF'
  <div class="slide" id="s1">
    <div class="slide-label">占位 · 替换为你的内容</div>
    <div class="slide-title">这里是 <span>你的汇报</span> 标题</div>
    <div class="slide-subtitle">
      副标题写一句结论 · 关键数字用 <strong>strong</strong> 高亮 · <span class="pos">+正向</span> / <span class="neg">-负向</span> / <span class="warn">警示</span>
    </div>
    <div style="flex:1;display:flex;align-items:center;justify-content:center;color:var(--text3);font-family:var(--font-mono);text-align:center;line-height:1.8;">
      编辑 <strong style="color:var(--text);">src/slides/slide-1.html</strong> 开始 ·
      运行 <strong style="color:var(--text);">python3 build.py</strong> 重新合成<br>
      添加新页：从 <strong style="color:var(--text);">src/slides-templates/</strong> 选一套模板拷过来
    </div>
  </div>
EOF

# 对应的空 init 函数
cat > "$TARGET/src/scripts/slide-1.js" <<'EOF'
function initSlide1() {}
EOF

# 给项目根加一份简短的说明
cat > "$TARGET/README.md" <<'EOF'
# 我的汇报

由 [ppt-report-generator](https://github.com/) 模板初始化。

## 常用命令

```bash
python3 build.py        # 合成 HTML → 输出到 dist/
open dist/*.html        # 浏览器打开
python3 export_pdf.py   # 导出 PDF → dist/（需 playwright + img2pdf）
```

## 添加一页

```bash
# 1. 选模板
cp src/slides-templates/two-country.html src/slides/slide-2.html

# 2. 写数据（xlsx / csv / json 三选一，build 自动识别）
#    xlsx：直接把 Excel 文件丢进 src/data/，多 sheet 自动展开
cp ~/Downloads/我的数据.xlsx src/data/slide-2.xlsx

# 3. 写图表初始化
cat > src/scripts/slide-2.js <<'JS'
function initSlide2() {
  const D = window.__DATA_2__;   // build 自动从 xlsx/csv/json 读取
  // ...
}
JS

# 4. 改文案 → build
python3 build.py
```

## 数据格式

- **xlsx** — 每个 sheet → JSON 顶层一个 key（推荐 · 需 `pip install openpyxl`）
- **csv**  — 整份 → JSON 数组（单表数据）
- **json** — 直接读取（复杂嵌套结构）

详见 `src/README.md`。
EOF

echo ""
echo "✅ 初始化完成！"
echo ""
echo "下一步："
echo "  cd $TARGET"
echo "  python3 build.py"
echo "  open dist/*.html"
echo ""
