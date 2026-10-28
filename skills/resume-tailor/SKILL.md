---
name: resume-tailor
description: Use when tailoring an existing Word (.docx) resume/CV to a specific job description, JD, role, or company while keeping the résumé's original look and layout. Trigger on requests like "tailor my resume", "customize my CV for this job", "update the resume text for <company>", "tailor my resume without changing the format", or when given a .docx plus a job posting and asked to match keywords/skills. Covers text-only in-place editing that preserves 100% of formatting (fonts, colors, bullets, tables, icons, layout), then PDF export and preview.
license: MIT
---

# Resume Tailor (format-preserving, text-only)

Tailor an existing `.docx` resume to a job description by **replacing only the
text**, never the design. The original file is never modified: a copy is edited
and saved to a new path. Fonts, colors, sizes, list numbering, tables, icon
drawings, headers, and SmartArt are preserved exactly because only the
paragraph text runs (`w:t`) are rewritten.

## When to use

- User supplies a `.docx` resume and a JD/role/company and wants the text
  updated to match, but the visual design kept identical.
- The résumé uses a designed template (two-column layout, colored headings,
  icon bullets, shaded bands, career timeline) that must not be disturbed.
- User says things like "just update the text", "don't change the format",
  "keep the same look", "make it look like the original".

## Hard requirements

- **Word** must be installed (PDF export uses Word COM automation).
- Python with `python-docx` and `pymupdf` (see `scripts/requirements.txt`).
- Windows / PowerShell (the PDF export helper is a `.ps1`).
- **Never overwrite the source resume.** Always write to a new output path.

## The core principle: match counts, change words

A designed résumé's layout depends on how many bullets/lines each section has.
If you add or remove bullets, tables reflow and the design breaks. So:

- Keep the **same number of bullets/items/paragraphs** the original has.
- Fold extra desired points into existing lines; split a point into two lines
  only if you must, using an existing line's slot.
- Never add/remove paragraphs, table rows, or cells.

## Workflow

### 1. Inspect the original (read-only)

```powershell
python scripts\dump_paragraphs.py "C:\path\Original.docx" --out paras.txt
python scripts\inspect_runs.py      "C:\path\Original.docx" --out runs.txt
```

- `dump_paragraphs.py` lists every paragraph (body + nested tables) as
  `[NNN] (LOC) text`, so you know the section order and counts.
- `inspect_runs.py` shows each paragraph's runs with `bold`, `color`, `font`,
  `sz`, and whether the run carries a `drawing` (icon). Use it to see which
  lines have **bold labels** (e.g. `"Cloud & Infrastructure:"`) or **selective
  bolding** inside a sentence.

Important structural facts to expect (and NOT to edit):
- Bullets often come from Word **list numbering** (`w:numPr`) or from **icon
  drawing runs** in their own table cells. Replacing text leaves these intact.
- Headings, contact lines with hyperlinks, the career-timeline textboxes, and
  SmartArt are best left alone.

### 2. Build a replacement mapping (JSON)

Create a JSON file describing the text swaps. `new` is either a plain string
(whole paragraph becomes one run, keeping the first run's formatting) or a list
of `[text, bold]` segments to reproduce bold labels / selective bolding.

```json
{
  "replacements": [
    { "match": "Engineering Leadership & Team Management", "mode": "exact",
      "new": "Engineering Leadership & Team Development" },

    { "match": "Version Control & Repository Management:",
      "mode": "start",
      "new": [["SRE, Monitoring & Observability:", true],
              [" Application Logs, RCA, Performance Optimization", false]] }
  ]
}
```

Rules for `match`:
- `mode: "exact"` matches the whole normalized paragraph (whitespace-collapsed).
- `mode: "start"` matches a paragraph that **starts with** the given prefix.
  Prefer a short, unique **ASCII** prefix. This avoids failures caused by
  non-ASCII characters (en/em dashes, curly quotes) and by runs split mid-word.
- Each `match` must hit exactly **one** paragraph unless `"all": true` is set.
  The script reports any zero/multiple matches as errors so you can fix them.

Rules for `new`:
- Plain string → one run with the first run's `rPr`.
- Segment list → each `[text, bold]` becomes a run; `bold: true/false`
  explicitly adds/removes `w:b`. Use this for labelled lines and for
  sentence-level emphasis so the original bold pattern is reproduced.

A worked example lives in `reference/mapping.example.json`.

### 3. Apply the replacements

```powershell
python scripts\apply_replacements.py "C:\path\Original.docx" "C:\path\Tailored.docx" mapping.json
```

Output prints `APPLIED`, `ERRORS`, and any unmatched keys. Fix mappings until
`ERRORS: 0`.

### 4. Export to PDF (and check page count)

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\export_pdf.ps1 -In "C:\path\Tailored.docx" -Out "C:\path\Tailored.pdf"
```

`-ExecutionPolicy Bypass` is needed on machines whose PowerShell blocks local
`.ps1` scripts. It prints the page count. **The tailored PDF should have the
same number of pages as the original** — a different count means content was
added/removed and the layout shifted.

### 5. Preview and verify

```powershell
python scripts\verify_text.py "C:\path\Tailored.docx" --require "Site Reliability" --forbid "CompanyX"
python scripts\render_preview.py --out "C:\path\previews" "C:\path\Original.pdf" "C:\path\Tailored.pdf"
```

- `verify_text.py` confirms required keywords are present and forbidden/old
  strings are gone.
- `render_preview.py` renders side-by-side PNGs and a `preview.html`.
- Because the design is untouched, a text diff is the reliable correctness
  check; visual pixel-parity is guaranteed by the text-only edit.

## Editing checklist

1. Copy original → new file (script does this; source is opened read-only).
2. Subtitle/summary → align to the JD's title and top keywords.
3. Core competencies → swap generic items for JD-specific ones, **same count**.
4. Skills → add a JD-relevant lead line; reorder; keep the same line count.
5. Experience bullets → reword in place with JD vocabulary, **same count per
   role**; never invent metrics, employers, dates, or tools.
6. Fix obvious typos if present.
7. Export, confirm page count, run verify + preview.

## Guardrails

- Do **not** fabricate experience, tools, metrics, or outcomes. Only reframe
  what the original already claims.
- Do **not** add sections, headings, bullets, or table rows.
- Do **not** edit headings, icons, borders, shading, or the timeline.
- Always keep the original file untouched for future re-tailoring against other
  JDs.

## Install this skill

Copy or reference the skill directory so opencode can load it:

- Global (per user): copy `skills/resume-tailor/` into
  `~/.config/opencode/skills/resume-tailor/`, or
- Add its parent path to `opencode.json`:

  ```json
  { "$schema": "https://opencode.ai/config.json",
    "skills": { "paths": ["C:/path/to/AI-Skills-Agents/skills"] } }
  ```

Restart opencode after adding it.
