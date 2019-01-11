#!/usr/bin/python3
# -*- encoding=utf8 -*-

import time

from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebElement(object):

    _locator = ('', '')
    _web_driver = None
    _timeout = 10
    _wait_after_click = False  # TODO: how we can wait after click?

    def __init__(self, timeout=10, wait_after_click=False, **kwargs):
        self._timeout = timeout
        self._wait_after_click = wait_after_click

        for attr in kwargs:
            self._locator = (str(attr), str(kwargs.get(attr)))

    def find(self, timeout=10):
        """ Find element on the page. """

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

    def is_clickable(self):
        """ Check is element ready for click or not. """

        element = self.wait_to_be_clickable(timeout=0.1)
        return element is not None

    def is_presented(self):
        """ Check that element is presented on the page. """

        element = self.find(timeout=0.1)
        return element is not None

    def is_visible(self):
        """ Check is the element visible or not. """

        element = self.find(timeout=0.1)

        if element:
            return element.is_displayed()

        return False

    def get_text(self):
        """ Get text of the element. """

        element = self.find()
        text = ''

        try:
            text = str(element.text)
        except Exception as e:
            print('Error: {0}'.format(e))

        return text

    def get_attribute(self, attr_name):
        """ Get attribute of the element. """

        element = self.find()

        if element:
            return element.get_attribute(attr_name)

    def _set_value(self, web_driver, value, clear=True):
        element = self.find()

        if clear:
            element.clear()

        element.send_keys(value)

    def click(self, hold_seconds=0, x_offset=0, y_offset=0):
        """ Wait and click the element. """

        element = self.wait_to_be_clickable()

        action = ActionChains(self._web_driver)
        action.move_to_element_with_offset(element, x_offset, y_offset).\
            pause(hold_seconds).click(on_element=element).perform()

    def highlight_and_make_screenshot(self, file_name='element.png'):
        """ Highlight element and make the screen-shot of all page. """

        element = self.find()

        # Scroll page to the element:
        self._web_driver.execute_script("arguments[0].scrollIntoView();", element)

        # Add red border to the style:
        self._web_driver.execute_script("arguments[0].style.border='3px solid red'", element)

        # Make screen-shot of the page:
        self._web_driver.save_screenshot(file_name)


class ManyWebElements(WebElement):

    def __getitem__(self, item):
        """ Get list of elements and try to return required element. """
        elements = self.find()
        return elements[item]

    def find(self, timeout=10):
        """ Find elements on the page. """

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
        elements = self.find()
        return len(elements)

    def get_text(self):
        elements = self.find()
        result = []

        for element in elements:
            text = ''

            try:
                text = str(element.text)
            except Exception as e:
                print('Error: {0}'.format(e))

            result.append(text)

        return result

    def get_attribute(self, attr_name):
        """ Get attribute of all elements. """

        results = []
        elements = self.find()

        for element in elements:
            results.append(element.get_attribute(attr_name))

        return results

    def highlight_and_make_screenshot(self, file_name='element.png'):
        """ Highlight elements and make the screen-shot of all page. """

        elements = self.find()

        for element in elements:
            # Scroll page to the element:
            self._web_driver.execute_script("arguments[0].scrollIntoView();", element)

            # Add red border to the style:
            self._web_driver.execute_script("arguments[0].style.border='3px solid red'", element)

        # Make screen-shot of the page:
        self._web_driver.save_screenshot(file_name)


e = WebElement(xpath='test')
