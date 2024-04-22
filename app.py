import datetime
import time
import logging

import requests as requests
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


class PostForm(object):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=./DefaultChromeDataWC")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        self.__driver = webdriver.Chrome(
            executable_path=r"chromedriver", chrome_options=options
        )

    def get_url_start(self):
        url = "https://web.whatsapp.com/"
        self.__driver.get(url)
        self.__driver.maximize_window()
        # Ожидание 3 секунды, чтобы обойти защиты Cloudfire
        self.__driver.implicitly_wait(3)
        WebDriverWait(self.__driver, 70).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div/div[3]/header/div[1]/div/img')
            )
        )

    def _one_page_url(self, number):
        self.__driver.get(f"https://web.whatsapp.com/send/?phone={number}")

    def _two_page_check_online(self):
        try:
            time.sleep(3)
            element = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="main"]/header/div[2]/div[2]/span')
                )
            )
            time.sleep(3)
            element = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="main"]/header/div[2]/div[2]/span')
                )
            )
            result = element.text
            if "данные контакта" in result:
                result = f"Off {element.text}"
            elif "был" in result:
                result = f"Off {element.text}"
            else:
                result = f"On {element.text}"
        except:
            result = "Off"
        return result

    def __start__(self):
        try:
            self.get_url_start()
            response = requests.get("http://107.175.21.15:8000/api/v1/number").json()
            for _num in response["users"]:
                if _num["is_parser"]:

                    self._one_page_url(number=_num)
                    result = self._two_page_check_online()
                    time.sleep(600)
                    if result == "Off":
                        try:
                            if " " in result:
                                time_temp = result.split(" ")[-1]
                                result = f"{datetime.datetime.now().strftime('%d.%m.%Y')} {time_temp}"
                        except Exception:
                            pass
                        requests.put(
                            "http://107.175.21.15:8000/api/v1/number",
                            data={
                                "user_id": _num["user_id"],
                                "number": _num["number"],
                                "is_parser": True,
                                "is_online": False,
                                "last_online": result,
                            },
                        )
                    else:
                        requests.put(
                            "http://107.175.21.15:8000/api/v1/number",
                            data={
                                "user_id": _num["user_id"],
                                "number": _num["number"],
                                "is_parser": True,
                                "is_online": True,
                                "last_online": result,
                            },
                        )
        except Exception as error:
            logger.info(error)
            self.__driver.close()
        self.__driver.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )
    while True:
        try:
            test_class = PostForm()
            test_class.__start__()
        except Exception as error:
            logger.info(error)
