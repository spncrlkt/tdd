from django import forms

from lists.models import Item

EMPTY_LIST_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"

class ItemForm(forms.models.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].error_messages['required'] = EMPTY_LIST_ERROR

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(
                attrs={'placeholder': 'Enter a to-do item'}
            ),
        }

class ExistingListItemForm(ItemForm):

    class Meta(ItemForm.Meta):
        fields = ('list','text')

    def validate_unique(self):
        super().validate_unique()
        if self.non_field_errors():
            self._update_errors({'text': [DUPLICATE_ITEM_ERROR]})
            del self.errors['__all__']
