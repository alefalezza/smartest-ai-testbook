# Design

## Context

The domain design separates test creation, execution and reporting. TypeScript execution exists as a proof of concept; Python execution does not yet exist. See `doc/domain-design.md` and `doc/test-case-examples.md`.

## Goals / Non-Goals

**Goals:** Equivalent reporting in TypeScript and Python, using public contracts and recorded results.

**Non-Goals:** HTTP endpoints, persistence, JSON export, new evaluation algorithms and provider integrations. Recording the prompt in execution results is in scope. Python execution parity is a separately planned prerequisite for full integration.

## Decisions

- The application calls `IReportGenerator.generate(run)` separately after execution. The generator creates and returns an `IEvalReport`.
- The report is an independent snapshot: copy run metadata, each result and its scores, including original prompts, without retaining a reference to `IEvalRun` or its mutable collections. Do not aggregate results.
- Every TypeScript class implements a public interface; Python domain classes implement public `Protocol` contracts. Implement TypeScript first, then Python.
- No overall score, pass rate or aggregate count is computed. Each test and expectation retains its recorded outcome.

## Risks / Trade-offs

- Record the prompt in each result during execution, including failed model calls, so a later report never reads a changed test definition. The snapshot preserves the prompt template; substituted model input is not specified.
- Python integration cannot be verified against a real run until execution parity exists.
- `doc/requirements.md` mentions optional thresholds while the domain design requires one per expectation. Reconcile this wording before applying threshold-dependent rules.
