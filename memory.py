from pydantic.dataclasses import dataclass
from pydantic import Field, validate_call


class Memory:
    """Allows the agent to store and retrieve information about it's interactions"""

    def __init__(self):
        self.items = []

    def add_memory(self, memory: dict):
        """Add memory to working memory"""
        self.items.append(memory)

    def get_memories(self, limit: int = None) -> list[dict]:
        """Get formatted conversation history for prompt"""
        return self.items[:limit]


@dataclass
class Memory:
    items: list[dict] = Field(default_factory=list)

    @validate_call
    def add_memory(self, memory: dict):
        """Add memory to working memory"""
        self.items.append(memory)

    @validate_call
    def get_memories(self, limit: int | None = None) -> list[dict]:
        """Get formatted conversation history for prompt"""
        return self.items[:limit]
