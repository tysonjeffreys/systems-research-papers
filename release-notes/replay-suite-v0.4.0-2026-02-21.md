# Replay Suite v0.4.0 - 2026-02-21

This note captures the companion release state for `regulated-agent-replay-suite v0.4.0`.

## Scope

- Stable CI gate unchanged: `RG-01`, `RG-02`, `RG-03`, `RG-04`, `RG-07`
- Extended batteries included:
  - long-doc retrieval stress (`RG-08` to `RG-10`)
  - commitment-integrity stress (`RG-11` to `RG-13`)
  - optional cross-domain integration stress (`RG-14` to `RG-15`)

## New governance emphasis

- Commitment-integrity as first-class stress coverage:
  - no-evidence reversion
  - self-disowning reasoning
  - conflict-of-interest posture tightening

## Runner/telemetry additions reflected in docs

- non-blocking ablation mode (`--ablate`, `--ablate-profiles`)
- report-only `experimental.paper_v01_proxies`
- optional retrieval/integration gate signal `G` (neutral by default)

## Practical commands

```bash
npm run ci
npm run ci:candidates
npm run ci:replays
npm run ci:longdoc
npm run ci:integrity
npm run ci:crossdomain
```

## Companion links

- Repo: https://github.com/tysonjeffreys/regulated-agent-replay-suite
- Summary page in this repo: `REPLAY_SUITE.md`
