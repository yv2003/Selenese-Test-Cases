

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time
import unittest

class ToDoAppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the Chrome driver
        cls.driver = webdriver.Chrome()  # Use webdriver.Firefox() for Firefox
        cls.driver.get("https://tojsproj.netlify.app/")  # Change this path to your file location

    @classmethod
    def tearDownClass(cls):
        # Close the browser after all tests
        cls.driver.quit()

    def test_add_task(self):
        driver = self.driver
        input_box = driver.find_element(By.ID, "input-text")
        add_button = driver.find_element(By.CSS_SELECTOR, "button.btn")

        input_box.send_keys("New Task")
        add_button.click()
        time.sleep(1)
        
        try:
            task = driver.find_element(By.XPATH, "//ul[@id='list-container']/li[last()]")
            self.assertIn("New Task", task.text)
            print("test_add_task passed")
        except AssertionError:
            print("test_add_task failed")
            raise

    def test_prevent_empty_task(self):
        driver = self.driver
        add_button = driver.find_element(By.CSS_SELECTOR, "button.btn")
        add_button.click()

        alert = Alert(driver)
        alert_text = alert.text
        alert.accept()

        try:
            self.assertEqual(alert_text, "Please Enter Task")
            print("test_prevent_empty_task passed")
        except AssertionError:
            print("test_prevent_empty_task failed")
            raise

    def test_mark_task_as_completed(self):
        driver = self.driver
        input_box = driver.find_element(By.ID, "input-text")
        add_button = driver.find_element(By.CSS_SELECTOR, "button.btn")

        input_box.send_keys("Complete Task")
        add_button.click()
        time.sleep(1)

        task = driver.find_element(By.XPATH, "//ul[@id='list-container']/li[last()]")
        task.click()

        try:
            self.assertIn("checked", task.get_attribute("class"))
            print("test_mark_task_as_completed passed")
        except AssertionError:
            print("test_mark_task_as_completed failed")
            raise

    def test_delete_task(self):
        driver = self.driver
        input_box = driver.find_element(By.ID, "input-text")
        add_button = driver.find_element(By.CSS_SELECTOR, "button.btn")

        input_box.send_keys("Task to Delete")
        add_button.click()
        time.sleep(1)

        delete_button = driver.find_element(By.XPATH, "//ul[@id='list-container']/li[last()]/button")
        delete_button.click()
        time.sleep(1)

        task_texts = [task.text for task in driver.find_elements(By.XPATH, "//ul[@id='list-container']/li")]

        try:
            self.assertNotIn("Task to Delete", task_texts)
            print("test_delete_task passed")
        except AssertionError:
            print("test_delete_task failed")
            raise

    def test_toggle_task_completion(self):
        driver = self.driver
        input_box = driver.find_element(By.ID, "input-text")
        add_button = driver.find_element(By.CSS_SELECTOR, "button.btn")

        input_box.send_keys("Toggle Task")
        add_button.click()
        time.sleep(1)

        task = driver.find_element(By.XPATH, "//ul[@id='list-container']/li[last()]")
        task.click()

        try:
            self.assertIn("checked", task.get_attribute("class"))
            task.click()
            self.assertNotIn("checked", task.get_attribute("class"))
            print("test_toggle_task_completion passed")
        except AssertionError:
            print("test_toggle_task_completion failed")
            raise

    def test_task_count_after_adding_multiple_tasks(self):
        driver = self.driver
        input_box = driver.find_element(By.ID, "input-text")
        add_button = driver.find_element(By.CSS_SELECTOR, "button.btn")
    
        tasks_to_add = ["Task 1", "Task 2", "Task 3"]
        for task in tasks_to_add:
            input_box.send_keys(task)
            add_button.click()
            time.sleep(1)

        tasks = driver.find_elements(By.XPATH, "//ul[@id='list-container']/li")

        try:
            self.assertEqual(len(tasks), len(tasks_to_add))
            print("test_task_count_after_adding_multiple_tasks passed")
        except AssertionError:
            print("test_task_count_after_adding_multiple_tasks failed")
            raise

    def test_delete_specific_task(self):
        driver = self.driver
        input_box = driver.find_element(By.ID, "input-text")
        add_button = driver.find_element(By.CSS_SELECTOR, "button.btn")
    
        tasks_to_add = ["Task A", "Task B", "Task C"]
        for task in tasks_to_add:
            input_box.send_keys(task)
            add_button.click()
            time.sleep(1)

        delete_button = driver.find_element(By.XPATH, "//ul[@id='list-container']/li[2]/button")
        delete_button.click()
        time.sleep(1)

        remaining_tasks = [task.text for task in driver.find_elements(By.XPATH, "//ul[@id='list-container']/li")]

        try:
            self.assertEqual(remaining_tasks, ["Task A", "Task C"])
            print("test_delete_specific_task passed")
        except AssertionError:
            print("test_delete_specific_task failed")
            raise

if __name__ == "__main__":
    unittest.main()
