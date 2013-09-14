from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        #tries to submit empty list item

        #error message

        #tries to submit valid item, works

        #tries second empty list item

        #error message

        #corrects it by adding text
        self.fail('write me')
