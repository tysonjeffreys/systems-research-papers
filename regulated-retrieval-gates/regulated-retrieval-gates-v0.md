# regulated-retrieval-gates-v0

Companion retrieval-gate note aligned with replay-suite `v0.5.0` governance framing.

Operational reproducibility in this framework means replayability + traceability by default, with strict determinism only for contract-critical fields (labels, safety flags, structured report keys). Replayability means rerunning fixed-version inputs and reproducing candidate sets, selection outcomes (or distributions with tie/abstain mass), and posture decisions that controlled commit rights.

Traceability means every commit/withhold decision is inspectable: what evidence was retrieved, which constraints were active, which telemetry thresholds were crossed, and why abstention or commit was selected. This is the governance target for verifier-free domains, where correctness may be underdetermined but operating discipline is still enforceable.

Implementation companion: `regulated-retrieval-gates` provides deterministic scoring modules, telemetry, and abstention-gated commit decisions (`COMMIT_OK`, `COMMIT_CAUTION`, `ABSTAIN_GATHER`) with replayable benchmark reports.

Coherence in retrieval selection is a supported regime, not a forced choice. Stable selection requires sufficient evidence density, clear operator interpretation, adequate margins, and low contradiction mass.

Current telemetry focus includes:

- base selection signals: `margin`, `tieMass`, `contradictionMass`, `operatorErrorRate`
- commitment-integrity signals: `noEvidenceReversionRate`, `selfDisowningRate`, `incentiveConflictMass`
- basis-change signals: `basisChangeRisk`, `basisChangeRiskMass`

Support-deficit interpretation:

- high `tieMass` and/or low `margin` should be read as insufficient support, not model failure
- elevated `contradictionMass` indicates unstable causal structure for commit
- `ABSTAIN_GATHER` is the correct posture when support is insufficient: gather discriminating evidence, then rerun selection

v0.2+ opt-in phase-discipline additions:

- phase state support: `restore`, `transition`, `act`, `override`
- durable commit policy: durable commits allowed only in `transition`
- override recovery rule: commits remain blocked after `override` until recovery passes through `restore -> transition`
- deterministic audit field on decisions: `phasePolicy`
- exported helpers: `createPhaseManager`, `evaluateDurableCommitPolicy`

Long-doc retrieval stress suite coverage remains included (scope errors, causal dependence breaks, context sensitivity).

These retrieval signals are intended to tighten posture upstream of downstream write/commit rights managed by the replay suite.
