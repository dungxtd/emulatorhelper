import time
from datetime import timedelta
from typing import TYPE_CHECKING

from module.base.button import Button
from module.base.decorator import cached_property
from module.base.utils import *
from module.logger import logger
from module.webui.setting import State
from module.ocr.tesseract_ocr import TesseractOcr

class Ocr:
    SHOW_LOG = False
    SHOW_REVISE_WARNING = False

    def __init__(self, buttons, lang='en', letter=(255, 255, 255), threshold=128, name=None):
        """
        Args:
            buttons (Button, tuple, list[Button], list[tuple]): OCR area.
            lang (str): 'azur_lane' or 'cnocr'.
            letter (tuple(int)): Letter RGB.
            threshold (int):
            name (str):
        """
        self.name = str(buttons) if isinstance(buttons, Button) else name
        self._buttons = buttons
        self.letter = letter
        self.threshold = threshold
        self.lang = lang

    @property
    def cnocr(self) -> "TesseractOcr":
        return TesseractOcr()

    @property
    def buttons(self):
        buttons = self._buttons
        buttons = buttons if isinstance(buttons, list) else [buttons]
        buttons = [button.area if isinstance(button, Button) else button for button in buttons]
        return buttons

    @buttons.setter
    def buttons(self, value):
        self._buttons = value

    def pre_process(self, image):
        """
        Args:
            image (np.ndarray): Shape (height, width, channel)

        Returns:
            np.ndarray: Shape (width, height)
        """
        image = extract_letters(image, letter=self.letter, threshold=self.threshold)

        return image.astype(np.uint8)

    def after_process(self, result):
        """
        Args:
            result (str): ''

        Returns:
            str:
        """
        return result

    def ocr(self, image, direct_ocr=False):
        """
        Args:
            image (np.ndarray, list[np.ndarray]):
            direct_ocr (bool): True to skip preprocess.

        Returns:

        """
        start_time = time.time()

        if direct_ocr:
            image_list = [i for i in image]
        else:
            image_list = [crop(image, area) for area in self.buttons]

        # This will show the images feed to OCR model
        # self.cnocr.debug(image_list)

        result_list = self.cnocr.extract_texts(image_list)
        result_list = [''.join(result) for result in result_list]
        result_list = [self.after_process(result) for result in result_list]

        if len(self.buttons) == 1 and len(result_list) > 0:
            result_list = result_list[0]
        if self.SHOW_LOG:
            logger.attr(name='%s %ss' % (self.name, float2str(time.time() - start_time)),
                        text=str(result_list))

        return result_list

class Digit(Ocr):
    """
    Do OCR on a digit, such as `45`.
    Method ocr() returns int, or a list of int.
    """

    def __init__(self, buttons, lang='en', letter=(255, 255, 255), threshold=128, name=None):
        super().__init__(buttons, lang=lang, letter=letter, threshold=threshold, name=name)

    def after_process(self, result):
        result = super().after_process(result)

        return result
