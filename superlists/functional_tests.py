from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(6)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_reterive_it_later(self):
        self.browser = webdriver.Firefox()
        self.browser.get('http://localhost:8000')

        # U notices the page title and header mention to do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test')

        # U is invited to enter a to-do item straight away

        # U typus "Buy peacokc feathers" into a text box

        # When U hits enter, the page lists "1: Buy peacock feathers" in a to-do list

        # Text box intives U to add another item

        # U enters "Use peacock feathers to make a fly"

        # The page updates again, and now shows both items in the list

        # Explanatory exists for the unique url

        # U visits uniq url, the list is still there


if __name__ == '__main__':
    unittest.main(warnings='ignore')
