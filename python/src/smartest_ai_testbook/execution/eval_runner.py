from dataclasses import replace
from typing import Mapping, Protocol

from smartest_ai_testbook.execution.eval_run import EvalResult, EvalRun, EvalScore, IEvalResult, IEvalRun
from smartest_ai_testbook.execution.exact_match_evaluator import Evaluator
from smartest_ai_testbook.execution.model import Model
from smartest_ai_testbook.test_creation.test_case import ITestCase
from smartest_ai_testbook.test_creation.test_suite import ITestSuite


class IEvalRunner(Protocol):
    async def run(self, suite: ITestSuite, model: Model) -> IEvalRun: ...


class EvalRunner(IEvalRunner):
    def __init__(self, evaluators: Mapping[str, Evaluator]):
        self.evaluators = evaluators

    async def run(self, suite: ITestSuite, model: Model) -> IEvalRun:
        if not suite.tests:
            raise ValueError("Cannot run an empty suite.")
        run = EvalRun(suite.id, model.provider_name, model.model_name)
        for test in suite.tests:
            run.add_result(await self._run_test(test, model))
        return run

    async def _run_test(self, test: ITestCase, model: Model) -> IEvalResult:
        prompt = test.prompt
        try:
            output = await model.generate_response(prompt, test.variables)
        except Exception as error:
            return EvalResult(test.id, prompt, error=str(error))

        result = EvalResult(test.id, prompt, output)
        for expectation in test.expectations:
            metadata = dict(expectation_id=expectation.id, expectation_name=expectation.name,
                            evaluator_type=expectation.evaluator_type, threshold=expectation.threshold)
            try:
                if expectation.evaluator_type not in self.evaluators:
                    raise ValueError(f"Unknown evaluator type: {expectation.evaluator_type}")
                score = await self.evaluators[expectation.evaluator_type].evaluate(test, output, expectation)
                result.add_score(replace(score, **metadata, passed=score.error is None and score.value is not None and score.value >= expectation.threshold))
            except Exception as error:
                result.add_score(EvalScore(**metadata, passed=False, feedback="Evaluation failed.", error=str(error)))
        return result
