# -*- coding: utf-8 -*-
"""List every paragraph of a .docx resume, in document order, with its location
(body / table cell / nested table) and text. Read-only.

Usage:
    python dump_paragraphs.py "Original.docx" [--out paras.txt]
"""
import argparse
import sys
from docx import Document
from docx.oxml.ns import qn


def iter_block_paragraphs(container, loc="BODY"):
    """Yield (w:p element, location) recursively through body and tables."""
    for child in container.iterchildren():
        if child.tag == qn("w:p"):
            yield (child, loc)
        elif child.tag == qn("w:tbl"):
            for row in child.findall(qn("w:tr")):
                for ci, cell in enumerate(row.findall(qn("w:tc"))):
                    yield from iter_block_paragraphs(cell, loc + "+TC%d" % ci)


def para_text(p):
    return "".join(t.text or "" for t in p.iter(qn("w:t")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    doc = Document(args.src)
    lines = []
    idx = 0
    total_txt = 0
    for p, loc in iter_block_paragraphs(doc.element.body):
        idx += 1
        txt = para_text(p)
        if txt.strip():
            total_txt += 1
        lines.append("[%03d] (%s) %s" % (idx, loc, txt))
    lines.append("")
    lines.append("TOTAL paragraphs: %d   (non-empty: %d)" % (idx, total_txt))
    out = "\n".join(lines)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print("wrote", args.out, "(%d lines)" % len(lines))
    else:
        sys.stdout.write(out + "\n")


if __name__ == "__main__":
    main()
