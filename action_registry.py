from pydantic import Field, validate_call
from pydantic.dataclasses import dataclass

from action import Action

from game_types import (
    action_adapter,
    action_list_adapter,
    dict_list_adapter,
    str_list_adapter,
)


@dataclass
class ActionRegistry:
    """Registers and handles a collection of actions"""

    actions: dict = Field(default_factory=dict)

    @validate_call
    def register(self, action: Action):
        self.actions[action.name] = action

    @validate_call
    def get_action(self, name: str) -> Action | None:
        return action_adapter.validate_python(self.actions.get(name, None))

    def get_actions(self) -> list[Action]:
        """Get all registered actions"""
        return action_list_adapter.validate_python(list(self.actions.values()))

    def get_actions_names(self) -> list[str]:
        """Get all registered actions names"""
        return str_list_adapter.validate_python(
            [action.name for action in self.get_actions()]
        )

    def get_actions_llm_schema(self) -> list[dict]:
        """Get all registered actions in the dict format expected by LLM APIs (LiteLLM)."""
        return dict_list_adapter.validate_python(
            [action.to_litellm_schema() for action in self.get_actions()]
        )
