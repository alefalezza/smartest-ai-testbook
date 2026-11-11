# Tasks

## 1. Resolve prerequisites

- [x] 1.2 Reconcile the optional-threshold wording in requirements with the domain design's mandatory expectation threshold.

## 2. TypeScript reporting

- [x] 2.1 Define reporting interfaces and implement a report retaining the original run and its recorded results.
- [x] 2.2 Implement the report generator to expose each recorded result without aggregation.
- [x] 2.3 Test reporting mixed outcomes and an empty run without producing aggregates.
- [x] 2.4 Test reporting with failed expectations and execution errors; verify recorded details, no aggregation or repeated execution or evaluations.
- [x] 2.5 Run TypeScript tests and typecheck.

## 3. Python reporting

- [ ] 3.1 Plan and complete Python execution parity as a separate prerequisite, including real run, result and score contracts and behavior.
- [ ] 3.2 Implement equivalent Python reporting protocols and classes.
- [ ] 3.3 Test matching scenarios and integration with a real Python run; run the Python test suite.

## 4. Cross-language verification

- [ ] 4.1 Compare observable report fields, outcomes and boundary cases across both languages; update documentation for accepted decisions.

## 5. Report snapshots and original prompts

- [x] 5.1 Record the original prompt in each TypeScript execution result, including model failures.
- [x] 5.2 Replace the run reference in the report with a snapshot of run metadata, results, original prompts and scores; copy mutable collections and values.
- [x] 5.3 Verify snapshots remain unchanged after edits to the run, results, scores or test definition, and preserve prompts after failed model calls.
- [x] 5.4 Update domain documentation and diagrams to reflect report snapshots and recorded prompts, preserving the distinction from test versioning.
