from selenium import webdriver
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_todo_list(self):
        # Edith has heard about a new online to-do app
        # She goes to check out its homepage
        self.browser.get("http://localhost:8000")

        # She notices the page title and header mentions to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn("To-Do", header_text)


        # She is invited to enter a to-do item straight away
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')


        # She types "Buy peacock feather" into a text box
        # Edith's hobby is tying fly-fishing lures
        input_box.send_keys('Buy peacock feather')

        # When she hits enter, the pages updates, and now the page lists
        # "1. Buy peacock feathers" as an item in to-do list
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertTrue(any(row.text == '1: Buy peacock feather' for row in rows))

        # There is still a text box inviting her to add another item
        # She enters "Use peacock feathers to make a fly" (Edith is very methodical)
        # The page updates again, and now show both items on her list 
        self.fail('Finish the tests!')
        # Satisfied, she goes back to sleep

if __name__ == "__main__":
    unittest.main()
