from typing import Protocol

from smartest_ai_testbook.execution.eval_run import EvalScore
from smartest_ai_testbook.test_creation.expectation import IExpectation
from smartest_ai_testbook.test_creation.test_case import ITestCase


class Evaluator(Protocol):
    async def evaluate(self, test: ITestCase, output: str, expectation: IExpectation) -> EvalScore: ...


class ExactMatchEvaluator(Evaluator):
    async def evaluate(self, test: ITestCase, output: str, expectation: IExpectation) -> EvalScore:
        value = 1 if output == test.goldenReference else 0
        return EvalScore(
            value=value, scale_min=0, scale_max=1, passed=value >= expectation.threshold,
            feedback="Output matches the golden reference." if value == 1 else "Output does not match the golden reference.",
        )
