import numpy as np
import re

from module.base.utils import get_color
from module.daily.assets import *
from module.logger import logger
from module.ocr.ocr import Digit
from module.ui.page import page_daily
from module.ui.ui import UI

MEMBER = Digit(MEMBER, threshold=128)

class Daily(UI):
    daily_current: int
    daily_checked: list
    emergency_module_development = False

    def daily_run_one(self):
        logger.hr('Daily run auto approve member')
        # self.ui_ensure(page_daily)
        self.device.sleep(1)
        self.device.screenshot()
        text = MEMBER.ocr(self.device.image)

        # username và id của người dùng
        pattern = r'(.+?) ID: (\d+)(?:.*?@(.+?) \(ID:(\d+)\))?'
        if len(text):
            match = re.match(pattern, text)
            if match:
                username = match.group(1).strip()
                user_id = match.group(2)
                referrer_name = match.group(3)
                referrer_id = match.group(4)
                
                logger.info(f"Username: {username}")
                logger.info(f"User ID: {user_id}")
                if referrer_name and referrer_id:
                    logger.info(f"Referrer Name: {referrer_name}")
                    logger.info(f"Referrer ID: {referrer_id}")
                    logger.info(f"Touch to approve button")
                    self.device.click(APPROVE)
                else:
                    logger.info(f"Touch to reject button")
                    self.device.click(REJECT)

    def daily_run(self):
        self.daily_run_one()

    def run(self):
        """
        Pages:
            in: Any page
            out: page_daily
        """
        self.daily_run()
