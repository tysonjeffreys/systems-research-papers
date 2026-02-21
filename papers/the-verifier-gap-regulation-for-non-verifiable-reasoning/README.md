# The Verifier Gap (v0.1)

This paper names the verifier gap regime and defines a minimal regulation layer for non-verifiable reasoning systems.

This paper is a short bridge in the Baseline / regulation series. It names the "verifier gap" regime (selection without task-specific verifiers) and specifies a minimal **Verifier Gap Layer**:

- judge-as-sensor telemetry (do not treat learned critics/judges as authorities)
- abstain/tie mass and disagreement as first-class uncertainty signals
- band-limited candidate generation and bounded selection (tournaments / capped pairwise comparisons)
- commit gating for persistent writes (including representation/container updates)
- judge versioning, drift monitoring, and rollback/recovery semantics

## Artifacts
- Source: [main.tex](./main.tex)
- Mirror: [mirror.md](./mirror.md)
- Mirror audit: [mirror.audit.md](./mirror.audit.md)
- Changelog: [CHANGELOG.md](./CHANGELOG.md)
- Version: [VERSION](./VERSION)
- PDF (stable): [latest.pdf](./latest.pdf)
- PDF (manual named copy): `<paper-title> - vX.Y.Z.pdf`
