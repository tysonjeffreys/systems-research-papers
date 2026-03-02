# Regulated Reflection Fork Pair (Fork A + Fork B) — 2026-03-02

## Summary

This release pairs two companion notes that together define regulated reflection policy and implementation boundaries:

- Fork A: `papers/epistemic-load/` (`v1.0`)
- Fork B: `papers/reflection-without-thrash/` (`v0.1.1`)

## What changed

- Added new paper folder `papers/epistemic-load/` from the Prism project bundle.
- Added a short companion-note cross-link in Fork B to Fork A.
- Patch-bumped Fork B from `v0.1` to `v0.1.1` and propagated version references across paper surfaces.
- Updated top-level `README.md` to list both notes as a paired release and added Fork A to the artifacts table.
- Updated top-level `CHANGELOG.md` for this coordinated drop.

## Integration contract

- Fork B decides whether the system should keep revising.
- Fork A decides whether introspective claims can update durable state.
- Both depend on deterministic evidence-delta and reliability-linked telemetry.
