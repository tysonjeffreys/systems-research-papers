# Epistemic Load: Introspective Reliability as a Function of Compensation

This paper defines introspection as a measured channel whose reliability depends on regulatory state, not as a privileged source of truth.

Core focus:
- Defines epistemic load (`L_e`) as a deterministic proxy for compensation at the reasoning and commit layer.
- Defines introspective reliability (`R_i`) as a monotone function of epistemic load.
- Specifies admissibility truth conditions for introspective claims by claim type and action scope.
- Enforces durable rewrite safety: no commit-authoritative causal self-explanations without evidence delta (or explicit override authorization).
- Connects policy to deterministic replay metrics and audit logs for falsifiable evaluation.

## Companion note
- [Reflection Without Thrash](../reflection-without-thrash/) defines RSML governor rails that stabilize revision loops.
- Epistemic Load (this note) defines whether introspective claims are admissible to update plans, artifacts, and durable state.

## Artifacts
- Source: [main.tex](./main.tex)
- Mirror: [mirror.md](./mirror.md)
- Mirror audit: [mirror.audit.md](./mirror.audit.md)
- Changelog: [CHANGELOG.md](./CHANGELOG.md)
- Version: [VERSION](./VERSION)
- Prism metadata: [prism.project.json](./prism.project.json)
- Figures: [figures/](./figures/)
