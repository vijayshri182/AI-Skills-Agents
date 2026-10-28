# -*- coding: utf-8 -*-
"""Verify a tailored .docx: required keywords present, forbidden strings gone.

Usage:
    python verify_text.py "Tailored.docx" --require "Site Reliability" --require "Kubernetes" --forbid "Old Title"
"""
import argparse
import sys
from docx import Document
from docx.oxml.ns import qn


def full_text(path):
    doc = Document(path)
    return "\n".join("".join(t.text or "" for t in p.iter(qn("w:t")))
                     for p in doc.element.body.iter(qn("w:p")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("--require", action="append", default=[])
    ap.add_argument("--forbid", action="append", default=[])
    args = ap.parse_args()

    txt = full_text(args.docx)
    ok = True
    for kw in args.require:
        hit = kw in txt
        ok = ok and hit
        print(("OK   " if hit else "MISS ") + kw)
    for kw in args.forbid:
        hit = kw in txt
        ok = ok and not hit
        print(("BAD  " if hit else "gone ") + kw)
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
