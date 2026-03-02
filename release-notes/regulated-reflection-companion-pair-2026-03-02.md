# Regulated Reflection Companion Pair (Epistemic Load + Reflection Without Thrash) — 2026-03-02

## Summary

This release pairs two companion notes that together define regulated reflection policy and implementation boundaries:

- `papers/epistemic-load/` (`v1.0`)
- `papers/reflection-without-thrash/` (`v0.1.1`)

## What changed

- Added new paper folder `papers/epistemic-load/` from the Prism project bundle.
- Added a short companion-note cross-link from Reflection Without Thrash to Epistemic Load.
- Patch-bumped Reflection Without Thrash from `v0.1` to `v0.1.1` and propagated version references across paper surfaces.
- Updated top-level `README.md` to list both notes as a paired release and added Epistemic Load to the artifacts table.
- Updated top-level `CHANGELOG.md` for this coordinated drop.

## Integration contract

- Reflection Without Thrash decides whether the system should keep revising.
- Epistemic Load decides whether introspective claims can update durable state.
- Both depend on deterministic evidence-delta and reliability-linked telemetry.
