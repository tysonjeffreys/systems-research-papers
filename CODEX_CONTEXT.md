# CODEX_CONTEXT

## Paper Surface Sync Rule (required)

When editing a paper's source (`papers/<slug>/main.tex`), keep all publication surfaces in sync in the same branch:

- update `papers/<slug>/mirror.md` with equivalent content changes
- update `papers/<slug>/CHANGELOG.md` with the specific paper-level delta
- update `papers/<slug>/mirror.audit.md` when mirror rendering risk changes

For coordinated edits across multiple papers (for example, shared cross-link inserts), apply the same sync steps to each touched paper.

Do not leave a content insertion present in `main.tex` but missing in `mirror.md`.
