# Git Commit & Push Guide for Projects

Reusable workflow for committing and pushing an independent Git repository
to GitHub from the PowerShell terminal tool (runs as your OS user with your
machine's existing setup).

## 1. Prerequisites (already set up on this machine)

| Item | Value |
|---|---|
| Git identity | `user.name=Vish0624`, `user.email=vish0624@netcracker.com` |
| SSH key | `~/.ssh/id_ed25519` (public key added to the GitHub account) |
| Remote style | SSH URL: `git@github.com:<owner>/<repo>.git` |
| GitHub account (SSH) | `vijayshri182` (verify with `ssh -T git@github.com`) |

> The GitHub repo must already exist (create it first in the GitHub web UI).
> A web probe may return 404 for private repos; ssh `ls-remote` is the
> reliable way to confirm access: `git ls-remote origin`.

## 2. Verify the repo before committing

Open the shell **inside the repo directory** (else `git` resolves the wrong
top-level — the parent `C:\Vijay_GitHub` is the root of an unrelated repo):

```powershell
cd <path>\<your-repo>

git rev-parse --show-toplevel   # must be <path>\<your-repo>
git branch --show-current       # e.g. main
git remote -v                   # must be git@github.com:<owner>/<repo>.git
git status --short              # inspect changes
git diff --stat                 # review diffs
```

## 3. Stage ONLY the intended files

Never `git add .` blindly. Stage exactly what belongs in the commit:

```powershell
git add file1 file2 file3 ...
git diff --cached --stat                  # verify staged set
git diff --cached --name-status
```

Useful sanity checks before staging:

```powershell
git check-ignore credentials.json token.json .env .env.* .pem output/* 2>$null
# check-ignore prints matching ignored paths (expected: credentials.json, token.json, ...)
```

Always keep out of commits:
- `credentials.json`, `token.json`, `.env*`, `*.pem`, API keys, OAuth tokens
- generated output artifacts (e.g. `output/jobs.json`, `output/job_alert_report.md`)
- `__pycache__/`, `.pytest_cache/`, `.venv/`

## 4. Commit

```powershell
git commit -m "type: short summary"
```

Conventional prefixes used: `feat:`, `fix:`, `docs:`, `test:`, `chore:`.

If this is the first commit for a fresh repo and the author is wrong, re-author
the (unpushed) commit:

```powershell
git config user.name "Vish0624"
git config user.email "vish0624@netcracker.com"
git commit --amend --reset-author --no-edit
```

## 5. Push

```powershell
git push -u origin main
```

First push also sets branch tracking (`... set up to track 'origin/main'.`).

If a push ever hangs on an HTTPS credential prompt, switch the remote to SSH:

```powershell
git remote set-url origin git@github.com:<owner>/<repo>.git
```

For a fully non-interactive run (no prompts, no hangs):

```powershell
$env:GIT_SSH_COMMAND = "ssh -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=accept-new"
git push -u origin main
```

## 6. Verify after push

```powershell
git status          # working tree clean
git branch -vv      # main <hash> [origin/main] <message>
git log -1 --oneline
git remote -v
```

Successful push prints: `* [new branch] main -> main` and
`branch 'main' set up to track 'origin/main'.` (exit code 0).
Note: git writes progress to stderr, so PowerShell may render it in red —
check `$LASTEXITCODE`, not the console color.

## 7. Rules

- Work in the repo directory; never modify the parent `C:\Vijay_GitHub` repo's
  tracked content.
- Never stage or commit secrets, credentials, or generated outputs.
- Commit only the intended files; inspect `git diff --cached --stat` first.
- Do not commit or push automatically without an explicit request.