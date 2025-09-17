import typing

from pydantic.dataclasses import dataclass

from game_types import ActionParametersModel


@dataclass
class Action:
    """Registers and action with adittional information useful to the agent"""

    name: str
    function: typing.Callable
    description: str
    parameters: ActionParametersModel
    terminal: bool = False

    def execute(self, **args: typing.Any) -> typing.Any:
        """Execute the action's function"""
        return self.function(**args)

    def to_litellm_schema(self) -> dict:
        """
        Convert Action into the dict format expected by LLM APIs (LiteLLM).
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": self.parameters.type,
                    "properties": self.parameters.properties.model_dump(),
                    "required": self.parameters.required,
                },
            },
        }
