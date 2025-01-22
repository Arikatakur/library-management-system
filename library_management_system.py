class LibraryManagementSystem:
    def __init__(self):
        self.books = []

    def add_book(self, title, author, isbn):
        if not title or not author or not isbn:
            raise ValueError("Title, author, and ISBN are required.")
        for book in self.books:
            if book["isbn"] == isbn:
                raise ValueError("Book with this ISBN already exists.")
        self.books.append({
            "title": title,
            "author": author,
            "isbn": isbn,
            "available": True
        })

    def borrow_book(self, isbn):
        for book in self.books:
            if book["isbn"] == isbn:
                if book["available"]:
                    book["available"] = False
                    return f"Book '{book['title']}' borrowed successfully."
                else:
                    return f"Book '{book['title']}' is not available."
        return "Book not found."

    def return_book(self, isbn):
        for book in self.books:
            if book["isbn"] == isbn:
                if not book["available"]:
                    book["available"] = True
                    return f"Book '{book['title']}' returned successfully."
                else:
                    return f"Book '{book['title']}' is already available."
        return "Book not found."

    def search_book(self, title=None, author=None, isbn=None):
        if not title and not author and not isbn:
            return self.books  # Return all books if no filters are applied
        
        results = []
        for book in self.books:
            # Check if the book matches ALL provided filters
            matches_title = not title or title.lower() in book["title"].lower()
            matches_author = not author or author.lower() in book["author"].lower()
            matches_isbn = not isbn or isbn == book["isbn"]
            
            if matches_title and matches_author and matches_isbn:
                results.append(book)
        return results

    def list_available_books(self):
        return [book for book in self.books if book["available"]]
