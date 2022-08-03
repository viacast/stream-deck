from enum import Enum


class Button(Enum):
  BUTTON_NULL = 'button-null'
  BUTTON_1 = 'button-1'
  BUTTON_2 = 'button-2'
  BUTTON_3 = 'button-3'
  BUTTON_4 = 'button-4'
  BUTTON_5 = 'button-5'
  BUTTON_6 = 'button-6'
  BUTTON_7 = 'button-7'
  BUTTON_8 = 'button-8'
  BUTTON_9 = 'button-9'
  BUTTON_10 = 'button-10'
  BUTTON_11 = 'button-11'
  BUTTON_12 = 'button-12'
  BUTTON_13 = 'button-13'
  BUTTON_14 = 'button-14'
  BUTTON_15 = 'button-15'
  BUTTON_16 = 'button-16'
  BUTTON_17 = 'button-17'
  BUTTON_18 = 'button-18'
  BUTTON_19 = 'button-19'
  BUTTON_20 = 'button-20'
  BUTTON_21 = 'button-21'
  BUTTON_22 = 'button-22'
  BUTTON_23 = 'button-23'
  BUTTON_24 = 'button-24'
  BUTTON_25 = 'button-25'
  BUTTON_26 = 'button-26'
  BUTTON_27 = 'button-27'
  BUTTON_28 = 'button-28'
  BUTTON_29 = 'button-29'
  BUTTON_30 = 'button-30'
  BUTTON_31 = 'button-31'
  BUTTON_32 = 'button-32'

  def get_key(self):
    return list(Button).index(self) - 1

  @staticmethod
  def from_key(key):
    try:
      return list(Button)[key + 1]
    except IndexError:
      return Button.BUTTON_NULL
