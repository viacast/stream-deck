#!/usr/bin/env python3


import os
import subprocess
from sre_constants import SUCCESS
import threading

from PIL import Image, ImageDraw, ImageFont

from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

from stream_deck import Page, Button


ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")


def render_key_image(deck, icon_filename, font_filename, font_size, label_text):
  icon = Image.open(icon_filename)
  image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, 0, 0])
  draw = ImageDraw.Draw(image)
  font = ImageFont.truetype(font_filename, font_size)

  draw.text((image.width / 2, image.height - 5), text=label_text,
            font=font, anchor="ms", fill="white")
  return PILHelper.to_native_format(deck, image)


def update_key_image(deck, key, *, image, font, font_size, action, text, state):
  image = render_key_image(deck, image, font, font_size, text)
  # lock access
  with deck:
    deck.set_key_image(key, image)


def key_change_callback(deck, key, state, page: Page):
  button_pressed = Button.from_key(Button, key)
  print(button_pressed)
  buttons_in_page = []
  for button in page.buttonMapping.keys():
    buttons_in_page.append(button)

  if button_pressed not in buttons_in_page:
    print("not a valid button")
    return

  button_type_key = page.buttonMapping.get(button_pressed)
  button_type = page.types.get(button_type_key)

  keys_images = button_type.images
  keys_events = button_type.events
  button_text = button_type.text
  button_fonts = button_type.fonts

  if state:
    image = page.images.get(keys_images.pressed)
    action = page.actions.get(keys_events.onPress)
    text = button_text.pressed
    font = button_fonts.default
  else:
    image = page.images.get(keys_images.default)
    action = page.actions.get(keys_events.onRelease)
    text = button_text.default
    font = button_fonts.default

  print(button_type_key)
  print(image)
  print(action)
  print(text)

  update_key_image(deck, key, image=image, font=font,
                   font_size=font_size, action=action, text=text, state=False)
  print("Trying to execute the command")
  print(action)
  subprocess.call([action])
  return


ref_page = {
  "buttonMapping": {
    "button-1": "play",
    "button-2": "play",
    "button-12": "play",
    "button-22": "play",
    "button-32": "play"
  },
  "images": {
    "play": "/home/rubens/Documents/stream-deck/assets/viacast-logo-light.png",
    "play-pressed": "/home/rubens/Documents/stream-deck/assets/viacast-logo-red.png",
    "pause": "pause.png",
    "update-preview": "/tmp/playcast-client-stream-deck-preview.png"
  },
  "actions": {
    "play": "/home/rubens/Documents/stream-deck/calls/teste.sh"
  },
  "types": {
    "play": {
      "events": {
        "onPress": "play",
        "onRelease": ""
      },
      "text": {
        "default": "Teste",
        "pressed": "pressed",
        "fontSize": 18
      },
      "fonts": {
        "default": "/home/rubens/Documents/stream-deck/assets/Roboto-Regular.ttf",
        "pressed": ""
      },
      "images": {
        "default": "play",
        "pressed": "play-pressed"
      }
    }
  }
}


if __name__ == "__main__":
  streamdecks = DeviceManager().enumerate()

  print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

  for index, deck in enumerate(streamdecks):
    # This example only works with devices that have screens.
    if not deck.is_visual():
      continue

    deck.open()
    deck.reset()

    print("Opened '{}' device (serial number: '{}', fw: '{}')".format(
      deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
    ))

    # Set initial screen brightness to 30%.
    deck.set_brightness(20)

    # exit(SUCCESS)
    page = Page(**ref_page)

    for button, button_type_key in page.buttonMapping.items():

      button_type = page.types.get(button_type_key)
      if not button_type:
        continue
      keys_images = button_type.images
      keys_events = button_type.events
      button_text = button_type.text
      button_fonts = button_type.fonts

      index = button.get_key()
      image = page.images.get(keys_images.default)
      action = page.actions.get(keys_events.onPress)
      text = button_text.default
      font = button_fonts.default
      font_size = button_text.fontSize

      print(button.get_key())
      print(button_type_key)
      print(image)
      print(action)
      print(text)

      update_key_image(deck, index, image=image, font=font,
                       font_size=font_size, action=action, text=text, state=False)

      # exit(SUCCESS)

      # # Register callback function for when a key state changes.
    deck.set_key_callback(
      lambda deck, key, state: key_change_callback(deck, key, state, page))

    # # Wait until all application threads have terminated (for this example,
    # # this is when all deck handles are closed).
    for t in threading.enumerate():
      try:
        t.join()
      except RuntimeError:
        pass
