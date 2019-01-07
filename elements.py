#

import time

#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC


class WebElement(object):

    _locators = {}
    _web_driver = None

    def __init__(self, **kwargs):
        for attr in kwargs:
            self._locators[attr] = kwargs.get(attr)

    def _wait(self, web_driver):
        # TODO: how to change By.XPATH?

        element = None

        try:
            pass
            # element = WebDriverWait(web_driver, timeout).until(
            #    EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "asns-spinner")]'))
            # )
        except:
            pass  # Ignore timeout errors

        return element

    def wait_to_be_clickable(self, timeout=10):
        """ Wait until the element will be clickable. """
        # TODO: wait here
        print(self._web_driver)
        time.sleep(1)

    def is_clickable(self):
        """ Check is element clickable or not. """
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

    def _set_value(self, web_driver, value):
        # TODO: wait until object will be ready and set value to this object.
        element = self._wait(web_driver=web_driver)
        print('set value:', value)
        # element.clear()
        # element.sendkeys(value)

    def click(self):
        raise NotImplemented

    def long_click(self, timeout=0.5):
        raise NotImplemented

    def highlight_and_make_screenshot(self, file_name='element.png'):
        """ Highlight element and make the screen-shot of all page. """
        raise NotImplemented


class ManyWebElements(WebElement):

    def _set_value(self, web_driver, value):
        """ Not applicable for the list of elements. """
        raise NotImplemented

    def count(self):
        raise NotImplemented

    def get_text(self):
        raise NotImplemented

    def get_attribute(self):
        raise NotImplemented

    def highlight_and_make_screenshot(self, file_name='element.png'):
        """ Highlight elements and make the screen-shot of all page. """
        raise NotImplemented


e = WebElement(xpath='test')
