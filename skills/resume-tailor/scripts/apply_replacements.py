# -*- coding: utf-8 -*-
"""Apply text-only replacements to a copy of a .docx resume, preserving ALL
formatting. Only runs that carry w:t are rewritten; drawing/icon runs, list
numbering (numPr), tables, shading and textboxes are left untouched.

Usage:
    python apply_replacements.py SRC.docx OUT.docx mapping.json [--dry-run]

mapping.json:
{
  "replacements": [
    {"match": "prefix or full text", "mode": "start", "new": "replacement"},
    {"match": "Exact paragraph text", "mode": "exact",
     "new": [["Bold label:", true], [" normal value", false]]},
    {"match": "repeated line", "mode": "exact", "new": "x", "all": true}
  ]
}

`new` may be:
  - a string  -> the whole paragraph becomes a single run, keeping the first
                 text run's formatting; or
  - a list of [text, bold] segments -> formatted runs (bold true/false applied
                 explicitly). Use for bold labels / sentence emphasis.

The source file is opened read-only and never modified.
"""
import argparse
import copy
import json
import sys
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def norm(s):
    return " ".join((s or "").split())


def para_text(p):
    return "".join(t.text or "" for t in p.iter(qn("w:t")))


def text_runs(p):
    out = []
    for r in p.iter(qn("w:r")):
        if r.find(qn("w:t")) is None:
            continue
        if r.find(qn("w:drawing")) is not None or r.find(qn("w:pict")) is not None:
            continue
        out.append(r)
    return out


def replace_paragraph(p, content):
    runs = text_runs(p)
    if not runs:
        return False
    base_rpr = runs[0].find(qn("w:rPr"))
    after = runs[-1].getnext()
    for r in runs:
        r.getparent().remove(r)

    if isinstance(content, str):
        content = [(content, None)]

    for text, bold in content:
        nr = OxmlElement("w:r")
        if base_rpr is not None:
            nr.append(copy.deepcopy(base_rpr))
        rpr = nr.find(qn("w:rPr"))
        if bold is not None:
            if rpr is None:
                rpr = OxmlElement("w:rPr")
                nr.insert(0, rpr)
            b = rpr.find(qn("w:b"))
            if bold and b is None:
                rpr.append(OxmlElement("w:b"))
            elif not bold and b is not None:
                rpr.remove(b)
        t = OxmlElement("w:t")
        t.set(qn("xml:space"), "preserve")
        t.text = text
        nr.append(t)
        if after is not None:
            after.addprevious(nr)
        else:
            p.append(nr)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("mapping")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    with open(args.mapping, "r", encoding="utf-8") as f:
        spec = json.load(f)
    reps = spec.get("replacements", spec if isinstance(spec, list) else [])

    doc = Document(args.src)
    paras = [(p, norm(para_text(p))) for p in doc.element.body.iter(qn("w:p"))]
    paras = [(p, t) for p, t in paras if t]

    errors = []
    applied = 0
    for rep in reps:
        match = rep["match"]
        mode = rep.get("mode", "start")
        content = rep["new"]
        allow_all = rep.get("all", False)
        if mode == "exact":
            hits = [p for p, t in paras if t == norm(match)]
        else:
            hits = [p for p, t in paras if t.startswith(match)]
        if not hits:
            errors.append("NO MATCH: %r" % match)
            continue
        if len(hits) > 1 and not allow_all:
            errors.append("AMBIGUOUS (%d): %r" % (len(hits), match))
            continue
        for p in hits:
            if args.dry_run:
                applied += 1
            elif replace_paragraph(p, content):
                applied += 1
            else:
                errors.append("NO TEXT RUNS: %r" % match)

    if not args.dry_run:
        doc.save(args.out)

    print("APPLIED: %d" % applied)
    print("ERRORS: %d" % len(errors))
    for e in errors:
        print("  -", e)
    if not args.dry_run:
        print("SAVED:", args.out)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
