from litellm import completion
from pydantic import validate_call

import env_config  # noqa: F401
from game_initializer import actions_registry, memories


@validate_call
def agent_loop(iteration: int, max_iterations: int, model=str):
    while iteration < max_iterations:
        messages = [msg.model_dump for msg in memories.get_memories()]
        tools = actions_registry

        response = completion(
            model=model, messages=messages, tools=tools, max_tokens=1024
        )

        iteration += 1
        print(f"Iteration number {iteration}...")
