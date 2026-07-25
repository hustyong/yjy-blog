#!/usr/bin/env bash
# 从 ../analysis 重新生成 site/guide/*.md（拷贝 → 编号平移+链接化 → 转义 <）。
# analysis/ 是唯一内容源，本脚本只写 site/guide，绝不改 analysis。
# 用法：在 site/ 下执行  bash sync.sh
set -euo pipefail
cd "$(dirname "$0")"
# 内容源在另一仓库（claude-code-learn/analysis）；可用环境变量 ANALYSIS_SRC 覆盖
SRC="${ANALYSIS_SRC:-/Users/jieyongyang/work/claude-code-learn/analysis}"
DST="guide"

declare -a MAP=(
  "00-Overview-and-Main-Loop.md:00-overview.md"
  "Tool-Call-Authority-System-Complete.md:01-tool-call-authority.md"
  "01-Agent-System.md:02-agent.md"
  "02-Skill-System.md:03-skill.md"
  "03-Session-and-Compaction.md:04-session-compaction.md"
  "04-MCP-Protocol.md:05-mcp.md"
  "05-Plugin-System.md:06-plugin.md"
  "06-Hooks-System.md:07-hooks.md"
  "07-Context-Assembly.md:08-context-assembly.md"
  "08-Bootstrap-and-Performance.md:09-bootstrap-performance.md"
  "Prompt-Cache.md:prompt-cache.md"
  "09-Permission-Rule-System.md:10-permission-rules.md"
  "10-Bash-Command-Security.md:11-bash-security.md"
)

mkdir -p "$DST"
for pair in "${MAP[@]}"; do
  src="${pair%%:*}"; dst="${pair##*:}"
  cp "$SRC/$src" "$DST/$dst"
done
echo "已拷贝 ${#MAP[@]} 篇 → $DST/"

python3 .vitepress/linkify.py "$DST"        # 《0X》+1 平移 + 交叉引用转链接
python3 .vitepress/escape_angles.py "$DST"  # 散文里裸 < 转义，防 Vue 误判标签
echo "同步完成。运行 npm run docs:dev 预览，或 npm run docs:build 构建。"
