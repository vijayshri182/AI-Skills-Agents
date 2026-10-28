# Architecture: Central Skills Discovery & Installation

**Status:** Planned architecture (documentation only). No installer or cross-repo integration implemented in this work package.

## Vision
`AI-Skills-Agents` is the central source of truth for reusable AI-agent skills, instructions, guides, and workflows. Whenever work starts in any participating project repository, the agent should inspect the central skills catalogue, identify applicable skills, download or install them locally, validate them, and load the relevant instructions before proceeding with project work.

## A. Central Catalogue
- **Canonical location:** This repository (`AI-Skills-Agents`) holds reusable skills, guides, and workflows.
- **Manifest/catalogue:** A discoverable catalogue/manifest (to be added) will describe each skill's name, purpose, applicability, compatibility, dependencies, version, and installation location.
- **Distinction:** Skills (reusable task/instruction bundles), general reference guides (like the Git guide), and project-specific instructions are distinct categories.

## B. Project-Start Discovery
1. At project start, the agent inspects the central catalogue in `AI-Skills-Agents`.
2. It identifies skills relevant to the project's goals, technology, tools, and safety constraints.
3. It reports applicable, installed, missing, incompatible, or unavailable skills.
4. Discovery does not assume automatic activation.

## C. Local Installation
- **Target location:** Download applicable skills into a supported local project or agent skills directory (to be defined in conventions).
- **Validation:** Validate required files, integrity, version, dependencies, and compatibility before loading.
- **Preserve local changes:** Avoid overwriting local modifications without an explicit, safe update strategy.
- **Offline resilience:** Keep project work possible when the central repository is temporarily unavailable by reusing validated local copies.

## D. Loading and Use
- **Phases:** Discovery → Installation → Loading are distinct.
- **Precedence:** Agents must read applicable skill instructions before performing work.
- **Activation:** Downloading/installing a skill does not automatically make it discoverable or active; loading must be explicit per agent/runtime rules.

## E. Versioning and Updates
- **Tracking:** Record the version or commit of each installed skill.
- **Reproducibility:** Support reproducible installations and controlled updates.
- **Update detection:** Detect upstream changes and report available updates.
- **Conflict handling:** Preserve local project customizations and make conflicts visible (no silent overwrites).

## F. Safety and Precedence
- **Trust:** Treat downloaded skills as trusted only after appropriate validation.
- **Precedence:** Shared skills must never weaken stricter project safety rules, permissions, or authorization gates.
- **Secrets:** Never expose secrets or copy credentials into skills.
- **Authorization:** Require human authorization for destructive or externally consequential actions where applicable.
- **Fail safe:** Fail safely when the source, version, integrity, compatibility, or installation target is ambiguous.

## G. Incremental Rollout Plan
1. **Define format & conventions:** Skill format, naming, manifest schema, installation paths.
2. **Create catalogue/manifest:** Build discoverable catalogue describing skills.
3. **Define installation & version-pinning:** Rules for reproducibility and controlled updates.
4. **Build/test installer/updater:** Local mechanism with validation and conflict handling.
5. **Pilot integration:** Integrate project-start discovery into one pilot project.
6. **Validate:** Test loading, safety, reproducibility, and offline behavior.
7. **Roll out:** Extend to additional repositories using pilot lessons.

*No steps above are implemented in this work package.*

## Success Criteria
- A new project can discover relevant central skills without manual file-by-file searching.
- Applicable skills can be installed locally and reproducibly.
- Agents can discover and read installed skill instructions.
- Skill versions and installation outcomes are auditable.
- Project-specific safeguards take precedence.
- Updates do not silently overwrite local work.
- Other project repositories are not modified without an explicitly scoped integration task.

## Integration Notes
- Reference this architecture from project AGENTS/instructions at start of work.
- Consume via catalogue/manifest; do not duplicate skill content across projects.
- This document is the design record committed to `AI-Skills-Agents` as the single source of truth.
