import time
import logging
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.expected_conditions import NoSuchElementException
from .captcha_handler import CaptchaHandler


LOGGER = logging.getLogger(__name__)
options = Options()
options.add_argument('--headless')


class ThreatDefenceRedirectMiddleware(RedirectMiddleware):
    """
    Custom RedirectMiddleware
    Using Selenium and chromedriver with a --headless flag
    Checks if redirected to a CAPTCHA page or a browser identification page and acts accordingly
    """
    def __init__(self, settings):
        self.threat_defence = 'threat_defence.php'
        self.driver = webdriver.Chrome('/home/mr_evya/idaide/chromedriver', chrome_options=options)
        self.tries = 0
        self.captcha_handler = CaptchaHandler()
        self.cookies = None
        super().__init__(settings)

    # Test for `threat_defence` in redirect url, else call super class' redirect
    def _redirect(self, redirected, request, spider, reason):
        time.sleep(3)
        if self.threat_defence not in redirected.url:
            return super()._redirect(redirected, request, spider, reason)
        LOGGER.info('Threat defense triggered for {0}'.format(request.url))
        LOGGER.info('Redirected to: {0}'.format(redirected.url))
        request.cookies = self.bypass_threat_defense(redirected.url)
        self.driver.close()
        return request  # With cookies of solved CAPTCHA session

    def bypass_threat_defense(self, url):
        LOGGER.info('Number of tries: #{0}'.format(self.tries))
        self.driver.get(url)
        # While loop to decide whether we are on a browser detection (redirect) page or a captcha page
        while self.tries <= 5:  # Current limit is 5 giving pytesseract % of success
            LOGGER.info('Waiting for browser detection')
            time.sleep(3)
            try:
                self.cookies = self.find_solve_submit_captcha()
                break
            except NoSuchElementException:
                LOGGER.info('No CAPTCHA found in page')
            try:
                self.redirect_retry()
                break
            except NoSuchElementException:
                LOGGER.info('No Link in page either. EXITING')
                break
        # If the solution was wrong and we are prompt with another try call method again
        if self.threat_defence in self.driver.current_url:
            self.tries += 1
            LOGGER.info('CAPTCHA solution was wrong. Trying again')
            self.bypass_threat_defense(self.driver.current_url)
        if self.cookies:
            return self.cookies
        exit('Something went wrong')

    # Press retry link if reached a redirect page without captcha
    def redirect_retry(self):
        LOGGER.info('Looking for `retry` link in page')
        link = self.driver.find_element_by_partial_link_text('Click')
        LOGGER.info('Retrying to get CAPTCHA page')
        self.tries += 1
        self.bypass_threat_defense(link.get_attribute('href'))

    def find_solve_submit_captcha(self):
        LOGGER.info('Looking for CAPTCHA image in page')
        # Find
        captcha = self.driver.find_element_by_xpath("//img[contains(@src, 'captcha')]")
        LOGGER.info('Found CAPTCHA image: {0}'.format(captcha.get_attribute('src')))
        # Solve
        solved_captcha = self.captcha_handler.get_captcha(src=captcha.get_attribute('src'))
        LOGGER.info('CAPTCHA solved: {0}'.format(solved_captcha))
        input_field = self.driver.find_element_by_id('solve_string')
        input_field.send_keys(solved_captcha)
        LOGGER.info('Submitting solution')
        # Submit
        self.driver.find_element_by_id('button_submit').click()
        return self.driver.get_cookies()
