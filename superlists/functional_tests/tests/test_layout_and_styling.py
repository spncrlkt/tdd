from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)

        inputbox = self.browser.find_element_by_tag_name('input')
        window_width = self.browser.get_window_size()['width']
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            window_width / 2,
            delta=6
        )

        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_tag_name('input')
        window_width = self.browser.get_window_size()['width']
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            window_width / 2,
            delta=6
        )
