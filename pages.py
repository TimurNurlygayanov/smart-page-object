# TODO: write article about __elements nasledovanie hack.

from elements import WebElement


class WebPage(object):

    _web_driver = 'my web driver'

    def __init__(self, web_driver):
        self._web_driver = web_driver

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


class MyPage(WebPage):

    element = WebElement(xpath='//')


page = MyPage('TestDriver')
# page.element = 'testS'

page.element = 'testF!'

page.element.wait_to_be_clickable()
