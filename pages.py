# TODO: write article about __elements nasledovanie hack.

from elements import WebElement, ManyWebElements


class WebPage(object):

    _web_driver = 'my web driver'

    def __init__(self, web_driver, url=''):
        self._web_driver = web_driver
        # web_driver.get(url)

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            self.__getattribute__(name)._set_value(self._web_driver, value)
        else:
            super(WebPage, self).__setattr__(name, value)

    def __getattribute__(self, item):
        if not item.startswith('_'):
            element = object.__getattribute__(self, item)
            element._web_driver = self._web_driver
            return element
        return object.__getattribute__(self, item)

    def get(self, url):
        self._web_driver.get(url)

    def go_back(self):
        self._web_driver.back()

    def refresh(self):
        self._web_driver.refresh()

    def screenshot(self, file_name='screenshot.png'):
        self._web_driver.screenshot(file_name)

    def scroll_down(self, offset=0):
        """ Scroll the page down. """
        raise NotImplemented

    def scroll_up(self, offset=0):
        """ Scroll the page up. """
        raise NotImplemented

    def check_js_errors(self, ignore_list=None):
        raise NotImplemented

    def wait_page_loaded(self, timeout=600, check_js_complete=True,
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

        raise NotImplemented


class MyPage(WebPage):

    element = WebElement(xpath='//')
    some_elements = ManyWebElements(xpath='//')


page = MyPage('TestDriver')
page.element = 'testF!'
page.element.wait_to_be_clickable()
page.some_elements[0].click()
