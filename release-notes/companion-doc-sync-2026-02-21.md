# Companion Docs Sync - 2026-02-21

This note records documentation alignment updates after the replay-suite v0.4.0 companion changes.

## Regulated Agent Replay Suite

- Companion note refreshed to explicitly reference v0.4.0 scope.
- Coverage summary now includes:
  - long-doc retrieval stress (`RG-08` to `RG-10`)
  - commitment-integrity stress (`RG-11` to `RG-13`)
  - optional cross-domain integration stress (`RG-14` to `RG-15`)
- Trust-signal command list added (`ci`, `ci:candidates`, `ci:replays`, `ci:longdoc`, `ci:integrity`, `ci:crossdomain`).

## Regulated Retrieval Gates

- Companion note refreshed with current commitment-integrity telemetry:
  - `noEvidenceReversionRate`
  - `selfDisowningRate`
  - `incentiveConflictMass`
- Positioning clarified: retrieval telemetry tightens posture upstream of replay-suite commit rights.

## Repository Metadata

- Top-level README pointer now calls out v0.4.0 as the current harness release target.
- Top-level changelog includes this sync entry.
