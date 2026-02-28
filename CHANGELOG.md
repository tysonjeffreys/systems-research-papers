# Changelog

All notable paper updates are documented here.

## 2026-02-28 (Support-Invariant Cross-Paper Tightening)

- Added concise "coherence requires support" framing where it was still implicit, with additive edits only.
- Updated paper sources + mirrors:
  - `papers/baseline-regulation-and-global-constraint-signals-in-embodied-control-systems/`
  - `papers/why-intelligent-systems-waste-energy/`
  - `papers/toward-a-coherent-human-baseline/`
  - `papers/the-time-to-analysis-layer-pressure-points-in-ai-assisted-research-systems/`
- Updated companion docs:
  - `regulated-agent-replay-suite/regulated-agent-replay-suite-v0.md`
  - `regulated-retrieval-gates/regulated-retrieval-gates-v0.md`
  - `REPLAY_SUITE.md`
- Added release note: `release-notes/support-invariant-cross-paper-2026-02-28.md`.

## 2026-02-27 (Companion Docs Sync v0.5)

- Updated companion harness docs to reflect replay-suite `v0.5.0` scope.
- Documented optional frictionless-agency stress coverage (`RG-16` to `RG-21`) and opt-in friction metrics in:
  - `REPLAY_SUITE.md`
  - `regulated-agent-replay-suite/regulated-agent-replay-suite-v0.md`
  - `README_SNIPPET_HARNESS.md`
- Updated retrieval-gates companion note with opt-in phase discipline and durable commit policy details in:
  - `regulated-retrieval-gates/regulated-retrieval-gates-v0.md`
- Updated top-level README companion pointer to `v0.5.0`.
- Added release note: `release-notes/companion-doc-sync-2026-02-27.md`.

## 2026-02-27 (Frictionless Agency Onboarding)

- Added Frictionless Agency to the tracked paper index at `v0.1`.
- Added per-paper changelog entry: `papers/frictionless-agency/CHANGELOG.md` (`v0.1 - 2026-02-27`).
- Updated `README.md` paper summaries and artifacts table to include `papers/frictionless-agency/`.
- Added release note: `release-notes/frictionless-agency-v0.1-2026-02-27.md`.

## 2026-02-26 (Scope Closure + Basis-Change Framing)

- Added a coordinated framing update across six Prism papers: scope closure within LM mapping and basis-change triggers at the agentification boundary.
- Updated papers and versions:
  - Regulatory Ground (`v1.4.2`)
  - Phase Discipline (`v0.1.1`)
  - Critics-as-Sensors (`v0.1.1`)
  - Time-to-Analysis Layer (`v1.2.1`)
  - Verifier Gap (`v0.1.1`)
  - Concept Containers (`v1.3.1`)
- For each paper, updated both `main.tex` and `mirror.md` with additive insertions only, plus patch `VERSION` and per-paper `CHANGELOG.md` entries.
- Added release note: `release-notes/scope-closure-basis-change-2026-02-26.md`.

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
