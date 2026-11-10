from typing import Protocol
from uuid import uuid4

from smartest_ai_testbook.test_creation.test_case import ITestCase


class ITestSuite(Protocol):
    """Describe the constructor parameters for a test suite."""
    def __init__(
        self,
        id: str,
        name: str,
        tests: list[ITestCase]
    ):
        ...

    def add_test(self, test_case) -> 'ITestSuite':
        ...

class TestSuite(ITestSuite):
    def __init__(self, name: str):
        self.id = uuid4()
        self.name = name
        self.tests = []

    def add_test(self, test_case):
        self.tests.append(test_case)
        return self