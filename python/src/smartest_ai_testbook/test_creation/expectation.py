from typing import Protocol
from uuid import uuid4

class IExpectation(Protocol):
    """Describe the constructor parameters for an expectation."""
    def __init__(
        self,
        name: str,
        evaluator_type,
        threshold: float,
        options: dict
    ):
        ...

class Expectation:
    def __init__(self, name: str, evaluator_type, threshold: float, options: dict):
        self.id = uuid4()
        self.name = name
        self.evaluator_type = evaluator_type
        self.threshold = threshold
        self.options = options