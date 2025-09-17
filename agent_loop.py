import json
import traceback
from litellm import completion
from pydantic import validate_call
from dataclasses import asdict

import env_config  # noqa: F401
from game_initializer import actions_registry, memories, actions_environment
from game_types import (
    Memory,
    ErrorResultType,
)


@validate_call
def agent_loop(iteration: int, max_iterations: int, model=str):
    while iteration < max_iterations:
        messages = [
            (msg.model_dump() if isinstance(msg, Memory) else asdict(msg))
            for msg in memories.get_memories()
        ]
        tools = actions_registry.get_actions_llm_schema()

        response = completion(
            model=model, messages=messages, tools=tools, max_tokens=1024
        )

        if response.choices[0].message.tool_calls():
            for tool in response.choices[0].message.tool_calls:
                tool_name = tool.function.name
                tool_args = json.loads(tool.function.arguments)

                memories.add_memory(
                    Memory(
                        role="user",
                        content={"tool_name": tool_name, "tool_args": tool_args},
                    )
                )

                if tool_name == "terminate":
                    print(f"Termination message: {tool_args['message']}")
                    break
                elif tool_name in actions_registry.get_actions_names():
                    result = actions_environment.execute_actions()
                else:
                    result = ErrorResultType(
                        tool_executed=False,
                        error=f"Unknown tool: {tool_name}",
                        traceback=traceback.format_exc(),
                    )

                memories.add_memory(
                    Memory(
                        role="user",
                        content=result,
                    )
                )

                print(f"Executing: {tool_name} with args {tool_args}")
                print(f"Result: {result}")
        else:
            result = response.choices[0].message.content
            print(f"Response: {result}")
            break

        iteration += 1
        print(f"Iteration number {iteration}...")
