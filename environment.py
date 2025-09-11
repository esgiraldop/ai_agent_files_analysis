from action import Action
import traceback
import typing
from pydantic import validate_call, BaseModel
from datetime import datetime


class SuccessResultType(BaseModel):
    tool_executed: bool
    result: typing.Any
    timestamp: str


class ErrorResultType(BaseModel):
    tool_executed: bool
    error: str
    traceback: str


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
            return self.format_result(result)
        except Exception as e:
            return ErrorResultType(
                tool_executed=False,
                error=str(e),
                traceback=traceback.format_exc(),
            )

    @validate_call
    def format_result(self, result: typing.Any) -> SuccessResultType:
        """Format the result with metadata."""
        return SuccessResultType(
            tool_executed=True,
            result=result,
            timestamp=datetime.now().isoformat(),
        )
