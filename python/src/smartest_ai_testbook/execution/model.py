from typing import Mapping, Protocol


class Model(Protocol):
    provider_name: str
    model_name: str

    async def generate_response(self, prompt: str, variables: Mapping[str, str]) -> str: ...


class ModelProvider(Protocol):
    def get_model(self, model_name: str) -> Model: ...
