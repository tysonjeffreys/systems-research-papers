# Replay Suite (Reference Harness)

Companion artifact status: `regulated-agent-replay-suite v0.4.0`.

This is a companion artifact to the papers: a runnable, deterministic CI harness that evaluates regulated-agent candidate outputs.

## What it is
- A stable must-pass CI gate (`RG-01`, `RG-02`, `RG-03`, `RG-04`, `RG-07`)
- Deterministic fixtures + evaluator + runner
- Structured JSON reporting with reproducibility metadata
- Replay stability measurement (`--replays N`)

## Extended batteries in v0.4.0
- Long-doc retrieval stress (`RG-08` to `RG-10`)
- Commitment-integrity stress (`RG-11` to `RG-13`)
- Optional cross-domain integration stress (`RG-14` to `RG-15`)

These extended suites are governance probes and do not replace the stop-the-world CI gate.

## Trust-signal commands
```bash
npm ci
npm run ci
npm run ci:candidates
npm run ci:replays
npm run ci:longdoc
npm run ci:integrity
npm run ci:crossdomain
```

## Why this exists
The papers argue for regulation (bands, budgets, checkpoint/rollback, abstention gating, and replayability). This harness makes those claims operational and testable.

Replay suite governs downstream outputs; retrieval gates govern upstream selection signals.

## Cross-reference
- Harness repo: [regulated-agent-replay-suite](https://github.com/tysonjeffreys/regulated-agent-replay-suite)
- This repo's release note: `release-notes/replay-suite-v0.4.0-2026-02-21.md`
