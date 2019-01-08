#!/usr/bin/python3
# -*- encoding=utf8 -*-

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebElement(object):

    _locator = ('', '')
    _web_driver = None
    _timeout = 10

    def __init__(self, timeout=10, **kwargs):
        self._timeout = timeout
        for attr in kwargs:
            self._locator = (str(attr), str(kwargs.get(attr)))

    def find(self, timeout=10):
        # TODO: how to change By.XPATH?

        element = None

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
               EC.presence_of_element_located(self._locator)
            )
        except:
            # TODO: show beautiful RED error message with the description of the issue.
            print('Element not found on the page!')  # Ignore timeout errors

        return element

    def wait_to_be_clickable(self, timeout=10):
        """ Wait until the element will be ready for click. """

        element = None

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
                EC.element_to_be_clickable(self._locator)
            )
        except:
            pass  # Ignore timeout errors

        return element

    def wait_for_element(self, timeout=10):
        raise NotImplemented

    def is_clickable(self):
        """ Check is element ready for click or not. """
        raise NotImplemented

    def is_presented(self):
        """ Check that element is presented on the page. """
        raise NotImplemented

    def is_visible(self):
        """ Check is the element visible or not. """
        raise NotImplemented

    def get_text(self):
        raise NotImplemented

    def get_attribute(self):
        raise NotImplemented

    def _set_value(self, web_driver, value, clear=True):
        element = self.find()

        if clear:
            element.clear()

        element.send_keys(value)

    def click(self):
        """ Wait and click the element. """
        element = self.wait_to_be_clickable()
        element.click()

    def smart_click(self, timeout=0.5, x_offset=0, y_offset=0):
        """ Click any element with Selenium actions chain. """
        raise NotImplemented

    def highlight_and_make_screenshot(self, file_name='element.png'):
        """ Highlight element and make the screen-shot of all page. """
        raise NotImplemented


class ManyWebElements(WebElement):

    def __getitem__(self, item):
        """ Get list of elements and try to return required element. """
        elements = self._wait(self._web_driver)
        return elements[item]

    def find(self, timeout=10):
        # TODO: how to change By.XPATH?

        elements = []

        try:
            elements = WebDriverWait(self._web_driver, timeout).until(
               EC.presence_of_all_elements_located(self._locator)
            )
        except:
            # TODO: show beautiful RED error message with the description of the issue.
            print('Elements not found on the page!')  # Ignore timeout errors

        return elements

    def _set_value(self, web_driver, value):
        """ Not applicable for the list of elements. """
        raise NotImplemented

    def count(self):
        raise NotImplemented

    def get_text(self):
        elements = self.find()
        return [str(element.text) for element in elements]

    def get_attribute(self):
        raise NotImplemented

    def highlight_and_make_screenshot(self, file_name='element.png'):
        """ Highlight elements and make the screen-shot of all page. """
        raise NotImplemented


e = WebElement(xpath='test')
