from json import dumps
from typing import Dict

from .type import Type
from .button import Button
from .keys import ActionKey, ActionPath, ImageKey, ImagePath, TypeKey


class Page:
  buttonMapping: Dict[Button, TypeKey]
  images: Dict[ImageKey, ImagePath]
  actions: Dict[ActionKey, ActionPath]
  types: Dict[TypeKey, Type]

  def __init__(self, buttonMapping: Dict[Button, TypeKey], images: Dict[ImageKey, ImagePath], actions: Dict[ActionKey, ActionPath], types: Dict[TypeKey, Type]) -> None:
    self.buttonMapping = {
        Button(k): v
        for k, v in buttonMapping.items()
    }
    self.images = images
    self.actions = actions
    self.types = {
        k: Type(**v)
        for k, v in types.items()
    }

  def __str__(self) -> str:
    return dumps(self, default=vars, indent=2)
