from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'system')

import plyer
import socket
import structlog
import traceback
from typing import Callable

from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField


logger = structlog.get_logger(__name__)


BUTTON_VIBRATION_DURATION = 0.2


def vibrate(
    duration_sec = BUTTON_VIBRATION_DURATION,
):
    try:
        plyer.vibrator.vibrate(duration_sec)
        logger.debug("Vibrate callback triggered")
    except NotImplementedError:
        logger.debug("Vibrate not implemented on this device")


class Controller(GridLayout):
    def __init__(
        self,
    ):
        super().__init__()
        self._client = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
        )
        self._ip = None
        self._port = None

    def send(
        self,
        instance = None,
        callback: Callable = None,
    ):
        try:
            self._client.sendto(instance.text.encode(), (self._ip, int(self._port)))
            logger.debug(f"Sent to ({self._ip},{self._port}): {instance.text}")
            if callback:
                callback()
        except Exception:
            tb = traceback.format_exc()
            logger.error(f"Error caught: {tb}")

class Dpad(GridLayout):
    pass

class Abxy(GridLayout):
    pass

class SmallButton(Button):
    pass

class MediumButton(Button):
    pass

class MDIconWithText(MDIconButton):
    text = StringProperty(None)

class MainApp(MDApp):

    def _bind_buttons(
        self,
    ):
        buttons = [
            self._controller.ids.back,
            self._controller.ids.start,
            self._controller.ids.dpad.ids.top,
            self._controller.ids.dpad.ids.left,
            self._controller.ids.dpad.ids.right,
            self._controller.ids.dpad.ids.bottom,
            self._controller.ids.abxy.ids.top,
            self._controller.ids.abxy.ids.left,
            self._controller.ids.abxy.ids.right,
            self._controller.ids.abxy.ids.bottom,
        ]
        for button in buttons:
            button.bind(on_release=lambda instance: self._controller.send(instance, vibrate))

    def build(
        self,
    ):
        self._controller = Controller()
        self._bind_buttons()
        return self._controller

if __name__ == "__main__":
    try:
        MainApp().run()
    except Exception:
        tb = traceback.format_exc()
        logger.error(tb)