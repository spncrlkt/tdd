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
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)

        # U is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        # U types "Buy peacock feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')

        # When U hits enter, the page lists "1: Buy peacock feathers" in a to-do list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows),
            "New to-do item did not appear in table"
        )

        # Text box intives U to add another item
        self.fail('Finish the test!')

        # U enters "Use peacock feathers to make a fly"

        # The page updates again, and now shows both items in the list

        # Explanatory exists for the unique url

        # U visits uniq url, the list is still there


if __name__ == '__main__':
    unittest.main(warnings='ignore')
