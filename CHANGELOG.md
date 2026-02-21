# Changelog

All notable paper updates are documented here.

## 2026-02-21 (Companion Docs Sync)

- Updated companion notes for regulated-agent-replay-suite and regulated-retrieval-gates to reflect the v0.4.0 governance framing.
- Documented replay-suite extended batteries in companion docs: long-doc stress (RG-08 to RG-10), commitment-integrity stress (RG-11 to RG-13), and optional cross-domain stress (RG-14 to RG-15).
- Documented retrieval-gate commitment-integrity telemetry (noEvidenceReversionRate, selfDisowningRate, incentiveConflictMass) as posture-tightening signals.
- Added release note: release-notes/companion-doc-sync-2026-02-21.md.
- Added replay-suite release note: release-notes/replay-suite-v0.4.0-2026-02-21.md.

## 2026-02-17 (Backfill Release)

This is a semantic backfill release for pre-git paper edits. History is summarized per paper in `release-notes/`.

### Papers Updated

- Regulatory Ground (`v1.4.1`): operational reproducibility profile + replay-suite reference implementation.
- Verifier Gap (`v0.1`): retrieval-generation vs selection distinction, retrieval-gate artifact mapping, and reproducibility-without-verifiers language.
- Concept Containers (`v1.1`): abstention-gated container write discipline (`RG-07`) added near regulated writes.
- Critics-as-Sensors (`v0.1`): replay-gate implementation pointer and retrieval-gate analogue.
- Two-Regime Control (`v1.1` updated): phase-discipline commit-window language tied to telemetry-driven posture gating.

### Companion Notes Updated

- `regulated-agent-replay-suite-v0.md`
- `regulated-retrieval-gates-v0.md`
- `REPLAY_SUITE.md`

### Cross-Project Sync

- `regulated-agent-replay-suite` at `ed5b01a`
- `regulated-retrieval-gates` at `d1b6f2d`
- Full reconstructed backfill audit: `release-notes/reconstructed-change-log-2026-02-18.md`

See `release-notes/cross-project-sync-2026-02-17.md` for mapping details.
