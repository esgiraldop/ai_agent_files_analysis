import traceback
import typing
from datetime import datetime

from pydantic import validate_call

from action import Action
from game_types import ErrorResultType, SuccessResultType


class Environment:
    """Interface between the agent and the actions. Executes actions and return their results.
    Actions are passed with dependency injection, making the agent very modular."""

    @validate_call
    def execute_actions(
        self, action: Action, args: dict
    ) -> SuccessResultType | ErrorResultType:
        """Execute and action and return the result."""
        try:
            result = action.execute(**args)
            return self.format_result(result, action.name)
        except Exception as e:
            return ErrorResultType(
                tool_name=action.name,
                tool_executed=False,
                error=str(e),
                traceback=traceback.format_exc(),
            )

    @validate_call
    def format_result(self, result: typing.Any, tool_name: str) -> SuccessResultType:
        """Format the result with metadata."""
        return SuccessResultType(
            tool_name=tool_name,
            tool_executed=True,
            result=result,
            timestamp=datetime.now().isoformat(),
        )
