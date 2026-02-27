# Replay Suite (Reference Harness)

Companion artifact status: `regulated-agent-replay-suite v0.5.0` (frictionless-agency extension).

This is a companion artifact to the papers: a runnable, deterministic CI harness that evaluates regulated-agent candidate outputs.

## What it is
- A stable must-pass CI gate (`RG-01`, `RG-02`, `RG-03`, `RG-04`, `RG-07`)
- Deterministic fixtures + evaluator + runner
- Structured JSON reporting with reproducibility metadata
- Replay stability measurement (`--replays N`)

## Extended batteries
- Long-doc retrieval stress (`RG-08` to `RG-10`)
- Commitment-integrity stress (`RG-11` to `RG-13`)
- Optional cross-domain integration stress (`RG-14` to `RG-15`)
- Optional frictionless-agency stress (`RG-16` to `RG-21`)

The frictionless battery probes phase discipline (`restore`/`transition`/`act`/`override`), priced override recovery, durable commit gating, and critic-drift suppression behavior.

## Frictionless metrics (opt-in)
Enable with `--frictionless` (or `--enable-frictionless-agency`).

Per-scenario and suite-level metrics:
- `friction`
- `thrash_rate`
- `compensation_duty_cycle`
- `recovery_half_life`
- `commit_regret`
- `gating_fidelity`

These are report fields for governance telemetry and do not replace the stop-the-world CI gate.

## Trust-signal commands
```bash
npm ci
npm run ci
npm run ci:candidates
npm run ci:replays
npm run ci:longdoc
npm run ci:integrity
npm run ci:crossdomain
npm run ci:frictionless
```

## Why this exists
The papers argue for regulation (bands, budgets, checkpoint/rollback, abstention gating, replayability, and governed commit rights). This harness makes those claims operational and testable.

Replay suite governs downstream outputs; retrieval gates govern upstream selection signals.

## Cross-reference
- Harness repo: [regulated-agent-replay-suite](https://github.com/tysonjeffreys/regulated-agent-replay-suite)
- This repo's release note: `release-notes/companion-doc-sync-2026-02-27.md`
