from typing import Optional
from .keys import ActionKey, ImageKey


class ButtonEvents:
  onPress: Optional[ActionKey]
  onRelease: Optional[ActionKey]

  def __init__(self, onPress: ActionKey, onRelease: ActionKey) -> None:
    self.onPress = onPress
    self.onRelease = onRelease


class ButtonText:
  default: Optional[str]
  pressed: Optional[str]

  def __init__(self, default: str, pressed: str) -> None:
    self.default = default
    self.pressed = pressed


class ButtonImage:
  default: Optional[ImageKey]
  pressed: Optional[ImageKey]

  def __init__(self, default: ImageKey, pressed: ImageKey) -> None:
    self.default = default
    self.pressed = pressed


class Type:
  events: ButtonEvents
  text: ButtonText
  image: ButtonImage

  def __init__(self, events: ButtonEvents, text: ButtonText, image: ButtonImage) -> None:
    self.events = ButtonEvents(**events)
    self.text = ButtonText(**text)
    self.image = ButtonImage(**image)
