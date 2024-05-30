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

    def check_phrases(self, input_string):
        # Định nghĩa các mẫu regex cho các điều kiện
        pattern1 = r'người chơi [\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+ \([0-9a-z]+\)'
        pattern2 = r'[\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+ \([0-9a-z]+\) đăng ký'

        # Kiểm tra các mẫu regex
        match1 = re.search(pattern1, input_string)
        match2 = re.search(pattern2, input_string)

        if match1 or match2:
            return False
        else:
            return True

    def daily_run_one(self):
        # self.ui_ensure(page_daily)
        self.device.sleep(2.5)
        self.device.screenshot()
        text = MEMBER.ocr(self.device.image)

        # username và id của người dùng
        referral_pattern = r'\((?:ID|1D|IĐ|iD|iĐ)[:\-\/\s]*(\d+)\)\s*\.?$'
        if len(text):
            if self.check_phrases(text):
                logger.info(f"----------------------------------")
                logger.info(text)
                text = text.strip()
                referral_match = re.search(referral_pattern, text)
                if referral_match and referral_match.group(1):
                    referrer_id = referral_match.group(1).strip()
                    logger.info(f"Referrer ID: {referrer_id}")
                    text = re.sub(referral_pattern, '', text).strip()
                    # Mẫu regex cho username và user_id nếu có
                    user_pattern = r'(.+?)\s+(?:ID|1D|IĐ|iD|iĐ)[:\-\/\s]*(\d+)'
                    user_match = re.search(user_pattern, text)
                    if user_match:
                        username = user_match.group(1).strip()  # Loại bỏ khoảng trắng ở đầu và cuối
                        user_id = user_match.group(2)

                        logger.info(f"Username: {username}")
                        logger.info(f"User ID: {user_id}")
                    logger.info(f"Touch to approve button")
                    self.device.click(APPROVE)
                else:
                    logger.info(f"Touch to reject button")
                    self.device.click(REJECT)
            else:
                logger.info(f"Wait for notification")
                self.device.sleep(2.5)
        else:
            self.device.sleep(2.5)
            self.device.click(RANDOM)

    def daily_run(self):
        logger.hr('Daily run auto approve member')
        while 1:
            self.daily_run_one()

    def run(self):
        """
        Pages:
            in: Any page
            out: page_daily
        """
        self.daily_run()
