#!/usr/bin/env python3
"""转义散文里裸露的 <…>/{{…}}，避免 VitePress(Vue) 把它当标签/插值。
仅动散文：跳过 ``` 围栏代码块，跳过行内 `code` 段。代码里的 < 一律不碰。"""
import sys, pathlib, re

def escape_prose(seg: str) -> str:
    # 只转义 <（去掉标签起始即可）；> 保留，避免破坏行首 blockquote
    return seg.replace("<", "&lt;")

def process_line(line: str) -> str:
    # 按反引号切分：奇数段是行内代码(保留)，偶数段是散文(转义)
    parts = line.split("`")
    for i in range(0, len(parts), 2):
        parts[i] = escape_prose(parts[i])
    return "`".join(parts)

total = 0
for p in sorted(pathlib.Path(sys.argv[1]).glob("*.md")):
    out, in_fence, n = [], False, 0
    for line in p.read_text(encoding="utf-8").split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line); continue
        if in_fence:
            out.append(line); continue
        new = process_line(line)
        if new != line:
            n += 1
        out.append(new)
    p.write_text("\n".join(out), encoding="utf-8")
    total += n
    print(f"{p.name:32s} 修 {n} 行")
print(f"—— 合计 {total} 行 ——")
