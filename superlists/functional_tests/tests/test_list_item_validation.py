from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        #tries to submit empty list item
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        #error message
        error = self.browser.find_element_by_css_selector('.error')
        self.assertEqual(error.text, "You can't have an empty list item")

        #tries to submit valid item, works
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        #tries second empty list item
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        #error message
        error = self.browser.find_element_by_css_selector('.error')
        self.assertEqual(error.text, "You can't have an empty list item")

        #corrects it by adding text
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')

        self.fail("Don't forget to also test duplicate items!")
