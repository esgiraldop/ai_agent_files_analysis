import typing

class Action:
    """Registers and action with adittional information useful to the agent"""
    def __init__(self, name: str, function: typing.Callable, description: str, parameters: dict, terminal: bool = False):
        self.name = name
        self.function = function
        self.description = description
        self.terminal = terminal
        self.parameters = parameters

    def execute(self, **args) -> typing.Any:
        """Execute the action's function"""
        return self.function(**args)