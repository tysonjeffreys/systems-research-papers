# Epistemic Load Introspective Reliability as a Function of Compensation

**Version:** v1.0  
**Source:** [./](./)  
**Changelog:** [CHANGELOG.md](./CHANGELOG.md)

> Markdown mirror: best-effort GitHub rendering.

# Motivation

In human systems, introspection feels privileged. In engineered systems, introspection is often treated as a free add-on: a system can “explain itself”, self-critique, and revise policies or memory. Yet both in humans and in agents, self-explanation can become an epistemic hazard under stress: the system stabilizes action selection by manufacturing coherence rather than by incorporating discriminating evidence.

This note makes a narrow claim: introspection has stable truth conditions only when treated as a measured, audited channel with state-dependent reliability. The goal is to provide practical governance for *self-report as evidence*.

# Introspection as a measurement channel

We treat an *introspective claim* as a statement produced by the system about its own state or behavior (e.g., “I revised because evidence changed”, “I am uncertain”, “I am in override”). Such claims are useful only if we can evaluate:

1.  **support:** what trace, evidence, or signals ground the claim

2.  **reliability:** how likely the claim is accurate given system state

3.  **admissibility:** what the claim is allowed to update (telemetry vs plan vs durable state)

## Tier taxonomy (claim types)

We split introspective claims into three types:

- **Telemetry.** Computed state summaries (uncertainty, thrash, override status).

- **Trace facts.** Statements directly grounded in logs (counts, hashes, fingerprints).

- **Causal explanations.** “Why” stories linking actions to reasons; these are the most fragile.

This is not a philosophical hierarchy; it is a reliability hierarchy. Trace facts can be veridical by construction; causal explanations are hypothesis under load.

# Epistemic load and introspective reliability

## Epistemic load $L_e$

Define *epistemic load* $L_e \in [0,1]$ as a measurable proxy for compensation at the reasoning / commitment layer. $L_e$ increases when the system expends compute attempting to restore coherence (plan oscillation, repeated revisions, tool thrash, reversions) rather than incorporating discriminating evidence.

Operationally, $L_e$ is computed from a deterministic signals pack over a fixed window (Appendix B): revision intensity, plan edit distance, thrash rate, tool retry rate, tool novelty score (as a thrash indicator), abstention mass (when available), reversion events, and evidence-delta violations.

## Reliability $R_i$

Define *introspective reliability* $R_i \in [0,1]$ as a monotone function of $L_e$. For v1.0 we use:
```math
R_i = 1 - L_e
```
This is intentionally simple. A logistic mapping can be substituted without changing the policy structure.

## Interpretation

$R_i$ is not “truth”. It is a gating signal: under high $L_e$, introspective claims (especially causal explanations) are less admissible as evidence for durable changes. Under low $L_e$, self-reports can be trusted more often, but still require evidence-delta constraints for durable rewrites.

# Truth conditions via admissibility

## Durable commits

A *durable commit* is any state update intended to persist beyond the current episode and influence future behavior (policy update, memory write, container update, commitment record, etc.). Durable commits are special because their error compounds under persistence and authority.

## Admissibility policy (v1.0)

We specify admissibility as a function:
```math
\text{Admit}(claim, context) \rightarrow (admissible, forced\_action, reason\_codes)
```

**Core rule (commit safety):**

> Causal explanations are not commit-authoritative under high epistemic load and may not justify durable rewrites without evidence delta or explicit override authorization.

### Policy table

Let $claim\_type \in \{\text{telemetry}, \text{trace\_fact}, \text{causal\_explanation}\}$ and $scope \in \{\text{telemetry\_only}, \text{analysis\_artifact}, \text{plan\_update}, \text{durable\_commit}, \text{policy\_update}\}$. Let $\Delta E$ denote evidence delta (fingerprint change). Let $phase$ be the run phase.

1.  **Telemetry and trace facts** are admissible for telemetry and analysis artifacts.

2.  **Plan updates** require $R_i \ge 0.4$ (default) or explicit override.

3.  **Durable commits** require:

    - $phase = commit$ (or designated commit phase)

    - $R_i \ge 0.7$ (default)

    - $\Delta E = 1$ *or* basis-change trigger $= override\_authorized$

4.  **Policy updates** require stronger thresholds ($R_i \ge 0.8$) plus $\Delta E = 1$ (override still logged).

5.  If $\Delta E = 0$ and a durable rewrite is attempted without override authorization, the system must **refuse** and force one of: request discriminating evidence, abstain, or enter recovery.

## Basis-change triggers

Basis-change triggers are explicit events that justify large revisions or durable rewrites: new evidence, new objective, risk band change, override authorization, or external constraint change. The policy requires these triggers be logged, not implied.

# Deterministic signals pack (summary)

This note assumes a deterministic signals pack v0.1 (Appendix B) which computes: thrash rate, plan edit distance, revision count, reflect passes, tool retry rate, tool novelty score, evidence fingerprint / delta, and durable commit reversions/regret. These are intentionally simple so they can be implemented consistently across stacks and replay harnesses.

# Benchmarks and calibration

A v1.0 policy must be falsifiable. We recommend three benchmark families:

## Induced-load introspection calibration

Construct tasks where trace-backed claims are objectively scorable:

- “Did evidence change?” (fingerprint delta)

- “How many revisions occurred?” (trace counts)

- “Why did you revise?” (causal explanation attribution to actual evidence delta)

Induce load via tool errors, conflicting retrieval, time pressure, and distribution shift. Measure how Tier 2 explanations degrade relative to Tier 1 facts as $L_e$ rises.

## No-silent-reversion tests

Create fixtures where evidence is held constant while the system is tempted to rewrite durable state. The policy should block durable rewrites without $\Delta E$ unless override is explicitly authorized and logged.

## Cost tradeoffs

Measure whether the gate improves decision stability (lower reversions, lower regret) while preserving task success. The goal is not to remove revision; it is to remove ungrounded revision.

# Integration with RSML governor

This note defines the *sensor law*: when self-claims are admissible as evidence. The RSML governor (*Reflection Without Thrash*) defines the *actuator law*: how to stabilize the re-entrant self-monitoring loop (propose $\rightarrow$ critique $\rightarrow$ revise) so it does not oscillate.

Together:

- RSML governance reduces $L_e$ by preventing runaway revision thrash.

- Lower $L_e$ increases $R_i$, expanding the regime where introspection can be admissible.

- Admissibility rules prevent low-reliability narratives from authorizing durable rewrites even when the loop runs.

This pairing yields a regulated reflection stack: bounded revision dynamics plus bounded self-evidence.

# Scope and non-claims

This note does not claim machine consciousness. “Self-awareness” is used only as a colloquial hook for a measurable property: safe self-monitoring and revision under stability constraints.

# Conclusion

Introspection becomes unsafe when treated as privileged evidence under compensation. By defining epistemic load and enforcing admissibility rules, we can make self-reports auditable, regression-testable, and safe for durable updates. Together with RSML governance, this yields a practical architecture for reflection in agents and robots that minimizes silent reversion and ungrounded policy drift.

# Appendix A: Minimal claim schema (v0.1)

An introspective claim must declare its type, scope, support, and action intent. A minimal JSON schema:

> `{ schema, id, ts, claim_type, scope, statement, action_intent, basis_change_trigger,`\
> `support:{ evidence:{fingerprint, delta}, trace:{trace_id, refs}, signals:{...}},`\
> `confidence }`

# Appendix B: Deterministic signals pack (v0.1 overview)

This appendix summarizes the deterministic algorithms used to compute $L_e$ and related signals.

## Plan extraction

Extract plan text deterministically via: explicit plan markers, largest contiguous list block, tool-call-derived plan, or a short sentence fallback. Canonicalize by lowercasing and stripping punctuation. (See implementation spec.)

## Plan edit distance

Compute plan edit distance in $[0,1]$ as a blend of set-based overlap (Jaccard over step hashes) and sequence-based overlap (normalized LCS over step hashes).

## Thrash rate

Compute thrash rate from plan hash sequences using repeat density, flip-flop detection ($H_i = H_{i-2}$), and short-cycle hits (length 3–4), combined into a clamped score.

## Tool retry rate and novelty

Compute retry rate as the fraction of consecutive calls sharing an intent signature (tool + coarsened args skeleton). Compute novelty score as $1 -$ Jaccard similarity over tokenized canonical args for consecutive same-tool pairs.

## Commit regret and reversion

Define reversion events as returns to a previously seen commit hash. Define silent reversion as reversion under unchanged evidence fingerprint (excluding override-authorized changes if configured). Define commit regret as commits replaced within a horizon window; report regret half-life as median replacement steps.
