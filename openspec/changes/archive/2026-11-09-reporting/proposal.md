# Proposal

## Why

Users need to review individual recorded test outcomes after a suite run. Reporting provides a clear domain boundary for that review.

## What Changes

- Generate an independent report snapshot that lists the recorded results of a completed run without aggregation. Record each original prompt during execution so the snapshot can preserve it.
- Expose individual results, recorded expectation outcomes, and run metadata.
- Implement equivalent reporting behavior in TypeScript and Python, in that order. Python execution parity is a prerequisite for real integration.
- Keep HTTP, persistence and JSON export outside this change.

## Capabilities

### New Capabilities

- `reporting`: Generate reports from recorded suite runs.

### Modified Capabilities

None.

## Impact

New reporting domain contracts, classes and tests in both language implementations. TypeScript execution contracts already exist; Python execution integration depends on a separate prerequisite.
