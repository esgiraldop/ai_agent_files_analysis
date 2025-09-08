from action import Action
import traceback
import typing
from time import time

class Environment:
    """Interface between the agent and the actions. Executes actions and return their results.
        Actions are passed with dependency injection, making the agent very modular."""
    def execute_actions(self, action: Action, args: dict) -> dict:
        """Execute and action and return the result."""
        try:
            result = action.execute(**args)
            return self.format_result(result)
        except Exception as e:
            return {
                "tool_executed": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def format_result(self, result: typing.Any) -> dict:
        """Format the result with metadata."""
        return{
            "tool_executed": True,
            "result": result,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z")
        }
