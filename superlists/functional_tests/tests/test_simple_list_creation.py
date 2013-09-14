from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_reterive_it_later(self):
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

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
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)

        # When U hits enter, the page lists "1: Buy peacock feathers" in a to-do list
        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        # Text box intives U to add another item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # U enters "Use peacock feathers to make a fly"
        # The page updates again, and now shows both items in the list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table(
            '2: Use peacock feathers to make a fly'
        )

        # new U shouldn't see prev U's
        self.browser.quit()

        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # make a new item , ensure that the url is distinct from user_list_url
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # When new U hits enter, the page lists "1: Buy peacock feathers" in a to-do list
        user_2_list_url = self.browser.current_url
        self.assertRegex(user_2_list_url, '/lists/.+')
        self.assertNotEqual(user_2_list_url, user_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Explanatory exists for the unique url
        # U visits uniq url, the list is still there
