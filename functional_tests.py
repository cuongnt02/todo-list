from selenium import webdriver
import unittest


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


        # She is invited to enter a to-do item straight away
        self.fail("Finish the tests!")


        # She types "buy peacock feather" into a text box
        # Edith's hobby is tying fly-fishing lures

        # When she hits enter, the pages updates, and now the page lists
        # "1. Buy peacock feathers" as an item in to-do list

        # There is still a text box inviting her to add another item
        # She enters "Use peacock feathers to make a fly" (Edith is very methodical)

        # The page updates again, and now show both items on her list 

        # Satisfied, she goes back to sleep

if __name__ == "__main__":
    unittest.main()
