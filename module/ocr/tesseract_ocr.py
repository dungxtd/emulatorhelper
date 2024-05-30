import os

import re
import cv2
import numpy as np
from PIL import Image
from module.base.decorator import Config, cached_property, del_cached_property, run_once

from module.exception import RequestHumanTakeover
from module.logger import logger
import pytesseract

logger.info('Loading OCR dependencies')



class TesseractOcr():

    tesseract_binary_list = [
        './toolkit/Tesseract-OCR/tesseract.exe',
    ]

    @cached_property
    def tesseract_binary(self):
        # Try adb in deploy.yaml
        from module.webui.setting import State
        file = State.deploy_config.TesseractExecutable
        file = file.replace('\\', '/')
        if os.path.exists(file):
            return os.path.abspath(file)

        # Try existing adb.exe
        for file in self.tesseract_binary_list:
            if os.path.exists(file):
                return os.path.abspath(file)

        # Use adb in system PATH
        file = 'tesseract.exe'
        return file

    @cached_property
    def tesseract_tessdata_dir(self):
        # Try adb in deploy.yaml
        from module.webui.setting import State
        file = State.deploy_config.TesseractTessdataDir
        file = file.replace('\\', '/')
        if os.path.exists(file):
            return os.path.abspath(file)

        file = 'tessdata'
        return file
        


    def __init__(self):
        self._args = ()
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_binary
        self.tessdata_dir_config = fr'--tessdata-dir "{self.tesseract_tessdata_dir}"'

    def init(self):
        self

    def extract_texts(self, img):
        """Extracts the texts in the given image slices and returns them."""
        images = img

        texts = []
        for idx, img in enumerate(images):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            ret, thresh1 = cv2.threshold(
                gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

            rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 12))
            dilation = cv2.dilate(thresh1, rect_kernel, iterations=3)

            contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            im2 = img.copy()

            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)

                # Draw the bounding box on the text area
                rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Crop the bounding box area
                cropped = im2[y:y + h, x:x + w]

                # Using tesseract on the cropped image area to get text
                text = pytesseract.image_to_string(cropped, lang="vie", config=self.tessdata_dir_config)

                # Clean text
                text = text.replace("\n", " ").replace("  ", " ").strip()

                if (len(text)):
                    texts.append(text)

        return texts

    def debug(self, img_list):
        """
        Args:
            img_list: List of numpy array, (height, width)
        """
        self.init(*self._args)
        Image.fromarray(img_list[0]).show()
