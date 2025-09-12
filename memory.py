from pydantic import Field, validate_call
from pydantic.dataclasses import dataclass

from game_types import Memory
from goal import Goal


@dataclass
class Memories:
    items: list[Memory | Goal] = Field(default_factory=list)

    @validate_call
    def add_memory(self, memory: Memory | Goal):
        """Add memory to working memory"""
        self.items.append(memory)

    @validate_call
    def get_memories(self, limit: int | None = None) -> list[Memory | Goal]:
        """Get formatted conversation history for prompt"""
        return self.items[:limit]
