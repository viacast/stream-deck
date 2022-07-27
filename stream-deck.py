from stream_deck import Page
from stream_deck.button import Button


ref_page = {
    "buttonMapping": {
        "button-1": "play",
        "button-2": "pause"
    },
    "images": {
        "play": "playcast-play.png",
        "pause": "pause.png",
        "update-preview": "/tmp/playcast-client-stream-deck-preview.png"
    },
    "actions": {
        "play": "play.sh"
    },
    "types": {
        "play": {
            "events": {
                "onPress": "",
                "onRelease": ""
            },
            "text": {
                "default": "",
                "pressed": ""
            },
            "images": {
                "default": "play",
                "pressed": "play"
            }
        }
    }
}


page = Page(**ref_page)

for button, button_type_key in page.buttonMapping.items():
  button_type = page.types.get(button_type_key)
  if not button_type:
    continue
  images = button_type.images
  print(button, button_type, images)
