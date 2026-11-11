from typing import Protocol
from uuid import UUID, uuid4

from smartest_ai_testbook.test_creation.expectation import IExpectation

class ITestCase(Protocol):
    id: UUID
    prompt: str
    goldenReference: str | None
    variables: dict[str, str]
    rubric: str | None
    expectations: list[IExpectation]
    def __init__(
        self,
        prompt: str, 
        goldenReference: str | None, 
        variables: dict, 
        rubric: str | None,
        expectations: list[IExpectation]
    ):
        ...

class TestCase(ITestCase):
    """Concrete implementation of a test case. Don't use this class directly, use the TestCaseBuilder instead."""
    def __init__(self, 
                 prompt, 
                 goldenReference, 
                 variables, 
                 rubric, 
                 expectations
              ):
        self.id = uuid4()
        self.prompt = prompt
        self.goldenReference = goldenReference
        self.variables = variables
        self.rubric = rubric
        self.expectations = expectations

class TestCaseBuilder:
    """Builder class for creating test cases."""
    def __init__(self):
        self.prompt = None
        self.goldenReference = None
        self.variables = {}
        self.rubric = None
        self.expectations = []

    def set_prompt(self, prompt: str):
        self.prompt = prompt
        return self

    def set_golden_reference(self, goldenReference: str):
        self.goldenReference = goldenReference
        return self

    def add_variable(self, key: str, value):
        self.variables[key] = value
        return self

    def set_rubric(self, rubric: str):
        self.rubric = rubric
        return self

    def add_expectation(self, expectation):
        self.expectations.append(expectation)
        return self

    def build(self) -> TestCase:
        if not self.prompt:
            raise ValueError("Prompt must be set.")
        return TestCase(
            prompt=self.prompt,
            goldenReference=self.goldenReference,
            variables=self.variables,
            rubric=self.rubric,
            expectations=self.expectations
        )
