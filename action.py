import typing
from pydantic.dataclasses import dataclass


@dataclass
class Action:
    """Registers and action with adittional information useful to the agent"""

    name: str
    function: typing.Callable
    description: str
    parameters: dict
    terminal: bool = False

    def execute(self, **args: typing.Any) -> typing.Any:
        """Execute the action's function"""
        return self.function(**args)
