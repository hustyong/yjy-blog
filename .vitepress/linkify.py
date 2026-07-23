#!/usr/bin/env python3
"""把 guide/*.md 副本里的 《…》 交叉引用转成 VitePress 相对链接，并按 A 方案 +1 平移编号。
仅处理散文（跳过 ``` 围栏代码块）；analysis/ 原文不受影响（本脚本只跑在 site/guide 副本上）。
未在映射表里的 《…》 原样保留。"""
import re, sys, pathlib

# 全量映射：匹配到的整段 《…》 → 替换文本（含新编号与相对链接）
M = {
    # —— 纯数字引用（旧号 → 新号 +1；00 不变）——
    "《00》": "[《00》](./00-overview.md)",
    "《01》": "[《02》](./02-agent.md)",
    "《02》": "[《03》](./03-skill.md)",
    "《03》": "[《04》](./04-session-compaction.md)",
    "《04》": "[《05》](./05-mcp.md)",
    "《06》": "[《07》](./07-hooks.md)",
    "《07》": "[《08》](./08-context-assembly.md)",
    "《09》": "[《10》](./10-permission-rules.md)",
    "《10》": "[《11》](./11-bash-security.md)",
    # —— 数字+名字 变体 ——
    "《02 Skill 系统》": "[《03 Skill 系统》](./03-skill.md)",
    "《07 上下文装配》": "[《08 上下文装配》](./08-context-assembly.md)",
    "《09 · 权限规则系统》": "[《10 · 权限规则系统》](./10-permission-rules.md)",
    "《10 · Bash 命令安全》": "[《11 · Bash 命令安全》](./11-bash-security.md)",
    "《10 · Bash / 命令安全、沙箱与分类器》": "[《11 · Bash / 命令安全、沙箱与分类器》](./11-bash-security.md)",
    # —— 组合引用 ——
    "《02/07》": "[《03》](./03-skill.md)/[《08》](./08-context-assembly.md)",
    # —— 按名字引用（无号，仅加链接）——
    "《工具·调用·权限系统》": "[《工具·调用·权限系统》](./01-tool-call-authority.md)",
    "《全景与主循环》": "[《全景与主循环》](./00-overview.md)",
    "《Agent 系统》": "[《Agent 系统》](./02-agent.md)",
    "《Skill 系统》": "[《Skill 系统》](./03-skill.md)",
    "《会话管理与压缩》": "[《会话管理与压缩》](./04-session-compaction.md)",
    "《MCP 协议》": "[《MCP 协议》](./05-mcp.md)",
    "《Plugin 系统》": "[《Plugin 系统》](./06-plugin.md)",
    "《Hooks 扩展系统》": "[《Hooks 扩展系统》](./07-hooks.md)",
    "《上下文装配》": "[《上下文装配》](./08-context-assembly.md)",
    "《权限规则系统》": "[《权限规则系统》](./10-permission-rules.md)",
}

REF = re.compile(r"《[^》]*》")

def transform(text):
    out, in_fence, n = [], False, 0
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line); continue
        if in_fence:
            out.append(line); continue
        def repl(m):
            nonlocal n
            r = M.get(m.group(0))
            if r is None:
                return m.group(0)
            n += 1
            return r
        out.append(REF.sub(repl, line))
    return "\n".join(out), n

total = 0
for p in sorted(pathlib.Path(sys.argv[1]).glob("*.md")):
    txt = p.read_text(encoding="utf-8")
    new, n = transform(txt)
    if n:
        p.write_text(new, encoding="utf-8")
    total += n
    print(f"{p.name:32s} 转换 {n} 处")
print(f"—— 合计 {total} 处 ——")
