# reporting Specification

## Purpose

Enable users to review individual recorded test outcomes for a completed suite run.

## Requirements

### Requirement: Generate a report from a completed run
The system SHALL generate an independent snapshot of a completed run without aggregating its results. The report SHALL contain copied run metadata and individual recorded results, including each original prompt, without retaining a reference to the run.

#### Scenario: Generate a report
- **WHEN** a completed run is supplied to the report generator
- **THEN** the report contains the run metadata and individual recorded results without an aggregate score or counts

#### Scenario: Original data changes after report generation
- **WHEN** the run, a result, a score or the test definition is modified after report generation
- **THEN** the report retains its original recorded contents, including the original prompt

### Requirement: Review results and failures
The report SHALL make the run metadata, original test prompts, individual results, output or errors, and expectation outcomes available for review.

#### Scenario: An expectation fails
- **WHEN** a run contains a failed expectation
- **THEN** the report identifies the expectation and its evaluator, recorded threshold, score and feedback or error
- **AND** it exposes the test as failed alongside the other recorded results

#### Scenario: Execution fails
- **WHEN** a test has an execution error
- **THEN** the report exposes that error and the test's failed outcome

### Requirement: Preserve recorded evaluations
Reporting SHALL use recorded results without running the model or repeating evaluations. Scores on different scales SHALL NOT be averaged directly.

#### Scenario: Review a recorded run
- **WHEN** a report is generated
- **THEN** each recorded evaluation remains available with its own score scale and outcome

### Requirement: Record the prompt used for each test
The execution subsystem SHALL record each test prompt with its result at execution time, including when model generation fails, so that later reports can preserve the original prompt.

#### Scenario: Test definition changes after execution
- **WHEN** a test prompt is edited after its execution and a report is subsequently generated
- **THEN** the report contains the prompt recorded for that execution
