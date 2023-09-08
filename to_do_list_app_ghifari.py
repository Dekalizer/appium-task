import unittest
import time
import random
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    udid='emulator-5554',
    appPackage='com.gosty.todolistapp',
    appActivity='com.gosty.todolistapp.ui.splash.SplashActivity',
    language='en',
    locale='US'
)

appium_server_url = 'http://localhost:4723'

class Book():
    def __init__(self, title, author) -> None:
        self.title = title
        self.author = author

    def getTitle(self) -> str:
        return self.title
    
    def getAuthor(self) -> str:
        return self.author

class TestAppium(unittest.TestCase):
    # book_list = list()
    log = ""

    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, capabilities)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def scroll(self, times, multiplier = 1) -> None:
        x = self.driver.get_window_rect()['width']
        y = self.driver.get_window_rect()['height']

        for i in range(times):
            self.driver.swipe(x/2, multiplier*3*y/4, x/2, multiplier*1.5*y/4)

    def check_element_presence(self, element_id) -> bool:
        try:
            self.driver.find_element(by=AppiumBy.ID, value=element_id)
            return True 
        except:
            return False 
        
    # def get_all_books(self, detail = False, latest = False) -> list:  
    def get_all_books(self, detail = False) -> list:
        # Only run this method when on book list page/home
        
        registered_books = list()
        all_books_found = False

        # Assuming book attributes and attribute ids remain unchanged
        book_attributes = {'Cover URL': 'com.gosty.todolistapp:id/iv_cover', 
                            'Title': 'com.gosty.todolistapp:id/tv_data_title', 
                            'Author': 'com.gosty.todolistapp:id/tv_data_author', 
                            'Year': 'com.gosty.todolistapp:id/tv_data_year', 
                            'Category': 'com.gosty.todolistapp:id/tv_data_category'}
        
        while not all_books_found:
            book_counter = 0
            old_books = self.driver.find_elements(by=AppiumBy.ID, value='com.gosty.todolistapp:id/item_book_card')

            if len(old_books) == 0:
                raise Exception("No books are registered")

            for book in old_books:
                duplicate = False  
                # Scrolling until title and author is visible
                try:
                    title = book.find_element(by=AppiumBy.ID, value='com.gosty.todolistapp:id/tv_title').text
                    author = book.find_element(by=AppiumBy.ID, value='com.gosty.todolistapp:id/tv_author').text
                except:
                    try:
                        self.scroll(1, 0.25)
                        title = book.find_element(by=AppiumBy.ID, value='com.gosty.todolistapp:id/tv_title').text
                        author = book.find_element(by=AppiumBy.ID, value='com.gosty.todolistapp:id/tv_author').text
                    except:
                        pass

                for i in registered_books:
                    if title == i.title:
                        if author == i.author:
                            book_counter += 1
                            duplicate = True
                            break
                        
                if not duplicate and not detail:
                    registered_books.append(Book(title=title, author=author))
                elif not duplicate and detail:
                    registered_books.append(Book(title=title, author=author))
                    book.find_element(by=AppiumBy.CLASS_NAME, value='android.view.ViewGroup').click()

                    log = "Looping through all attributes"
                    for attr, attr_id in book_attributes.items():
                        
                        # Checking if attributes are displayed
                        if not (self.check_element_presence(attr_id)):
                            raise Exception(attr + " not found.")

                    self.driver.back()
                    time.sleep(1)

            if (book_counter == len(old_books)):
                all_books_found = True

            self.scroll(1, 0.75)

        # self.book_list = registered_books
        
        # return self.book_list
        return registered_books
    
    def random_attr(self, invalid_year_opt = False) -> list:

        url1 = ['https://img.freepik.com/free-photo/red-white-cat-i-white-studio_155003-13189.jpg',
                   'https://img.freepik.com/premium-vector/cute-knight-cartoon-character_257245-76.jpg',
                   'https://w0.peakpx.com/wallpaper/888/610/HD-wallpaper-dog-cartoon-dog.jpg',
                   'https://media.tenor.com/gWYdnRWUVtIAAAAd/monday-left-me-broken-cat.gif',
                   'https://media.tenor.com/P_xXDrjXl-AAAAAd/gogon-tunjang-sigit-rendang.gif']
        title1 = ['', 'The ', 'Great ', 'Story of The ', 'The Legendary ', 'Giga ', 'Sigma ']
        title2 = ['Apple', 'Cat', 'Dog', 'Knight', 'Mountain', 'Wolf', 'Princess']
        title3 = [' and The ', ' and ', ' and The Legendary ']
        author1 = ['John', 'Paul', 'Bill', 'Chris', 'James', 'Will']
        author2 = [' Wilson', ' Miller', ' Cooper', ' Carter', ' Williams']
        category1 = ['Horror', 'Romance', 'Fiction', 'Scientific', 'Funny']

        url = random.choice(url1)
        title = random.choice(title1) + random.choice(title2) + random.choice(title3) + random.choice(title2)
        author = random.choice(author1) + random.choice(author2)
        year = random.randint(1000,2023)
        invalid_year = 2147483648
        category = random.choice(category1)
        
        if invalid_year_opt:
            return [url,title,author,invalid_year,category]
        else:
            return [url,title,author,year,category]
        

    def test_list(self) -> None:
        print("\nRunning book list test")
        try:
            log = "Running test for listing books"
            self.driver.implicitly_wait(5)

            log = "Getting all books"
            books = self.get_all_books()

            print("Found " + str(len(books)) +" registered books.")

        except Exception as e:
            assert False, e


    def test_book_details(self) -> None:
        print("\nRunning book details test")
        try:
            log = "Running test for book details"
            self.driver.implicitly_wait(5)

            log = "Getting all books and showing the details"
            self.get_all_books(detail=True)

        except Exception as e:
            assert False, e

    def test_book_add_valid(self) -> None:
        print("\nRunning add book (valid) test")

        book_attributes = {'Cover URL': 'com.gosty.todolistapp:id/edt_cover', 
                            'Title': 'com.gosty.todolistapp:id/edt_title', 
                            'Author': 'com.gosty.todolistapp:id/edt_author', 
                            'Year': 'com.gosty.todolistapp:id/edt_year', 
                            'Category': 'com.gosty.todolistapp:id/edt_category'}
        try:
            log = "Running test for adding a book"
            self.driver.implicitly_wait(5)

            error = [False]

            log = "Getting randomized inputs"
            new_values = self.random_attr()

            # url, title, author, year, category = (attr[i] for i in range(len(attr)))

            log = "Searching for add book button"
            try:
                add_book_button = self.driver.find_element(by=AppiumBy.ID, value='com.gosty.todolistapp:id/fab_add')
            except:
                add_book_button = self.driver.find_element(by=AppiumBy.ID, value='com.gosty.todolistapp:id/fab_add_empty')

            log = "Clicking add book button"
            add_book_button.click()

            log = "Getting all fields"
            fields = list(self.driver.find_element(by=AppiumBy.ID, value=value) for key, value in book_attributes.items())

            log = "Searching for submit button"
            submit = self.driver.find_element(by=AppiumBy.ID, value='com.gosty.todolistapp:id/btn_add')

            log = "Looping and filling through all form fields"
            for field, value in zip(fields, new_values):
                field.send_keys(value)
                submit.click()

                if (field != fields[-1]):
                    log = "Check if it is submitted"
                    if (self.check_element_presence("com.gosty.todolistapp:id/item_book_card")):
                        raise Exception('Submitted new book with blank field')     

            # Checking if the newly added book is registered
            self.driver.implicitly_wait(5)
            books = self.get_all_books()

            for book in books:
                if new_values[1] == book.title and new_values[2] == book.author:
                    print("Book with the title '" + new_values[1] + "' and author '" + new_values[2] + "' found!")
                    return
                
            raise Exception("New book was not found")
        
                

        except Exception as e:
            assert False, e

    def test_book_update(self) -> None:
        print("\nRunning book update test")
        # Assuming book attributes and attribute ids remain unchanged
        book_attributes = {'Cover URL': 'com.gosty.todolistapp:id/edt_cover', 
                            'Title': 'com.gosty.todolistapp:id/edt_title', 
                            'Author': 'com.gosty.todolistapp:id/edt_author', 
                            'Year': 'com.gosty.todolistapp:id/edt_year', 
                            'Category': 'com.gosty.todolistapp:id/edt_category'}
        
        book_attributes_detail = {'Cover URL': 'com.gosty.todolistapp:id/iv_cover', 
                            'Title': 'com.gosty.todolistapp:id/tv_data_title', 
                            'Author': 'com.gosty.todolistapp:id/tv_data_author', 
                            'Year': 'com.gosty.todolistapp:id/tv_data_year', 
                            'Category': 'com.gosty.todolistapp:id/tv_data_category'}
        try:
            log = "Running book update test"
            self.driver.implicitly_wait(5)
            
            log = "Getting the first book on the list"
            try:
                book = self.driver.find_elements(by=AppiumBy.ID, value="com.gosty.todolistapp:id/item_book_card")[0].find_element(by=AppiumBy.CLASS_NAME, value='android.view.ViewGroup')
            except:
                raise Exception("No books are registered")

            log = "Clicking the book"
            book.click()

            log = "Clicking the update button"
            self.driver.find_element(by=AppiumBy.ID, value='com.gosty.todolistapp:id/btn_update').click()

            log = "Saving all current attributes"
            fields = list(self.driver.find_element(by=AppiumBy.ID, value=value) for key, value in book_attributes.items())
            old_attr = list(field.text for field in fields)

            log = "Getting new attribute values to the book"
            new_attr = self.random_attr()

            submit_button = self.driver.find_element(by=AppiumBy.ID, value='com.gosty.todolistapp:id/btn_submit')

            log = "Clearing all fields"
            for field in fields:
                field.clear()
        
            log = "Inputting new attribute values to the book"
            for field, value in zip(fields,new_attr):
                try:
                    field.send_keys(value)
                    submit_button.click()
                except:
                    raise Exception("Submitted with blank field")
           
            # Checking if the newly updated book's data has changed
            log = "Getting the attributes displayed"
            current_attr = list(self.driver.find_element(by=AppiumBy.ID, value=value).text for key, value in book_attributes_detail.items())[1:]
            current_attr = list(current_attr[i].replace(": ", "") for i in range(len(current_attr)))

            for current, old, new in zip(current_attr, old_attr[1:], new_attr[1:]):
                if (current != str(new)):
                    raise Exception("Attribute did not change")
            
            print("Book has been sucessfully updated")

        except Exception as e:
            assert False, e

    def test_book_delete(self) -> None:
        print("\nRunning book delete test")
        # Assuming book attributes and attribute ids remain unchanged
        
        book_attributes = {'Cover URL': 'com.gosty.todolistapp:id/edt_cover', 
                            'Title': 'com.gosty.todolistapp:id/edt_title', 
                            'Author': 'com.gosty.todolistapp:id/edt_author', 
                            'Year': 'com.gosty.todolistapp:id/edt_year', 
                            'Category': 'com.gosty.todolistapp:id/edt_category'}
        
        book_attributes_detail = {'Cover URL': 'com.gosty.todolistapp:id/iv_cover', 
                            'Title': 'com.gosty.todolistapp:id/tv_data_title', 
                            'Author': 'com.gosty.todolistapp:id/tv_data_author', 
                            'Year': 'com.gosty.todolistapp:id/tv_data_year', 
                            'Category': 'com.gosty.todolistapp:id/tv_data_category'}
        try:
            log = "Running book delete test"
            self.driver.implicitly_wait(5)
            
            log = "Getting the first book on the list"
            try:
                book = self.driver.find_elements(by=AppiumBy.ID, value="com.gosty.todolistapp:id/item_book_card")[0].find_element(by=AppiumBy.CLASS_NAME, value='android.view.ViewGroup')
            except:
                raise Exception("No books are registered")

            log = "Clicking the book"
            book.click()

            log = "Saving all current attributes"
            old_attr = list(self.driver.find_element(by=AppiumBy.ID, value=value).text for key, value in book_attributes_detail.items())[1:]
            old_attr = list(old_attr[i].replace(": ", "") for i in range(len(old_attr)))

            log = "Clicking the delete button"
            self.driver.find_element(by=AppiumBy.ID, value='com.gosty.todolistapp:id/btn_delete').click()
            self.driver.implicitly_wait(5)

            log = "Check if there is a confirmation button"
            if (self.check_element_presence("com.gosty.todolistapp:id/fab_add") or self.check_element_presence('com.gosty.todolistapp:id/fab_add_empty')):
                log = "Check if the book is deleted"
                books = self.get_all_books()

                for book in books:
                    if book.title == old_attr[0] and book.author == old_attr[1]:
                        raise Exception('The book is not deleted and there is no delete confirmation button')

                raise Exception('The book is deleted and there is no delete confirmation button')
            
            print("Book has been successfully deleted")

        except Exception as e:
            assert False, e

if __name__ == '__main__':
    unittest.main()