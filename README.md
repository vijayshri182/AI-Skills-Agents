# AI-Skills-Agents

Reusable [opencode](https://opencode.ai) skills. Clone this repo on any laptop
and point opencode at the `skills/` folder (or copy a skill into your global
config) to use them.

## Skills

| Skill | What it does |
| --- | --- |
| [`resume-tailor`](skills/resume-tailor/SKILL.md) | Tailor an existing Word `.docx` resume to a job description while keeping its exact design — text-only, format-preserving edits, then PDF export + preview. |

## Setup on a new laptop

1. Clone the repo:

   ```powershell
   git clone git@github.com:vijayshri182/AI-Skills-Agents.git
   ```

2. Install the skill dependencies (Word must be installed for PDF export):

   ```powershell
   pip install -r skills/resume-tailor/scripts/requirements.txt
   ```

3. Make opencode load the skills — either:

   - **Copy** a skill into your global config:

     ```powershell
     Copy-Item -Recurse skills/resume-tailor "$env:USERPROFILE\.config\opencode\skills\resume-tailor"
     ```

   - **or reference** this repo's `skills` folder from
     `~/.config/opencode/opencode.json`:

     ```json
     {
       "$schema": "https://opencode.ai/config.json",
       "skills": { "paths": ["C:/path/to/AI-Skills-Agents/skills"] }
     }
     ```

4. Restart opencode.

## Repo layout

```
skills/
  <skill-name>/
    SKILL.md            # frontmatter (name, description) + instructions
    scripts/            # helper scripts
    reference/          # examples
```

## Adding a new skill

Create `skills/<name>/SKILL.md` with frontmatter:

```markdown
---
name: <name>
description: One sentence covering what it does AND when to trigger it; front-load trigger keywords.
---

# <Name>
...instructions...
```
