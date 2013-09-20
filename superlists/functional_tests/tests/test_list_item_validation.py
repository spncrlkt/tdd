from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        #tries to submit empty list item
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('\n')

        #error message
        error = self.browser.find_element_by_css_selector('.alert-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        #tries to submit valid item, works
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        #tries second empty list item
        self.get_item_input_box().send_keys('\n')

        #error message
        error = self.browser.find_element_by_css_selector('.alert-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        #corrects it by adding text
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(
            'Buy wellies\n'
        )
        self.check_for_row_in_list_table('1: Buy wellies')

        self.get_item_input_box().send_keys(
            'Buy wellies\n'
        )
        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.browser.find_element_by_css_selector('.alert-error')
        self.assertEqual(error.text, "You've already got this in your list")
