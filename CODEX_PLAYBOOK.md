# Baseline Papers — Codex Playbook (Prism-first authoring, Git-first publishing)

## Non-negotiables
- Treat this repo as the **source-of-truth** for paper sources + release metadata.
- `main` is **published-only**. All work happens on branches and is merged only when ready to release.
- Folder names are **stable identifiers** (no version numbers in folder names).
- Versions live in: git tags + per-paper VERSION file + changelogs + release notes.
- Keep Prism/LaTeX sources clean: do NOT commit build junk.
- If editing any code repos (e.g., regulated-agent-replay-suite / regulated-retrieval-gates), read and follow `DEV_RULES_FOR_CHATGPT.md` first. Do not refactor or remove functionality unless explicitly instructed.

---

## Repo structure (target)
baseline-papers/
  papers/
    <paper-slug>/
      main.tex
      README.md
      CHANGELOG.md
      VERSION
      figures/ (optional)
      refs.bib (optional)
      latest.pdf                # stable convenience artifact (committed)
      mirror.md                 # stable GitHub-readable mirror (best-effort)
      mirror.audit.md           # mirror rendering audit (best-effort)
      releases/
        <paper-slug>-vX.Y.Z.pdf # immutable versioned artifact (copy of latest.pdf)
        <paper-slug>-vX.Y.Z.md  # immutable versioned artifact (copy of mirror.md)
        README.md               # optional index for releases/
  release-notes/
    <tag>.md                    # e.g. why-energy-v1.1.0.md
  CHANGELOG.md                  # repo-level, links to per-paper entries
  PUBLISHING.md
  README.md
  .gitignore
  tools/
    generate-paper-mirrors.mjs

---

## Tag + branch naming
- Branch: `paper/<paper-slug>/vX.Y.Z`
- Tag: `<short-slug>-vX.Y.Z` (example: `why-energy-v1.0.0`)
  - Maintain a mapping of paper-slug → short-slug in README.md (or decide short-slug = paper-slug if you want zero mapping).

---

## ONE-TIME MIGRATION TASKS (run once)

### 0) Safety
- Ensure working tree is clean before starting.
- Create a migration branch:
  - `git checkout -b chore/repo-restructure`

### 1) Add .gitignore to stop build-junk churn
Create/update `.gitignore` to ignore LaTeX/Prism outputs but NOT ignore `latest.pdf`.

Recommended patterns:
- LaTeX aux:
  *.aux
  *.bbl
  *.bcf
  *.blg
  *.fdb_latexmk
  *.fls
  *.log
  *.out
  *.run.xml
  *.synctex.gz
  *.toc
  *.lof
  *.lot
  *.nav
  *.snm
  *.vrb
- Common build dirs:
  build/
  out/
  dist/
- Keep committed convenience PDF:
  !**/latest.pdf

NOTE:
- If your paper folders currently contain `main.pdf` or `source.pdf`, those should generally be treated as build output and ignored/removed from tracking.

### 2) Untrack build junk already committed
If any ignored files are currently tracked:
- `git rm --cached -r -- <paths>`
- Do NOT delete sources (main.tex, figures, bib).
- Goal: after this, `git status` should not show build artifacts as tracked.

### 3) Create new stable folder layout
- Create folders: `papers/`, `release-notes/`, `tools/` if missing.

### 4) Rename/move each paper folder into papers/<paper-slug>/
Current folders are named like:
- `v1.0 - Why Intelligent Systems Waste Energy`

Target:
- `papers/why-intelligent-systems-waste-energy`

Rules for slugging:
- Remove leading version prefix (`vX.Y`, `vX.Y.Z`, `vX.Y_...`).
- Lowercase.
- Replace spaces/underscores with hyphens.
- Remove punctuation except hyphens.

For each paper folder moved:
- Ensure it contains:
  - `main.tex`
  - `README.md` (create if missing)
  - `VERSION` (create if missing)
  - `CHANGELOG.md` (create if missing)
  - `latest.pdf` (create via copy from an existing exported PDF if present)

### 5) Create VERSION + CHANGELOG.md per paper
Inside each `papers/<slug>/`:
- `VERSION` contains only `X.Y.Z` (example: `1.0.0`)
- `CHANGELOG.md` starts with:
  - Paper title
  - Current version line
  - Entries (newest first)

Template (per paper CHANGELOG.md):
- # <Paper Title>
- Current: vX.Y.Z
- ## vX.Y.Z — YYYY-MM-DD
  - Bullet changes…

### 6) Standardize latest.pdf
Inside each `papers/<slug>/`:
- Identify the most recent exported PDF currently present (often named with version + title).
- Copy it to `latest.pdf`.
- Do not keep multiple PDFs tracked in git. Only commit `latest.pdf`.
  (Older version PDFs should live in GitHub Releases, not the repo.)

### 7) Build Markdown mirrors inside each paper folder
For each paper:
- Create `papers/<paper-slug>/mirror.md` (best-effort, preserves math as LaTeX)
- Create `papers/<paper-slug>/mirror.audit.md` (flags macro/command risks for GitHub rendering)
- Create `papers/<paper-slug>/releases/` and place immutable, versioned copies:
  - `<paper-slug>-vX.Y.Z.md`
  - `<paper-slug>-vX.Y.Z.pdf` (requires latest.pdf to exist)
Preferred method:
- Run `node tools/generate-paper-mirrors.mjs`

### 8) Repo-level README index + CHANGELOG
- `README.md` should list each paper:
  - Title
  - Current version (read from VERSION file)
  - Links:
    - Prism source folder
    - latest.pdf
    - mirror.md
    - per-paper CHANGELOG.md

- `CHANGELOG.md` (repo-level) should include:
  - Release/date entries
  - For each entry: list papers changed and link to the relevant per-paper changelog section.

### 9) Relocate harness/gates writeups
If this repo currently contains folders like `regulated-agent-replay-suite/` or `regulated-retrieval-gates/` that are only markdown notes:
- Move those notes to the appropriate code repos (preferred), OR
- Replace them here with minimal “pointer docs” under `docs/` that link to the code repos.
In this papers repo, keep only:
- paper sources
- release notes
- index/changelogs
- lightweight references/links

### 10) Commit the migration
- `git add -A`
- `git commit -m "Restructure repo: stable paper slugs, VERSION/CHANGELOG, md mirrors, ignore build junk"`
- Open PR / merge into main only when verified.

---

## EVERY-TIME WORKFLOW (for any paper update)

### 1) Create a branch
- `git checkout main`
- `git pull`
- `git checkout -b paper/<paper-slug>/vX.Y.Z`

### 2) Update version + changelogs FIRST
In `papers/<paper-slug>/VERSION`:
- set new version (X.Y.Z)

In `papers/<paper-slug>/CHANGELOG.md`:
- add a new top entry:
  - `## vX.Y.Z — YYYY-MM-DD`
  - bullets of changes

In repo-level `CHANGELOG.md`:
- add an entry referencing the paper + linking to per-paper changelog

### 3) Edit paper sources (Prism/LaTeX)
- Modify `papers/<paper-slug>/main.tex` and related assets as instructed.
- Do not remove sections or functionality unless explicitly instructed.
- Keep formatting consistent with existing paper style.

### 4) Generate/update mirror.md + audit + versioned release artifacts
Run:
- `node tools/generate-paper-mirrors.mjs`

This will:
- write `papers/<slug>/mirror.md`
- write `papers/<slug>/mirror.audit.md`
- create immutable `papers/<slug>/releases/<slug>-vX.Y.Z.md` if missing
- create immutable `papers/<slug>/releases/<slug>-vX.Y.Z.pdf` if `latest.pdf` exists and versioned PDF is missing

### 5) Human-in-the-loop: export PDF from Prism
STOP and ask the user to:
- Open Prism project at `papers/<paper-slug>/`
- Export PDF
- Save/overwrite: `papers/<paper-slug>/latest.pdf`

After the user exports:
- Verify `latest.pdf` file timestamp changed (or file hash changed).
- Re-run `node tools/generate-paper-mirrors.mjs` so the versioned PDF copy is created in `papers/<slug>/releases/`.

### 6) Cleanliness check
- `git status` should show only meaningful changes:
  - main.tex, VERSION, CHANGELOG.md, mirror.md, mirror.audit.md, latest.pdf, and new `releases/<slug>-vX.Y.Z.*` files
- There should be no build junk tracked. If present, add ignore rules or remove from tracking.

### 7) Commit
Commit message format:
- `<Paper Title>: vX.Y.Z`

Example:
- `Why Intelligent Systems Waste Energy: v1.1.0`

### 8) Merge to main (published-only discipline)
- Open a PR (preferred) or merge locally:
  - `git checkout main`
  - `git merge --no-ff paper/<paper-slug>/vX.Y.Z`
- `main` must remain publishable at all times.

### 9) Tag + push
- Create tag:
  - `git tag -a <short-slug>-vX.Y.Z -m "<Paper Title> vX.Y.Z"`
- Push branch + tag:
  - `git push`
  - `git push --tags`

### 10) GitHub Release
Create a GitHub Release for the tag with:
- Release notes copied from:
  - `release-notes/<tag>.md` (create/update this file)
- Assets:
  - `papers/<paper-slug>/releases/<paper-slug>-vX.Y.Z.pdf`
  - `papers/<paper-slug>/releases/<paper-slug>-vX.Y.Z.md`
  - (optional) `papers/<paper-slug>/latest.pdf`

---

## Mirror policy
- PDF is canonical; `mirror.md` is best-effort for GitHub readability.
- `mirror.audit.md` lists math commands and rendering-risk signals that may differ from PDF output.
- Never overwrite existing files in `papers/<slug>/releases/` unless explicitly instructed.

---

## Batch updates (multiple papers at once)
If updating multiple papers in one coordinated drop:
- Either:
  - one branch per paper (cleanest history), or
  - one batch branch `release/YYYY-MM-DD` (fastest).
If batch branch is used:
- Still update VERSION + per-paper changelog per paper.
- Still tag per-paper tags when releasing.

---

## Definition of Done (DoD) for any release
- `main` contains:
  - updated sources
  - updated VERSION
  - updated per-paper CHANGELOG
  - updated mirror.md
  - updated mirror.audit.md
  - versioned artifacts exist in `releases/` for the bumped version:
    - `<slug>-vX.Y.Z.pdf`
    - `<slug>-vX.Y.Z.md`
  - updated latest.pdf
  - updated repo CHANGELOG
- Tag exists and points at `main`.
- GitHub Release exists with PDF attached and release notes.
- Never overwrite existing files in `papers/<slug>/releases/` unless explicitly instructed.
