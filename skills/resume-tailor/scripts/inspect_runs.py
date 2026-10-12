# -*- coding: utf-8 -*-
"""Show run-level formatting for every paragraph of a .docx resume so you can
tell which lines have bold labels, selective bolding, or icon drawings.
Read-only.

Usage:
    python inspect_runs.py "Original.docx" [--out runs.txt]
"""
import argparse
import sys
from docx import Document
from docx.oxml.ns import qn


def iter_block_paragraphs(container, loc="BODY"):
    for child in container.iterchildren():
        if child.tag == qn("w:p"):
            yield (child, loc)
        elif child.tag == qn("w:tbl"):
            for row in child.findall(qn("w:tr")):
                for ci, cell in enumerate(row.findall(qn("w:tc"))):
                    yield from iter_block_paragraphs(cell, loc + "+TC%d" % ci)


def para_text(p):
    return "".join(t.text or "" for t in p.iter(qn("w:t")))


def run_info(r):
    txt = "".join(t.text or "" for t in r.iter(qn("w:t")))
    rpr = r.find(qn("w:rPr"))
    bold = ital = color = font = size = None
    if rpr is not None:
        if rpr.find(qn("w:b")) is not None:
            bold = True
        if rpr.find(qn("w:i")) is not None:
            ital = True
        c = rpr.find(qn("w:color"))
        if c is not None:
            color = c.get(qn("w:val"))
        rfs = rpr.find(qn("w:rFonts"))
        if rfs is not None:
            font = rfs.get(qn("w:ascii"))
        sz = rpr.find(qn("w:sz"))
        if sz is not None:
            size = sz.get(qn("w:val"))
    has_draw = (r.find(qn("w:drawing")) is not None
                or r.find(qn("w:pict")) is not None)
    return (txt, bold, ital, color, font, size, has_draw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    doc = Document(args.src)
    lines = []
    idx = 0
    for p, loc in iter_block_paragraphs(doc.element.body):
        idx += 1
        lines.append("[%03d] %s | %r" % (idx, loc, para_text(p)))
        for (t, b, i, c, f, s, d) in (run_info(r) for r in p.findall(qn("w:r"))):
            lines.append("      run: b=%s i=%s color=%s font=%s sz=%s draw=%s txt=%r"
                         % (b, i, c, f, s, d, t))
    lines.append("")
    lines.append("TOTAL: %d" % idx)
    out = "\n".join(lines)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print("wrote", args.out, "(%d lines)" % len(lines))
    else:
        sys.stdout.write(out + "\n")


if __name__ == "__main__":
    main()
