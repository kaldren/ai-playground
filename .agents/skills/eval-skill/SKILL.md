---
name: eval-skill
description: Evaluate a local Agent Skill from its evals/evals.json cases by running isolated with-skill and baseline trials, grading assertions, and producing an iteration benchmark. Use when the user invokes /eval-skill or asks to test or compare a skill's behavior.
---

# Evaluate an Agent Skill

Evaluate the target skill using its `evals/evals.json`. Perform the evaluation
with agents and file artifacts only; do not create a Python or shell evaluation
harness.

## Select the target

Treat the path or skill name following `/eval-skill` as the target. Resolve a
name by searching the current solution for a directory with that name that
contains both `SKILL.md` and `evals/evals.json`.

If no target is supplied, search the solution for `evals/evals.json` files. Use
the only match automatically; ask the user to choose when multiple matches make
the target ambiguous.

Validate before running:

- `skill_name` equals the target skill's frontmatter `name`.
- Every eval has a unique `id`, `prompt`, `expected_output`, and non-empty
  `assertions` list.
- Every path in `files` exists inside the target skill directory.

Report validation failures without changing the skill or eval definitions.

## Create the iteration

Create a workspace next to the target skill named `<skill-name>-workspace`.
Choose the next unused `iteration-N`; never overwrite an existing iteration.

Use this layout for every eval:

```text
<skill-name>-workspace/
└── iteration-N/
    ├── eval-<id>/
    │   ├── with_skill/
    │   │   ├── outputs/
    │   │   ├── timing.json
    │   │   └── grading.json
    │   └── without_skill/
    │       ├── outputs/
    │       ├── timing.json
    │       └── grading.json
    └── benchmark.json
```

## Run each eval

Use a fresh, isolated agent context for every trial. Run trials independently
when parallel agents are available. Do not expose one trial's messages or
outputs to another trial.

For `with_skill`, give the runner:

- The target `SKILL.md` and an explicit instruction to use it.
- The eval's `prompt` verbatim.
- The files listed by the eval.
- Its `outputs` directory as the required destination.

For `without_skill`, give a separate runner the same prompt, files, and output
destination, but do not mention, attach, summarize, or expose `SKILL.md`.

Do not reveal `expected_output` or `assertions` to either runner. Those fields
are grading criteria, not task instructions. Preserve each runner's actual
output; do not repair it before grading.

Record platform-reported measurements in `timing.json`:

```json
{
  "total_tokens": null,
  "duration_ms": null
}
```

Replace `null` only with measurements the platform actually reports. Never
estimate them.

## Grade each trial

Use a fresh grading agent that did not generate either output. Give it the
eval's `expected_output`, assertions, and one trial's output artifacts. Do not
identify whether the trial used the skill.

Require one result per assertion, preserving its text exactly. A pass requires
specific evidence from the output. Missing, ambiguous, or merely implied
evidence fails. Save:

```json
{
  "assertion_results": [
    {
      "text": "Original assertion",
      "passed": true,
      "evidence": "Specific evidence from the output"
    }
  ],
  "summary": {
    "passed": 1,
    "failed": 0,
    "total": 1,
    "pass_rate": 1.0
  }
}
```

Use direct mechanical inspection for objectively checkable properties such as
file existence, JSON validity, exact counts, or line limits. Count all lines,
including blank lines and fenced diagram source.

## Aggregate and report

Write `benchmark.json` containing mean pass rate for `with_skill` and
`without_skill`, plus the with-skill minus baseline delta. Include mean time and
tokens only when those measurements exist. Include standard deviation only
when at least two measured values exist; otherwise use `null`.

Report:

- The iteration directory.
- Passed assertions and pass rate for each configuration.
- The pass-rate delta and available cost delta.
- Assertion-level patterns that improved, regressed, or failed in both trials.
- Links to generated outputs, grades, and the benchmark.

Do not modify `SKILL.md`, `evals.json`, or input fixtures while evaluating. End
after reporting results so a human can review the artifacts before requesting
skill changes.
