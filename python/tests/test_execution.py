import asyncio
import unittest

from smartest_ai_testbook.execution.eval_run import EvalResult, EvalScore
from smartest_ai_testbook.execution.eval_runner import EvalRunner
from smartest_ai_testbook.execution.exact_match_evaluator import ExactMatchEvaluator
from smartest_ai_testbook.test_creation.expectation import Expectation
from smartest_ai_testbook.test_creation.test_case import TestCaseBuilder as CaseBuilder
from smartest_ai_testbook.test_creation.test_suite import TestSuite as Suite


class Model:
    provider_name = "Test provider"
    model_name = "Test model"

    def __init__(self):
        self.calls = []

    async def generate_response(self, prompt, variables):
        self.calls.append((prompt, variables.copy()))
        if prompt == "Fail":
            raise ValueError("Model unavailable")
        return "Paris"


class FailingEvaluator:
    async def evaluate(self, test, output, expectation):
        raise ValueError("Judge unavailable")


class PartialEvaluator:
    async def evaluate(self, test, output, expectation):
        await asyncio.sleep(0)
        return EvalScore(value=0.5, scale_min=0, scale_max=1, passed=True, feedback="Partial")


def make_test(prompt, expectations):
    builder = CaseBuilder().set_prompt(prompt).set_golden_reference("Paris")
    for expectation in expectations:
        builder.add_expectation(expectation)
    return builder.build()


class ExecutionTests(unittest.TestCase):
    def test_execution_and_error_isolation(self):
        exact = Expectation("Exact", "exactMatch", 1, {})
        unknown = Expectation("Unknown", "unknown", 1, {})
        failing = Expectation("Judge", "failing", 1, {})
        suite = Suite("Answers")
        suite.add_test(make_test("Fail", [exact]))
        test = make_test("Return {{city}}", [unknown, failing, exact])
        test.variables["city"] = "Paris"
        suite.add_test(test)
        model = Model()
        run = asyncio.run(EvalRunner({"exactMatch": ExactMatchEvaluator(), "failing": FailingEvaluator()}).run(suite, model))
        self.assertEqual(model.calls, [("Fail", {}), ("Return {{city}}", {"city": "Paris"})])
        self.assertEqual((run.suite_id, run.provider_name, run.model_name), (suite.id, "Test provider", "Test model"))
        failed, result = run.results
        self.assertEqual((failed.prompt, failed.error, failed.scores, failed.passed), ("Fail", "Model unavailable", [], False))
        self.assertEqual(result.output, "Paris")
        self.assertEqual([score.error for score in result.scores], ["Unknown evaluator type: unknown", "Judge unavailable", None])
        self.assertEqual([score.passed for score in result.scores], [False, False, True])
        self.assertEqual(result.scores[2].expectation_id, exact.id)
        exact.name = "Edited"
        self.assertEqual(result.scores[2].expectation_name, "Exact")
        self.assertFalse(result.passed)

    def test_result_and_threshold_rules(self):
        result = EvalResult("id", "prompt", "Paris")
        self.assertFalse(result.passed)
        result.add_score(EvalScore(feedback="Match", passed=True, value=1))
        self.assertTrue(result.passed)
        self.assertFalse(EvalResult("id", "prompt", "Paris", "").passed)
        expectation = Expectation("Exact", "exactMatch", 1, {})
        suite = Suite("Mismatch")
        suite.add_test(make_test("Mismatch", [expectation]))
        class Mismatch(Model):
            async def generate_response(self, prompt, variables):
                return "paris "
        run = asyncio.run(EvalRunner({"exactMatch": ExactMatchEvaluator()}).run(suite, Mismatch()))
        self.assertEqual((run.results[0].scores[0].value, run.results[0].passed), (0, False))
        with self.assertRaisesRegex(ValueError, "empty suite"):
            asyncio.run(EvalRunner({}).run(Suite("Empty"), Model()))

    def test_runner_applies_threshold_to_async_evaluator(self):
        expectation = Expectation("Partial", "partial", 0.75, {})
        suite = Suite("Threshold")
        suite.add_test(make_test("Paris", [expectation]))
        run = asyncio.run(EvalRunner({"partial": PartialEvaluator()}).run(suite, Model()))
        score = run.results[0].scores[0]
        self.assertEqual((score.value, score.threshold, score.passed), (0.5, 0.75, False))
