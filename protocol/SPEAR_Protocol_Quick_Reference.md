# SPEAR/0.2: Shared Pidgin for Expressive Abstraction and Requirements

SPEAR is a task-specification protocol for reducing residual intent ambiguity without forcing the human to describe the entire world.

## Core schema

```text
TASK
  Verb + target transformation or decision.

OBJECTS & TYPES
  Name important objects and state their types, units, domains, and interfaces.

AUTHORITY
  State who may decide or act, what requires approval, what is prohibited,
  and how a human may override. Capability is not permission.

ABSTRACTION
  PRESERVE: invariants and distinctions the answer must retain.
  IGNORE: degrees of freedom that may be discarded.
  ASSUME: idealizations, priors, operating regime, and “spherical cow” model.

OBJECTIVE
  Quantity or ordering to optimize; include trade-off weights when known.

CONSTRAINTS
  HARD: must never be violated.
  SOFT: preferences with penalties or priority order.

PRECEDENCE & VOCABULARY
  Order rules, exceptions, sources, and tie-breaks.
  Define canonical labels and semantic equivalents.

UNCERTAINTY
  What is unknown, estimated, disputed, or allowed to vary.

OUTPUT
  Required artifact, structure, audience, length, notation, and precision.

EVALUATION & CHECK
  Acceptance tests, metrics, counterexamples, tolerances, and failure conditions.
  Recheck constraints, sums, units, order, output shape, and authority.

INTERACTION / STOP
  Clarification policy: ask only when expected reduction in task loss exceeds query cost.
  Name hard gates and consequential actions that require a halt or approval.

EXAMPLES
  Positive examples, negative examples, and boundary cases.
```

## Compact mathematical objective

Let \(\Theta\) be latent intent, \(M\) the specification, \(C_H(M)\) its human production cost, and \(d(\Theta,\hat\Theta)\) task distortion. A task-optimal pidgin seeks a language and encoder minimizing

\[
\mathbb E[d(\Theta,\hat\Theta)]
+\lambda\,\mathbb E[C_H(M)]
+\gamma\,\mathbb E[C_{\mathrm{interaction}}],
\]

or, under a human cost budget \(B\), maximizing task-relevant mutual information

\[
\sup_{\mathbb E[C_H(M)]\le B} I(Z_T;M\mid C),
\]

where \(Z_T\) is the coarsest abstraction sufficient for the task.

## Example: systems optimization

```text
TASK
  Reduce anomaly-detector serving latency.

OBJECTS & TYPES
  Input: event stream, 1–5 million events/s.
  Output: anomaly score in [0,1] and optional alert flag.

AUTHORITY
  MAY: benchmark, profile, and draft a configuration.
  APPROVAL REQUIRED: deploy, change alert semantics, or spend money.

ABSTRACTION
  PRESERVE: recall on labeled critical incidents; event order within each source.
  IGNORE: exact score calibration when alert ordering is unchanged.
  ASSUME: current traffic mix and CPU-only deployment.

OBJECTIVE
  Minimize p99 end-to-end latency.

CONSTRAINTS
  HARD: recall >= 0.98; no event loss; memory <= 64 GB.
  SOFT: minimize cloud cost after latency target is met.

PRECEDENCE & VOCABULARY
  HARD constraints > latency objective > cost preference.
  Use p50, p95, p99, recall, and cost as canonical metric labels.

OUTPUT
  Ranked intervention plan plus estimated latency/cost effects.

EVALUATION & CHECK
  Replay benchmark on the supplied trace; report p50, p95, p99, recall, and cost.

INTERACTION / STOP
  Ask before changing the anomaly definition or dropping fields.
  STOP before deployment; deployment requires human approval.
```

## Example: mathematical abstraction

```text
TASK
  Estimate convective cooling time.

ABSTRACTION
  ASSUME: body is a sphere of radius R with uniform temperature T(t).
  PRESERVE: total heat capacity, exposed area, ambient temperature, convection coefficient.
  IGNORE: limbs, internal temperature gradients, radiation, and airflow anisotropy.

MODEL
  m c_p dT/dt = -h (4 pi R^2) (T - T_inf).

OUTPUT
  Closed-form T(t), characteristic time constant, and validity limits.
```

The abstraction is good only if it preserves the variables sufficient for the requested decision. Correct mathematics on the wrong quotient produces false precision.
