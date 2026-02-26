# Scope Closure + Basis-Change Framing - 2026-02-26

This release note captures a coordinated framing pass across six Prism papers.

## Scope

- Added explicit scope closure language: within base model scope (distribution + decoding + constraints), self-report is behavioral output and not authority.
- Added explicit basis-change trigger boundary: persistent state, side-effectful execution, policy/config updates, and delegated execution authority.
- Added operational implication language: commit-class gating, uncertainty telemetry prerequisites, and rollback/recovery semantics for durable actions.

## Papers and versions

- Regulatory Ground for Agentic AI: `v1.4.2`
- Phase Discipline for Regulated Agents: `v0.1.1`
- Critics-as-Sensors: `v0.1.1`
- The Time-to-Analysis Layer: `v1.2.1`
- The Verifier Gap: `v0.1.1`
- Concept Containers: `v1.3.1`

## Editing policy followed

- Additive insertions only; no section removals or structural refactors.
- `main.tex` and `mirror.md` were updated in lockstep for each affected paper.
- Patch-only version bumps were applied with dated per-paper changelog entries.

## Related repositories

- `regulated-agent-replay-suite` (downstream replay/commit discipline)
- `regulated-retrieval-gates` (upstream retrieval/selection telemetry and gating)
