import json
import logging
import sys
import yaml
from os import path
from time import sleep

import board
import neopixel as np
import neopixel
from agt import AlexaGadget

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

with open('led_controller.yaml') as f:
    config = yaml.safe_load(f)

COLOR_MAGENTA = (255,0,255,0)
COLOR_WHITE = (0, 0, 0, 255)
COLOR_BLACK = (0, 0, 0, 0)

strip = np.NeoPixel(board.D18, config.get('npixels', 82),
                             brightness=config.get('brightness', 0.1),
                             pixel_order=config.get('rgb_order', 'GRBW'),
                             auto_write=False)

# below just shows that something is happening by turning
# on the strip briefly, todo turn this into a function or remove it
strip.fill(COLOR_MAGENTA)
strip.show()
sleep(1)
strip.fill(COLOR_BLACK)
strip.show()

class LedController(AlexaGadget):
    """
    Alexa gadget that controls an LED light strip
    """

    def __init__(self):

        # todo fix the self.config_file attribute to be part of
        # alexagadget class/object, and just access it here?

        self.config_file = path.abspath(__file__).split('.')[0] + '.yaml'

        with open(self.config_file) as f:
            self.config = yaml.safe_load(f)

        with open('secrets.yaml') as f:
            self.secrets = yaml.safe_load(f)

        # the parent init method handles bluetooth details and other
        # init tasks we need
        super().__init__()

        # set the color todo make configurable via alexa skill
        self.color = COLOR_MAGENTA

    def on_custom_ledcontroller_turnonleds(self, directive):

        payload = json.loads(directive.payload.decode('utf-8'))
        logger.info(f'directed to turn on leds with payload {payload}')

        strip.fill(self.color)
        strip.show()

    def on_custom_ledcontroller_turnoffleds(self, directive):

        payload = json.loads(directive.payload.decode('utf-8'))
        logger.infi(f'direct to turn off leds with payload {payload}')

        strip.fill(COLOR_BLACK)
        strip.show()

if __name__ == '__main__':
    try:
        LedController().main() # main inherited from AlexaGadget
    finally:
        strip.deinit()