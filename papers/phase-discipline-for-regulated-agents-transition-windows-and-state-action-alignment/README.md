# Phase Discipline for Regulated Agents (v0.1)

This paper introduces phase discipline as a runtime layer that schedules work classes (restore, transition, act) to reduce mismatch, thrash, and premature commits.

Core focus:
- Defines phase state and state-action alignment constraints.
- Adds transition windows for consolidation and gated commits.
- Composes phase control with global restraint posture signals.
- Proposes telemetry, metrics, and A/B validation patterns.

## Artifacts
- Source: [main.tex](./main.tex)
- Mirror: [mirror.md](./mirror.md)
- Mirror audit: [mirror.audit.md](./mirror.audit.md)
- Changelog: [CHANGELOG.md](./CHANGELOG.md)
- Version: [VERSION](./VERSION)
- PDF (stable): [latest.pdf](./latest.pdf)
- PDF (manual named copy): `<paper-title> - vX.Y.Z.pdf`
