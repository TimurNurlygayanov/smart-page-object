#!/usr/bin/python3
# -*- encoding=utf8 -*-

# TODO: write article about __elements nasledovanie hack.

import time
from elements import WebElement, ManyWebElements

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import KNOWN_JS_ISSUES


class WebPage(object):

    _web_driver = 'my web driver'

    def __init__(self, web_driver, url=''):
        self._web_driver = web_driver
        self.get(url)

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            self.__getattribute__(name)._set_value(self._web_driver, value)
        else:
            super(WebPage, self).__setattr__(name, value)

    def __getattribute__(self, item):
        attr = object.__getattribute__(self, item)

        if not item.startswith('_') and not callable(attr):
            attr._web_driver = self._web_driver

        return attr

    def get(self, url):
        self._web_driver.get(url)
        self.wait_page_loaded()

    def go_back(self):
        self._web_driver.back()

    def refresh(self):
        self._web_driver.refresh()
        self.wait_page_loaded()

    def screenshot(self, file_name='screenshot.png'):
        self._web_driver.screenshot(file_name)

    def scroll_down(self, offset=0):
        """ Scroll the page down. """
        raise NotImplemented

    def scroll_up(self, offset=0):
        """ Scroll the page up. """
        raise NotImplemented

    def check_js_errors(self, ignore_list=None):
        """ This function checks JS errors on the page. """

        ignore_list = ignore_list or []

        logs = self._web_driver.get_log('browser')
        for log_message in logs:
            if log_message['level'] != 'WARNING':
                ignore = False
                for issue in ignore_list:
                    if issue in log_message['message']:
                        ignore = True
                        break

                assert ignore, 'JS error "{0}" on the page!'.format(log_message)

    def wait_page_loaded(self, timeout=60, check_js_complete=True,
                         check_page_changes=True, check_images=False,
                         wait_for_element=None,
                         wait_for_xpath_to_disappear=''):
        """ This function waits until the page will be completely loaded.
            We use many different ways to detect is page loaded or not:

            1) Check JS status
            2) Check modification in source code of the page
            3) Check that all images uploaded completely
               (Note: this check is disabled by default)
            4) Check that expected elements presented on the page
        """

        page_loaded = False
        k = 0

        source = ''
        try:
            source = self._web_driver.page_source
        except:
            pass

        # Wait until page loaded (and scroll it, to make sure all objects will be loaded):
        while not page_loaded:
            time.sleep(0.1)
            k += 1

            if check_js_complete:
                # Scroll down and wait when page will be loaded:
                try:
                    self._web_driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    page_loaded = self._web_driver.execute_script("return document.readyState == 'complete';")
                except:
                    pass

            if page_loaded and check_page_changes:
                # Check if the page source was changed
                new_source = ''
                try:
                    new_source = self._web_driver.page_source
                except:
                    pass

                page_loaded = new_source == source
                source = new_source

            # Wait when spinner of page loading will disappear:
            if page_loaded and wait_for_xpath_to_disappear:
                bad_element = None

                try:
                    bad_element = WebDriverWait(self._web_driver, 0.1).until(
                        EC.presence_of_element_located((By.XPATH, wait_for_xpath_to_disappear))
                    )
                except:
                    pass  # Ignore timeout errors

                page_loaded = not bad_element

            if page_loaded and wait_for_element:
                try:
                    page_loaded = WebDriverWait(self._web_driver, 0.1).until(
                        EC.element_to_be_clickable(wait_for_element._locator)
                    )
                except:
                    pass  # Ignore timeout errors

            assert k < timeout, 'The page loaded more than {0} seconds!'.format(timeout)

        # Go up:
        self._web_driver.execute_script('window.scrollTo(document.body.scrollHeight, 0);')


class WebPageDA(WebPage):

    sort_by_times_seen = WebElement(xpath='//span[contains(text(), "Times Seen")]')
    table_data_cells = ManyWebElements(xpath='//*[contains(@class, "-ad-cell-") or contains(@class, '
                                             '"ad-cell__number") or contains(@class, "ad-cell__date")]')
    table_data_text_fields = ManyWebElements(xpath='//*[contains(@class, "asns-text-ad-item")]//span')
    next_button = WebElement(xpath='//span[text()="Next"]')
    search_field = WebElement(xpath='//s-input')
    show_advanced_filters = WebElement(xpath='//span[contains(text(), "Advanced filters")]')
    search_button = WebElement(xpath='//button[contains(@class, "s-btn -hollow")]')
    filter_by = WebElement(xpath='//div[text()="Ad"]')
    filter_method = WebElement(xpath='//div[text()="Text Contains"]')
    advanced_filter_text = WebElement(xpath='//input[@placeholder="Text"]')
    apply_filter_button = WebElement(xpath='//span[text()="Apply Filters"]')
    add_one_more_filter_button = WebElement(xpath='//span[text()="Add one more"]')
    first_advanced_filter = WebElement(xpath='(//div[contains(@class, "item__layout")])[1]//input')
    second_advanced_filter = WebElement(xpath='(//div[contains(@class, "item__layout")])[2]//input')
    ads_tab = WebElement(xpath='//span[text()="Ads"]')
    ads_main_numbers = ManyWebElements(xpath='//*[@class="asns-legend__number"]')
    image_ads_tab = WebElement(xpath='//span[contains(text(), "Image ")]')
    landing_pages_tab = WebElement(xpath='//span[text()="Landing Pages"]')
    text_ads_tab = WebElement(xpath='//span[contains(text(), "Text ")]')
    html_ads_tab = WebElement(xpath='//span[contains(text(), "HTML ")]')
    export_button = WebElement(xpath='(//span[text()="Export"])[1]')
    last_page_link = WebElement(xpath=('//span[contains(@class, "pagination__last-item")]//'
                                       'span[contains(@class, "link__content")]'))
    last_page_text = WebElement(xpath='//span[contains(@class, "pagination__last-item")]')
    all_ads = ManyWebElements(xpath='//tr[@class="asns-table-creative-row"]')
    ads_links = ManyWebElements(xpath='//td/a|//td/div/a')
    role_switcher = WebElement(xpath='//button[contains(@class, "platform_select")]')
    role_advertiser = WebElement(xpath='//div[text()="advertiser"]')
    role_publisher = WebElement(xpath='//div/div[contains(text(), "publisher")]')
    role_current = WebElement(xpath='(//button/div[contains(@class, "-select-trigger-label")])[1]')
    period_filter = WebElement(xpath='(//span[contains(@class, "Styles__filterCaption")])[3]')
    device_filter = WebElement(xpath='(//span[contains(@class, "Styles__filterCaption")])[2]')
    country_filter = WebElement(xpath='(//span[contains(@class, "Styles__filterCaption")])[1]')
    period_all_time = WebElement(xpath='//span[text()="All Time"]')
    device_desktop = WebElement(xpath='//span[text()="Desktop"]')
    country_us = WebElement(xpath='//span[text()="United States"]')
    overview_image_ads_links = ManyWebElements(xpath='//a[contains(@class, "MediaItemStyles__item_ad_link")]')
    overview_html_ads_links = ManyWebElements(xpath='//a[contains(@class, "InfoStyles__item_ad_link")]')
    overview_text_ads_links = ManyWebElements(xpath='//div[contains(@class, "TextItemStyles__info_link")]/a')
    overview_all_titles = ManyWebElements(xpath='//div[@type="secondary"]')
    landing_fast_link = ManyWebElements(xpath='(//div[@type="primary"]/a)[1]')
    landing_ads_examples = ManyWebElements(xpath='//div[contains(@class, "NoDataSamplesLoop__ad_")]')
    creative_target_url = WebElement(xpath='//div[@class="asns-creative-target-url"]')
    next_ads = WebElement(xpath='//div[contains(@class, "creative-popup__next")]')
    advertisers_links = ManyWebElements(xpath='//a[@class="asns-js-cross-link asns-publisher-detail"]')
    overview_main_info = WebElement(xpath='//div[contains(@class, "OverviewLayoutStyles__ranks")]')
    cross_ads_count_links = ManyWebElements(xpath='//a[@class="asns-publisher-link asns-js-cross-link"]')
    cross_image_ads = ManyWebElements(xpath='//img[@class="asns-table-media-ad-cell__image"]')
    cross_table_lines = ManyWebElements(xpath='//*[contains(@class,"asns-table-media-ad-cell__preview")]')
    export_type_first = WebElement(xpath='(//button[contains(@class, "exportTo")])[1]')
    keywords_advertiser_links = ManyWebElements(xpath='//tr/td[2]//a[contains(text(),".")]')
    upgrade_to_business_button = ManyWebElements(xpath='//span[text()="Upgrade to Business"]')
    see_all_features_links = ManyWebElements(xpath='//a[text()="See all features"]')
    upgrade_links = ManyWebElements(xpath='//span[text()="Upgrade"]')

    # Landing page elements:
    landing_pages_titles = ManyWebElements(xpath='//div[contains(@class,"asns-landing-title")]')
    landing_pages_links = ManyWebElements(xpath='//div[contains(@class,"asns-landing-detail--url")]')
    table_data_ads_count = ManyWebElements(xpath='//td[@data-test="ads"]')
    table_data_times_seen = ManyWebElements(xpath='//td[@data-test="timesSeen"]')
    table_data_days_seen = ManyWebElements(xpath='//td[@data-test="daysSeen"]')

    def wait_page_loaded(self, timeout=600, check_js_complete=True,
                         check_page_changes=True, check_images=False,
                         wait_for_element=None,
                         wait_for_xpath_to_disappear=''):
        if not wait_for_xpath_to_disappear:
            super(WebPageDA, self).wait_page_loaded(timeout=timeout,
                wait_for_xpath_to_disappear='//*[contains(@class, "asns-spinner")]')
            self.check_js_errors()

    def check_js_errors(self, ignore_list=None):
        if not ignore_list:
            super(WebPageDA, self).check_js_errors(ignore_list=KNOWN_JS_ISSUES)

    def search(self, search_query):
        self.search_field.click()
        element = self._web_driver.switch_to.active_element
        element.send_keys(search_query)
        self.search_button.click()
        self.wait_page_loaded()

    def set_filter_by(self, filter_by):
        self.filter_by.click()
        xpath = '//div[contains(@class, "option-ex-text") and text()="{0}"]'.format(filter_by)
        self._web_driver.find_element_by_xpath(xpath).click()

    def set_filter_method(self, filter_method):
        self.filter_method.click()
        xpath = '//div[contains(@class, "option-ex-text") and text()="{0}"]'.format(filter_method)
        self._web_driver.find_element_by_xpath(xpath).click()

    def configure_advanced_filter(self, filter_id, params):
        default_options = ['Include', 'Ad', 'Text Contains']

        for i, value in enumerate(params):
            xpath = ('(//div[contains(@class, "item__layout")])[{0}]'
                     '//div[text()="{1}"]').format(filter_id, default_options[i])
            xpath_element = ('//div[contains(@class, "option-ex-text")'
                             'and text()="{0}"]').format(value)
            self._web_driver.find_element_by_xpath(xpath).click()
            self._web_driver.find_element_by_xpath(xpath_element).click()

    def set_page_size(self, page_size=10):
        xpath_pattern = ('//div[text()="{0}" and (contains(@class, "option")'
                         'or contains(@class, "select"))]')
        self._web_driver.find_element_by_xpath(xpath_pattern.format('10')).click()
        self._web_driver.find_element_by_xpath(xpath_pattern.format(page_size)).click()

        self.wait_page_loaded()
