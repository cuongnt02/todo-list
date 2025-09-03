from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_todo_list(self):
        # Edith has heard about a new online to-do app
        # She goes to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mentions to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # She is invited to enter a to-do item straight away
        input_box = self.get_item_input_box()
        self.assertEqual(input_box.get_attribute("placeholder"), "Enter a to-do item")

        # She types "Buy peacock feathers" into a text box
        # Edith's hobby is tying fly-fishing lures
        input_box.send_keys("Buy peacock feathers")

        # When she hits enter, the pages updates, and now the page lists
        # "1. Buy peacock feathers" as an item in to-do list
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(row_text="1: Buy peacock feathers")

        # There is still a text box inviting her to add another item
        input_box = self.get_item_input_box()
        self.assertEqual(input_box.get_attribute("placeholder"), "Enter a to-do item")

        # She enters "Use peacock feathers to make a fly"
        # (Edith is very methodical)
        input_box.send_keys("Use peacock feathers to make a fly")
        input_box.send_keys(Keys.ENTER)

        # The page updates again, and now show both items on her list
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

        # Satisfied, she goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        input_box = self.get_item_input_box()
        input_box.send_keys("Buy peacock feathers")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # She notices that her list has a unique URL
        edith_url = self.browser.current_url
        self.assertRegex(edith_url, "/lists/.+")

        # Now a new user, Francis, comes along to the site

        ## We delete all browser's cookie
        ## as a way to simulate brand new user session
        self.browser.delete_all_cookies()

        # Francis visits the home page. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)

        # Francis start a new list entering a new item. He is less interesting
        # than Edith.
        input_box = self.get_item_input_box()
        input_box.send_keys("Buy milk")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # Francis gets his own unique URL
        francis_url = self.browser.current_url
        self.assertRegex(francis_url, "/lists/.+")
        self.assertNotEqual(francis_url, edith_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Buy milk", page_text)
        self.assertNotIn("Buy peacock feathers", page_text)

        # Satisfied, they both go back to sleep
