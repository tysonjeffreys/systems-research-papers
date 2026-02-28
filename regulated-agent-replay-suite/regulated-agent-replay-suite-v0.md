# regulated-agent-replay-suite-v0

Current companion release target: `v0.5.0`.

Reference implementation (Replay Suite v0). To make the regulator spec operational, we maintain a replayable CI gate that evaluates candidate agent outputs against must-pass scenarios (commit discipline, injection resistance, and over-compression refusal). The suite accepts candidate JSON artifacts, applies deterministic pass/fail rules plus decomposed telemetry signals, and supports replay stability measurement (`--replays N`) to quantify winner volatility under perturbation. This turns "regulation" from an architectural claim into an enforceable artifact.

Executable harness. The Verifier Gap layer is implemented as a minimal, versioned test battery that ingests candidate outputs, applies abstention-gated rules for commits, and emits PASS/FAIL plus stability metrics. The goal is not to prove correctness, but to enforce discipline under uncertainty.

Coherence in commit behavior is a supported regime. In this harness, support means evidence sufficiency, stable selection margins, and replay-stable abstention/tie behavior under perturbation.

Operationally: low support -> abstain -> gather evidence -> rerun. Commit rights are restored only when support recovers.

As of `v0.5.0`, extended batteries include:

- long-doc retrieval stress (`RG-08` to `RG-10`)
- commitment-integrity stress (`RG-11` to `RG-13`)
- optional cross-domain integration stress (`RG-14` to `RG-15`)
- optional frictionless-agency stress (`RG-16` to `RG-21`)

Frictionless suite additions (opt-in):

- phase discipline checks (`restore`, `transition`, `act`, `override`)
- override commit-tightening and mandatory recovery checks
- durable commit gating checks outside Transition
- abstention-mass and recovery-bound expectation checks
- report metrics: `friction`, `thrash_rate`, `compensation_duty_cycle`, `recovery_half_life`, `commit_regret`, `gating_fidelity`

Core trust-signal commands:

- `npm run ci`
- `npm run ci:candidates`
- `npm run ci:replays`
- `npm run ci:longdoc`
- `npm run ci:integrity`
- `npm run ci:crossdomain`
- `npm run ci:frictionless`

Replay suite governs downstream outputs; retrieval gates govern upstream selection signals.
