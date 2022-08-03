from typing import List, Optional
from StreamDeck.ImageHelpers import PILHelper
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.Devices import StreamDeck
from StreamDeck.DeviceManager import DeviceManager

from .type import Type
from .page import Page
from .button import Button
from .keys import ImageKey


class XStreamDeck:
  _deck: StreamDeck
  _pages: List[Page]
  _current_page_number: int

  def __init__(self, deck: StreamDeck) -> None:
    self._deck = deck
    self._pages = []
    self._setup_button_callbacks()

  def __repr__(self) -> str:
    return f"""<XStreamDeck type="{self._deck.deck_type()}" id="{self._deck.id()}">"""

  @property
  def current_page(self) -> Page:
    return self._pages[self._current_page_number]

  @property
  def current_page_number(self) -> int:
    return self.current_page_number

  def set_current_page(self, page):
    self._current_page_number = page

  def _render_page(self):
    page = self.current_page
    for button, button_type_key in page.buttonMapping.items():
      button_type = page.types.get(button_type_key)
      if not button_type:
        continue
      self.update_button_display(
          button, page.images.get(button_type.images.default))

  def _render_button_display(self, *, image_path, text='', font_size=12, font_family=None):
    icon = Image.open(image_path)
    image = PILHelper.create_scaled_image(
        self._deck, icon, margins=[0, 0, 0, 0])
    if text:
      font = None
      if font_family:
        font = ImageFont.truetype(font_family, font_size)
      draw = ImageDraw.Draw(image)
      draw.text((image.width / 2, image.height - 5), text=text,
                font=font, anchor="ms", fill="white")
    return PILHelper.to_native_format(self._deck, image)

  def _get_button_type(self, button: Button) -> Optional[Type]:
    page = self.current_page
    type_key = page.buttonMapping.get(button)
    if not type_key:
      return None
    return page.types.get(type_key)

  def _setup_button_callbacks(self) -> None:
    def callback(key, state):
      button = Button.from_key(key)
      type = self._get_button_type(button)
      image_key = type.images.default
      if state:
        image_key = type.images.pressed
      self.update_button_display(button, image_key)
    self._deck.set_key_callback(lambda _, key, state: callback(key, state))

  def add_page(self, page: Page) -> None:
    pass

  def update_button_display(self, button: Button, *, image_key: ImageKey = None, text='', font_size=12, font_family=None) -> None:
    page = self.current_page
    image_path = page.images.get(image_key)
    image = self._render_button_display(
        image_path=image_path, text=text, font_size=font_size, font_family=font_family)
    with self._deck as deck:
      deck.set_key_image(button.get_key(), image)

  @staticmethod
  def enumerate():
    return list(map(lambda deck: XStreamDeck(deck), DeviceManager().enumerate()))
