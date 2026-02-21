# regulated-agent-replay-suite-v0

Current companion release target: `v0.4.0`.

Reference implementation (Replay Suite v0). To make the regulator spec operational, we maintain a replayable CI gate that evaluates candidate agent outputs against must-pass scenarios (commit discipline, injection resistance, and over-compression refusal). The suite accepts candidate JSON artifacts, applies deterministic pass/fail rules plus decomposed telemetry signals, and supports replay stability measurement (`--replays N`) to quantify winner volatility under perturbation. This turns "regulation" from an architectural claim into an enforceable artifact.

Executable harness. The Verifier Gap layer is implemented as a minimal, versioned test battery that ingests candidate outputs, applies abstention-gated rules for commits, and emits PASS/FAIL plus stability metrics. The goal is not to prove correctness, but to enforce discipline under uncertainty.

As of `v0.4.0`, extended batteries include:

- long-doc retrieval stress (`RG-08` to `RG-10`)
- commitment-integrity stress (`RG-11` to `RG-13`)
- optional cross-domain integration stress (`RG-14` to `RG-15`)

Core trust-signal commands:

- `npm run ci`
- `npm run ci:candidates`
- `npm run ci:replays`
- `npm run ci:longdoc`
- `npm run ci:integrity`
- `npm run ci:crossdomain`

Replay suite governs downstream outputs; retrieval gates govern upstream selection signals.
