from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from lists.models import Item, List


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_item(self):
        my_list = List()
        my_list.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = my_list
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = my_list
        second_item.save()

        saved_list = List.objects.get()
        self.assertEqual(my_list, my_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, my_list)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.list, my_list)

    def test_cannot_save_null_list_item(self):
        my_list = List.objects.create()
        empty_item = Item(list=my_list, text=None)
        with self.assertRaises(IntegrityError):
            empty_item.save()

    def test_cannot_save_empty_list_item(self):
        my_list = List.objects.create()
        empty_item = Item(list=my_list, text="")
        with self.assertRaises(ValidationError):
            empty_item.full_clean()

    def test_get_absolute_url(self):
        my_list = List.objects.create()
        self.assertEqual(my_list.get_absolute_url(), f"/lists/{my_list.id}/")
