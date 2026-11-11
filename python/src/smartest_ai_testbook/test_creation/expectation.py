from typing import Protocol
from uuid import UUID, uuid4

class IExpectation(Protocol):
    """Describe the constructor parameters for an expectation."""
    id: UUID
    name: str
    evaluator_type: str
    threshold: float
    options: dict
    def __init__(
        self,
        name: str,
        evaluator_type,
        threshold: float,
        options: dict
    ):
        ...

class Expectation(IExpectation):
    def __init__(self, name: str, evaluator_type, threshold: float, options: dict):
        self.id = uuid4()
        self.name = name
        self.evaluator_type = evaluator_type
        self.threshold = threshold
        self.options = options
