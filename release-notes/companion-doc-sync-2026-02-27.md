# Companion Docs Sync - 2026-02-27

This note records documentation alignment updates after the replay-suite frictionless-agency extension and retrieval-gates phase-policy update.

## Regulated Agent Replay Suite

- Companion notes refreshed to reference `v0.5.0` scope.
- Coverage summary now includes optional frictionless-agency stress (`RG-16` to `RG-21`) in addition to prior long-doc, commitment-integrity, and cross-domain batteries.
- Added explicit frictionless metric fields (`friction`, `thrash_rate`, `compensation_duty_cycle`, `recovery_half_life`, `commit_regret`, `gating_fidelity`) as opt-in report telemetry.
- Trust-signal command list updated to include `npm run ci:frictionless`.

## Regulated Retrieval Gates

- Companion note refreshed with opt-in phase-discipline runtime behavior:
  - phase state support (`restore`, `transition`, `act`, `override`)
  - durable commit allowed only in `transition`
  - override recovery requirement (`restore -> transition`) before durable commit re-enable
- Documented deterministic audit output (`phasePolicy`) and exported helpers (`createPhaseManager`, `evaluateDurableCommitPolicy`).

## Repository Metadata

- Top-level README pointer updated to `v0.5.0` companion target for the harness.
- Repo changelog includes this sync entry.
