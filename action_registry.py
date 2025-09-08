from action import Action

class ActionRegistry:
    """Registers and handles a collection of actions"""
    def __init__(self):
        self.actions = {}

    def register(self, action: Action):
        self.actions[action.name] = action

    def get_action(self, name: str) -> Action | None:
        return self.actions.get(name, None)

    def get_actions(self) -> list[Action]:
        """Get all registered actions"""
        return list(self.actions.values())