import unittest
import subprocess
from library_management_system import LibraryManagementSystem

class TestLibraryManagementSystem(unittest.TestCase):
    def setUp(self):
        self.library = LibraryManagementSystem()

    def test_add_book(self):
        self.library.add_book("Title1", "Author1", "123")
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0]["title"], "Title1")
        
        with self.assertRaises(ValueError):
            self.library.add_book("", "Author2", "124")
        
        with self.assertRaises(ValueError):
            self.library.add_book("Title1", "Author1", "123")

    def test_borrow_book(self):
        self.library.add_book("Title2", "Author2", "456")
        result = self.library.borrow_book("456")
        self.assertEqual(result, "Book 'Title2' borrowed successfully.")
        
        result = self.library.borrow_book("456")
        self.assertEqual(result, "Book 'Title2' is not available.")
        
        result = self.library.borrow_book("999")
        self.assertEqual(result, "Book not found.")

        # Test borrowing a book when no books exist
        empty_library = LibraryManagementSystem()
        result = empty_library.borrow_book("456")
        self.assertEqual(result, "Book not found.")

    def test_return_book(self):
        self.library.add_book("Title3", "Author3", "789")
        self.library.borrow_book("789")
        
        result = self.library.return_book("789")
        self.assertEqual(result, "Book 'Title3' returned successfully.")
        
        result = self.library.return_book("789")
        self.assertEqual(result, "Book 'Title3' is already available.")
        
        result = self.library.return_book("999")
        self.assertEqual(result, "Book not found.")

        # Test returning a book when no books exist
        empty_library = LibraryManagementSystem()
        result = empty_library.return_book("789")
        self.assertEqual(result, "Book not found.")

    def test_search_book(self):
        self.library.add_book("Python Programming", "John Doe", "101")
        self.library.add_book("Learn Python", "Jane Smith", "102")

        results = self.library.search_book(title="Python")
        self.assertEqual(len(results), 2)

        results = self.library.search_book(author="Jane")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["isbn"], "102")

        results = self.library.search_book(isbn="101")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Python Programming")

        # Cover case where no parameters are passed to search_book
        results = self.library.search_book()
        self.assertEqual(len(results), 2)

        # Cover case where no books exist in the library
        empty_library = LibraryManagementSystem()
        results = empty_library.search_book()
        self.assertEqual(results, [])  # Ensure an empty list is returned

    def test_list_available_books(self):
        # Test with no books in the library
        available_books = self.library.list_available_books()
        self.assertEqual(len(available_books), 0)

        # Test with all books available
        self.library.add_book("Title4", "Author4", "111")
        self.library.add_book("Title5", "Author5", "112")
        available_books = self.library.list_available_books()
        self.assertEqual(len(available_books), 2)

        # Test when some books are borrowed
        self.library.borrow_book("111")
        available_books = self.library.list_available_books()
        self.assertEqual(len(available_books), 1)
        self.assertEqual(available_books[0]["isbn"], "112")

    def test_list_available_books_edge_case(self):
        # Test when all books are borrowed
        self.library.add_book("Title6", "Author6", "113")
        self.library.add_book("Title7", "Author7", "114")
        self.library.borrow_book("113")
        self.library.borrow_book("114")

        available_books = self.library.list_available_books()
        self.assertEqual(len(available_books), 0)  # No books should be available

    def test_search_book_no_params(self):
        # Test search_book explicitly when no books exist and no parameters are passed
        empty_library = LibraryManagementSystem()
        results = empty_library.search_book()
        self.assertEqual(results, [])  # Ensure an empty list is returned

    def test_search_book_no_params_with_books(self):
        # Test search_book explicitly when no parameters are passed and books exist
        self.library.add_book("Title9", "Author9", "116")
        self.library.add_book("Title10", "Author10", "117")
        results = self.library.search_book()
        self.assertEqual(len(results), 2)

    def test_list_empty_library(self):
        # Ensure list_available_books works with an empty library
        results = self.library.list_available_books()
        self.assertEqual(results, [])

    def test_edge_case_no_match(self):
        # Ensure search_book handles no match case correctly
        self.library.add_book("Title8", "Author8", "115")
        results = self.library.search_book(title="Nonexistent Title")
        self.assertEqual(len(results), 0)

    def test_search_book_multiple_params(self):
        self.library.add_book("Python Programming", "John Doe", "101")
        self.library.add_book("Learn Python", "Jane Smith", "102")
        self.library.add_book("Advanced Python", "John Doe", "103")

        # Search with both title and author
        results = self.library.search_book(title="Python", author="John")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["title"], "Python Programming")
        self.assertEqual(results[1]["title"], "Advanced Python")

    def test_main_execution(self):
        """Test that the script can be run as a module."""
        result = subprocess.run(
            ["python", "-m", "test_library_management"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)  # Ensure the script runs successfully
        self.assertIn("Ran 11 tests", result.stdout)  # Ensure the tests are executed

if __name__ == "__main__":
    unittest.main()
