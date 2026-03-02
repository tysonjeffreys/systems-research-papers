# Reflection Without Thrash

**Version:** v0.1.1  
**Source:** [./](./)  
**Changelog:** [CHANGELOG.md](./CHANGELOG.md)

> Markdown mirror: best-effort GitHub rendering.
# Abstract

As agents become tool-using, persistent, and increasingly autonomous, developers naturally attempt to add “reflection”: self-critique, self-evaluation, iterative plan revision, and policy editing. In practice, this often produces a familiar failure cluster—oscillatory planning, revision spirals, tool thrash, silent reversion, and self-disowning reasoning—especially under uncertainty and distribution shift.

This note proposes a testable framing: “reflection” is a *re-entrant self-monitoring loop* (propose $\rightarrow$ critique $\rightarrow$ revise $\rightarrow$ re-critique). Like any feedback system, the loop has stability limits. When loop gain is high, delays are large, or evidence is noisy, self-monitoring becomes *compensation*: costly corrective contention that attempts to stabilize coherence through repeated revision. When the loop is explicitly regulated (gain limits, band limits, evidence-delta gating, phase discipline, durable commits, recovery half-life), it becomes a stable regime: *reflective coordination*.

We define observable failure signatures, propose a minimal governor that turns reflection into a regulated regime, and outline falsifiable evaluations for agents and robots. This note does *not* claim machine consciousness. It treats “self-awareness” as a colloquial pointer to an operational property: a system’s ability to safely evaluate and revise its own commitments without entering unstable correction cycles.

# Motivation: we modeled intelligence on the loudest layer

Modern AI and robotics stacks have historically emphasized competence: perception, prediction, planning, and action. Regulation has often been treated as an external patch (timeouts, filters, safety wrappers) rather than as a first-class layer. This posture scales task performance while leaving systems fragile under contradiction, novelty, and distribution shift—conditions that require safe revision.

The Baseline series frames this gap as a missing regulatory layer and formalizes a distinction between low-cost coordination regimes and high-cost compensation regimes. The same distinction applies to “reflection”. Reflection is not automatically a capability add-on. It is a control regime that must be stabilized.

# Re-entrant self-monitoring loops (RSML): the minimal mechanism

Define a re-entrant self-monitoring loop (RSML) as an internal process that repeatedly evaluates and modifies its own candidate plan or commitment:

1.  Propose a candidate plan $p_0$

2.  Critique $p_0$ under constraints and evidence

3.  Revise $\rightarrow p_1$

4.  Re-critique $p_1$

5.  Repeat until commit / abstain / escalate

This is a feedback loop. In the language of control:

- **Gain ($g$):** how strongly critique updates plans or commitments

- **Delay ($d$):** how late critique arrives relative to action and state change

- **Noise ($\sigma$):** instability in evidence and internal signals (retrieval variance, sensor noise, conflicting objectives)

A conceptual update rule:
```math
p_{t+1} = p_t + g \cdot U\big(\text{Critique}(p_t, E_t)\big)
```
where $E_t$ is the current evidence set (retrieval results, sensor frames, logs, constraints).

Stability is an engineering problem: as $g \uparrow$, $d \uparrow$, or $\sigma \uparrow$, the loop oscillates or diverges.

# When RSML destabilizes, it looks like “self-model amplification”

In unregulated agents, RSML instability produces a recognizable compensation cluster.

## Failure signatures (trace-level observables)

These are intentionally measurable; they belong in replay harnesses and regression suites.

(F1) Oscillatory planning  
Plans flip between a small set of alternatives.

(F2) Revision spirals / justification loops  
More compute spent explaining revisions than producing stable commitments.

(F3) Tool thrash  
Repeated tool calls with low novelty and small parameter perturbations.

(F4) Silent reversion under unchanged evidence  
A previously selected plan/commit is undone without a change in evidence.

(F5) Self-disowning reasoning  
Contradictions resolved by disowning prior commitments without new evidence (“ignore that”).

(F6) Over-reflection that blocks action  
The loop continues after thresholds are met.

## Regime interpretation: compensation vs coordination

A useful regime lens is: stable reflection corresponds to coordination at the planning layer; unstable reflection corresponds to compensation—costly corrective contention used to maintain coherence under instability. This is the cognitive analogue of replanning bursts, estimator churn, and gain escalation in embodied stacks.

# The governor: turning reflection into a regulated regime

A regulator-ground posture instantiates directly here: allow revision, but bound it. RSML is a primary place where unbounded optimization pressure appears.

## Governor rails (minimal viable spec)

Rail A — Evidence-delta gating  
Revisions that change durable commitments require a non-zero evidence delta or an explicit basis-change trigger. If evidence is unchanged, the system may annotate disagreement but not silently rewrite.

Rail B — Band-limited reflection  
Hard caps: max critique passes, max revisions, max tool retries per phase. Reflection is episodic, not continuous.

Rail C — Gain limiting  
Critique proposes bounded edits. Large changes require explicit triggers (new objective, new evidence, risk band change, override authorized).

Rail D — Convergence or abort  
Within budget, the loop must converge, abstain, or escalate. If none occurs: stop-right (safe-mode reflection end).

Rail E — Durable commit discipline  
Durable commits occur only in a designated phase and must be append-only with explicit rollback semantics (no silent edits).

Rail F — Recovery half-life  
After override or thrash, enforce cooldown before permitting new durable commits.

## Phase discipline (recommended)

A practical RSML state machine:
```math
\text{OBSERVE} \rightarrow \text{PROPOSE} \rightarrow \text{CRITIQUE} \rightarrow \text{RESOLVE} \rightarrow \text{COMMIT} \rightarrow \text{ACT}
```
with explicit detours:
```math
\text{OVERRIDE} \rightarrow \text{RECOVER}
```
This keeps reflection legible in traces and aligns reflection with durable commit semantics.

# Containers and critics: making reflection cheap and stable

Reflection is expensive if its outputs are transcripts. Reflection becomes efficient when its outputs are reusable causal structure.

## Concept containers as reflection’s commit object

When the loop stabilizes, it should commit a *container* (variables, relations, levers, falsifiers, scope, provenance) rather than a long deliberation trace. This amortizes the expensive synthesis and reduces future revision pressure.

## Critics-as-sensors: bounded selection prevents runaway reflection

When uncertainty is high, critic disagreement/abstention should trigger evidence escalation (retrieve or intervene), not more unbounded reflection. Treat critique as telemetry, not authority.

## Time-to-analysis: reflection must terminate in an analysis artifact

A stable reflection episode should terminate in an intervention-ready analysis artifact (causal skeleton, disagreements, levers, falsifiers, uncertainty boundaries), not merely longer text.

# Robotics instantiation: RSML as cognitive compensation

In embodied stacks, compensation can be measured and regulated with a slow baseline regulator. RSML is the planning analogue. Define a reflection-compensation index using measurable terms such as: plan edit distance, critique pass rate, tool retry rate, evidence delta rate, and commit regret.

The governor’s job is not to eliminate reflection. It is to reduce sustained residence in high compensation and to force safe termination: converge / abstain / escalate.

# Falsifiable evaluations

## Experiment A: induced contradiction with persistent update

Tasks require the agent to represent a contradiction, gather discriminating evidence, and update a durable commitment such that future behavior changes predictably. Score: reversal count, evidence-delta consistency, commit regret, bounded compute.

## Experiment B: tool-use under perturbation

Inject tool errors, partial results, and adversarial noise mid-loop. Measure: tool thrash rate, convergence time, unsafe action attempts, rollback success.

## Experiment C: robotics sim-to-real with replanning churn

Induce distribution shift (latency/noise/contact uncertainty). Measure: replanning bursts, estimator churn, reflection-compensation index, and recovery time.

## Negative tests (falsifiers)

This framing weakens if stabilization reduces reflection signals but does not reduce reversals/commit regret; or if constraints reduce instability but degrade task success unacceptably; or if stable reflection emerges without evidence-delta gating and band limits.

# What this note claims and does not claim

**Claims (operational):** reflection is a re-entrant control loop with stability limits; failure signatures are measurable; a governor can reduce thrash and improve durable commit stability.

**Non-claims:** no theory of consciousness is required; no claim that current systems are sentient; “self-awareness” is used only as a colloquial hook for re-entrant self-monitoring behavior.

# Conclusion

As autonomy, persistence, and tool access increase, agent systems will increasingly need to revise plans and commitments under contradiction. Unregulated reflection often becomes compensation: oscillation, thrash, and silent reversion. A minimal governor—evidence-delta gating, band-limited reflection, phase discipline, durable commits, rollback, and recovery—turns reflection into a regulated control mode that can be evaluated, regression-tested, and shipped.

# Implementation companions

This hub note maps directly to two implementation companions:

- `regulated-agent-replay-suite/replay-suite/v0/rsml-stability-stress.json` for RSML stress scenarios and replay checks.

- `regulated-retrieval-gates` RSML governor rails for evidence-delta gating and phase-scoped durable commit control.

# Companion note

`papers/epistemic-load/` defines admissibility truth conditions for introspective claims and durable rewrites under epistemic load. Reflection Without Thrash (this note) governs revision-loop stability. In operational terms: Reflection Without Thrash decides whether revision should continue; Epistemic Load decides whether a self-claim can update durable state.

# Appendix A: Minimal RSML telemetry schema

- `reflect_passes`

- `revision_count`

- `plan_edit_distance`

- `evidence_fingerprint` + `evidence_delta`

- `tool_retry_rate` + `tool_novelty_score`

- `thrash_rate` (cycle/oscillation)

- `commit_hash` + `commit_regret`

- `convergence_score` (trend over window)

- `band` (risk/operating band)

# Note on authorship and tools

This work was developed through iterative reasoning, modeling, and synthesis. Large language model tools were used as a collaborative aid for drafting, editing, and cross-domain translation. All conceptual framing, structure, and final judgments remain the responsibility of the author.
