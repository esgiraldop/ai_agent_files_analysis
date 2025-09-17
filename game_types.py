import typing
from enum import Enum

from pydantic import BaseModel, TypeAdapter

if typing.TYPE_CHECKING:
    # For avoiding circular import with action.py
    from action import Action

# Adapters
string_adapter = TypeAdapter(str)
list_of_tuples_adapter = TypeAdapter(list[tuple[int, str]])
action_adapter = TypeAdapter("Action | None")
action_list_adapter = TypeAdapter(list["Action"])
dict_list_adapter = TypeAdapter(list[dict])
str_list_adapter = TypeAdapter(list[str])


class RoleEnum(str, Enum):
    assistant = "assistant"
    user = "user"
    system = "system"


# BaseModels


class SuccessResultType(BaseModel):
    tool_name: str
    tool_executed: bool
    result: typing.Any
    timestamp: str


class ErrorResultType(BaseModel):
    tool_name: str
    tool_executed: bool
    error: str
    traceback: str


class Memory(BaseModel):
    role: RoleEnum
    content: SuccessResultType | ErrorResultType | str


class PropertiesArgument(BaseModel):
    type: typing.Literal["object", "string"]
    description: str


class Properties(BaseModel):
    file_name: typing.Optional[PropertiesArgument] = None
    search_term: typing.Optional[PropertiesArgument] = None
    message: typing.Optional[PropertiesArgument] = None

    def model_dump(self, *args, **kwargs) -> dict:
        # Overrriding pydantic's model_dump to exclude None values, so empty Properties → {}
        # None values make litellm to blow up
        return super().model_dump(exclude_none=True, *args, **kwargs)


class ActionParametersModel(BaseModel):
    type: typing.Literal["string", "object"]
    properties: Properties
    required: list[str]
