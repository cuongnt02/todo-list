from django.utils import html
from django.test import TestCase
from lists.models import Item, List
import lxml.html


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_renders_input_form(self):
        response = self.client.get("/")
        parsed = lxml.html.fromstring(response.content)
        [form] = parsed.cssselect("form[method=POST]")
        self.assertEqual(form.get("action"), "/lists/new")
        [input] = form.cssselect("input[name=item_text]")


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        my_list = List.objects.create()
        response = self.client.get(f"/lists/{my_list.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_renders_input_form(self):
        my_list = List.objects.create()
        response = self.client.get(f"/lists/{my_list.id}/")
        parsed = lxml.html.fromstring(response.content)
        [form] = parsed.cssselect("form[method=POST]")
        self.assertEqual(form.get("action"), f"/lists/{my_list.id}/")
        inputs = form.cssselect("input")
        self.assertIn("item_text", [input.get("name") for input in inputs])

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="itemmey 1", list=correct_list)
        Item.objects.create(text="itemmey 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other list item", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, "itemmey 1")
        self.assertContains(response, "itemmey 2")
        self.assertNotContains(response, "other list item")

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/",
            data={"item_text": "A new item for the existing list"},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new item for the existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/", data={"item_text": "A new list item"}
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        my_list = List.objects.get()
        self.assertRedirects(response, f"/lists/{my_list.id}/")

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post("/lists/new", data={"item_text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        expected_error = html.escape("You can't have an empty list item")
        # print(response.content.decode())
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post("/lists/new", data={"item_text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
