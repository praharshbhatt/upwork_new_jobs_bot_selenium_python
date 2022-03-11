# Driver for navigation and web crawling
from typing import Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium_driver.constants as Const
import time


class SeleniumDriver:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def open_webpage(self, url: str):
        self.driver.get(url)
        time.sleep(1)

    def upwork_login(self, username: str, password: str, security_ans: str):

        # 1. For Username Input TextField
        self.driver.find_elements_by_xpath(
            '/html/body/div/div[2]/div/main/div/div[3]/form/div/div[1]/div[4]/div/input'
        )[0].send_keys(username)

        # 2. For Continue with Email button:
        self.driver.find_elements_by_xpath(
            '/html/body/div/div[2]/div/main/div/div[3]/form/div/div[1]/button'
        )[0].click()

        # 3. For Password Input TextField
        self.driver.find_elements_by_xpath(
            '/html/body/div/div[2]/div/main/div/div[3]/form/div/div[1]/div[3]/div/input'
        )[0].send_keys(password)
        time.sleep(5)

        # 4. For Continue button:
        self.driver.find_elements_by_xpath(
            '/html/body/div/div[2]/div/main/div/div[3]/form/div/div[1]/button'
        )[0].click()

        # 5. For Security question
        self.driver.find_elements_by_xpath(
            '/html/body/div/div[2]/div/main/div/div[3]/form/div/div[1]/div[3]/div[1]/div[1]/input'
        )[0].send_keys(security_ans)
        time.sleep(1)

        # 2. For Continue button:
        self.driver.find_elements_by_xpath(
            '/html/body/div/div[2]/div/main/div/div[3]/form/div/footer/div/div/div/button'
        )[0].click()
        time.sleep(1)

    def goto_recent_search(self):
        self.driver.find_elements_by_xpath(
            '/html/body/div[2]/div/div/div/main/div[2]/div[2]/div[1]/div[2]/div[2]/span/a'
        )[0].click()

    def list_all_results(self) -> Dict:
        jobs = {}
        
        # Check if the page had loaded correctly or not
        try:
            check_blocker = self.driver.find_elements(
                By.CLASS_NAME,
                'up-card-section'
            )
            if (not check_blocker):
                check_blocker = self.driver.find_elements(
                    By.CLASS_NAME,
                    "job-tile-responsive"
                )
            if (not check_blocker):
                time.sleep(60)
        except:
            print("Did not reach the results page.. Please check the browser")
            time.sleep(60)

        # Get all the job results
        results = self.driver.find_elements(
            By.CLASS_NAME,
            'up-card-section'
        )
        if (not results):
            results = self.driver.find_elements(
                By.CLASS_NAME,
                "job-tile-responsive"
            )

        for result in results:
            # print(result.text)
            try:
                # title
                title = result.find_element(By.CLASS_NAME, "job-tile-title")
                link = title.find_element(
                    By.TAG_NAME, "a").get_attribute("href")
                title = title.text

                # Description
                description = result.find_element(
                    By.XPATH,
                    '//*[@id="main"]/div/div/div/div/div[2]/div/div/div/div[1]/section[1]/div[2]/div[2]'
                ).text

                # First line details
                other_info = result.find_element(
                    By.XPATH,
                    '//*[@id="main"]/div/div/div/div/div[2]/div/div/div/div[1]/section[2]/div[2]/div[1]/small'
                )
                if (not other_info):
                    other_info = result.find_element(
                        By.XPATH,
                        '//*[@id="main"]/div/div/div/div/div[2]/div/div/div/div[1]/section[1]/div[2]/div[1]'
                    ).text

                jobs[link] = {
                    "title": title,
                    "description": description,
                    "other_info": other_info,
                    "link": link,
                }
            except Exception as e:
                pass
                # print(str(e))

        return jobs
