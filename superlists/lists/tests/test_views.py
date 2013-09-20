from django.core.urlresolvers import resolve
from django.utils.html import escape
from django.test import TestCase, Client
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List
from lists.forms import ItemForm


class HomePageTest(TestCase):
    maxDiff = None

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', {'form': ItemForm()})
        self.assertMultiLineEqual(response.content.decode(), expected_html)

    def test_home_page_renders_home_template_with_form(self):
        response = Client().get('/')
        self.assertTemplateUsed(response, 'home.html')
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.all().count(), 0)

class ListViewTest(TestCase):

    def test_list_view_dispalys_all_items(self):
        list = List.objects.create()
        Item.objects.create(text='itemey 1', list=list)
        Item.objects.create(text='itemey 2', list=list)

        other_list = List.objects.create()
        Item.objects.create(text='other itemey 1', list=other_list)
        Item.objects.create(text='other itemey 2', list=other_list)

        client = Client()
        response = client.get('/lists/%d/' % (list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other itemey 1')
        self.assertNotContains(response, 'other itemey 2')
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(response.context['list'], list)

    def test_saving_a_POST_request_to_an_existing_list(self):
        list = List.objects.create()
        other_list = List.objects.create()
        client = Client()
        response = client.post(
            '/lists/%d/' % (list.id,),
            data={'text': 'A new item for an existing list'}
        )
        self.assertEqual(Item.objects.all().count(), 1)
        new_item = Item.objects.all()[0]
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, list)

        self.assertRedirects(response, '/lists/%d/' % (list.id,))

    def test_empty_item_validation_errors_end_up_on_lists_page(self):
        list = List.objects.create()

        response = Client().post(
            '/lists/%d/' % (list.id,),
            data={'text':''}
        )
        self.assertEqual(Item.objects.all().count(), 0)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')

        response = Client().post(
            '/lists/%d/' % (list1.id,),
            data={'text':'textey'}
        )
        self.assertEqual(Item.objects.all().count(), 1)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You've already got this in your list")
        self.assertContains(response, expected_error)

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        client = Client()
        response = client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )

        self.assertEqual(Item.objects.all().count(), 1)
        new_item = Item.objects.all()[0]
        self.assertEqual(new_item.text, 'A new list item')
        self.assertEqual(List.objects.all().count(), 1)
        new_list = List.objects.all()[0]
        self.assertEqual(new_item.list, new_list)

        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

    def test_validation_errors_sent_back_to_home_page_template(self):
        response = Client().post('/lists/new', data={'text': ''})
        self.assertEqual(Item.objects.all().count(), 0)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
