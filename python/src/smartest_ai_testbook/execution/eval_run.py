from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol
from uuid import UUID, uuid4


@dataclass
class EvalScore:
    feedback: str
    passed: bool
    expectation_id: UUID | str | None = None
    expectation_name: str | None = None
    evaluator_type: str | None = None
    threshold: float | None = None
    value: float | None = None
    scale_min: float | None = None
    scale_max: float | None = None
    error: str | None = None


class IEvalResult(Protocol):
    test_id: UUID | str
    prompt: str
    output: str | None
    error: str | None
    scores: list[EvalScore]

    @property
    def passed(self) -> bool: ...
    def add_score(self, score: EvalScore) -> None: ...


class IEvalRun(Protocol):
    id: UUID
    suite_id: UUID | str
    started_at: str
    provider_name: str
    model_name: str
    results: list[IEvalResult]

    def add_result(self, result: IEvalResult) -> None: ...


class EvalResult(IEvalResult):
    def __init__(self, test_id: UUID | str, prompt: str, output: str | None = None, error: str | None = None):
        self.test_id = test_id
        self.prompt = prompt
        self.output = output
        self.error = error
        self.scores: list[EvalScore] = []

    def add_score(self, score: EvalScore) -> None:
        self.scores.append(score)

    @property
    def passed(self) -> bool:
        return self.error is None and self.output is not None and bool(self.scores) and all(score.passed for score in self.scores)


class EvalRun(IEvalRun):
    def __init__(self, suite_id: UUID | str, provider_name: str, model_name: str):
        self.id = uuid4()
        self.started_at = datetime.now(timezone.utc).isoformat()
        self.suite_id = suite_id
        self.provider_name = provider_name
        self.model_name = model_name
        self.results: list[IEvalResult] = []

    def add_result(self, result: IEvalResult) -> None:
        self.results.append(result)
