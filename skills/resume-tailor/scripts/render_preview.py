# -*- coding: utf-8 -*-
"""Render one or more PDFs to per-page PNGs and a side-by-side preview.html.

Usage:
    python render_preview.py --out previews Original.pdf Tailored.pdf [Designed.pdf]
"""
import argparse
import os
import pymupdf  # pip install pymupdf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="previews")
    ap.add_argument("--dpi", type=int, default=140)
    ap.add_argument("--width", type=int, default=620)
    ap.add_argument("pdfs", nargs="+")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    sets = []
    for pdf in args.pdfs:
        tag = os.path.splitext(os.path.basename(pdf))[0]
        tag = "".join(c if c.isalnum() or c in "-_" else "_" for c in tag)
        sets.append((tag, pdf))

    pages = {}
    for tag, pdf in sets:
        d = pymupdf.open(pdf)
        pages[tag] = d.page_count
        for i, pg in enumerate(d):
            pix = pg.get_pixmap(dpi=args.dpi)
            pix.save(os.path.join(args.out, "%s_page%d.png" % (tag, i + 1)))
        print("%s -> %d pages" % (tag, d.page_count))

    order = [t for t, _ in sets]
    maxp = max(pages.values())
    rows = []
    for i in range(maxp):
        cells = []
        for tag in order:
            if i < pages[tag]:
                cells.append(
                    '<td><h3>%s page %d</h3><img src="%s_page%d.png" '
                    'style="width:%dpx;border:1px solid #ccc;'
                    'box-shadow:2px 2px 6px rgba(0,0,0,.2)"></td>'
                    % (tag, i + 1, tag, i + 1, args.width))
            else:
                cells.append("<td></td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")

    html = (
        "<!DOCTYPE html><html><head><meta charset=\"utf-8\">"
        "<title>Resume preview</title><style>"
        "body{font-family:Segoe UI,Arial,sans-serif;margin:24px;background:#f5f5f5}"
        "h1{font-size:20px}h3{font-size:13px;color:#075650}"
        "table{border-collapse:separate;border-spacing:16px}td{vertical-align:top}"
        "</style></head><body><h1>Resume preview</h1><table>"
        + "".join(rows) + "</table></body></html>"
    )
    out_html = os.path.join(args.out, "preview.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    print("preview.html written:", out_html)


if __name__ == "__main__":
    main()
