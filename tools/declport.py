"""Carry 6815's 4.32->4.34 port across to 6812/6813 one top-level declaration at a time.

A chunk is a run of lines starting at a column-0 line. Chunks are aligned between 6815@4.32 and
6815@4.34 per file; every changed chunk (with any chunk the port inserted just before it, such as
`set_option maxRecDepth ... in`) becomes an old-text -> new-text rule, applied wherever the old
text appears verbatim in the target tree.
"""
import difflib, sys
from pathlib import Path

old_root, new_root, target = map(Path, sys.argv[1:4])

def chunks(text):
    out, cur = [], []
    for line in text.split("\n"):
        if line and not line[0].isspace() and cur:
            out.append("\n".join(cur)); cur = []
        cur.append(line)
    if cur: out.append("\n".join(cur))
    return out

rules = {}
for f in sorted(old_root.glob("*.lean")):
    g = new_root / f.name
    if not g.exists(): continue
    a, b = chunks(f.read_text()), chunks(g.read_text())
    pending = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if tag == "insert":
            pending = b[j1:j2]; continue
        if tag == "replace":
            olds, news = a[i1:i2], b[j1:j2]
            if len(olds) == len(news):
                for k, (o, n) in enumerate(zip(olds, news)):
                    rules[o] = "\n".join((pending if k == 0 else []) + [n])
            else:
                rules["\n".join(olds)] = "\n".join(pending + news)
        elif tag == "equal" and pending:
            rules[a[i1]] = "\n".join(pending + [b[j1]])
        pending = []

applied = 0
for f in sorted(target.glob("*.lean")):
    cs = chunks(f.read_text()); changed = False
    for idx, c in enumerate(cs):
        if c in rules and rules[c] != c:
            cs[idx] = rules[c]; applied += 1; changed = True
    if changed: f.write_text("\n".join(cs))
print(f"{len(rules)} rules; applied {applied} in {target}")
