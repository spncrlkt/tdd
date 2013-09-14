from django.core.urlresolvers import resolve
from django.test import TestCase, Client
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    # too long?

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

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        client = Client()
        response = client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )

        self.assertEqual(Item.objects.all().count(), 1)
        new_item = Item.objects.all()[0]
        self.assertEqual(new_item.text, 'A new list item')
        self.assertEqual(List.objects.all().count(), 1)
        new_list = List.objects.all()[0]
        self.assertEqual(new_item.list, new_list)

        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

class NewItemTest(TestCase):

    def test_saving_a_POST_request_to_an_existing_list(self):
        list = List.objects.create()
        other_list = List.objects.create()
        client = Client()
        response = client.post(
            '/lists/%d/new_item' % (list.id,),
            data={'item_text': 'A new item for an existing list'}
        )
        self.assertEqual(Item.objects.all().count(), 1)
        new_item = Item.objects.all()[0]
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, list)

        self.assertRedirects(response, '/lists/%d/' % (list.id,))
