class LibraryItem:
    def __init__(self, title, author, item_id):
        self.title = title
        self.author = author
        self.item_id = item_id
        self.is_checked_out = False

    def check_out(self):
        if not self.is_checked_out:
            self.is_checked_out = True
            print(f"'{self.title}' has been checked out.")
        else:
            print(f"'{self.title}' is already checked out.")

    def return_item(self):
        if self.is_checked_out:
            self.is_checked_out = False
            print(f"'{self.title}' has been returned.")
        else:
            print(f"'{self.title}' was not checked out.")

    def display_info(self):
        status = "Checked Out" if self.is_checked_out else "Available"
        print(f"Item ID: {self.item_id}")
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Status: {status}")


class Book(LibraryItem):
    def __init__(self, title, author, item_id, num_pages, publisher):
        super().__init__(title, author, item_id)
        self.num_pages = num_pages
        self.publisher = publisher

    def display_info(self):
        super().display_info()
        print(f"Type: Book")
        print(f"Number of Pages: {self.num_pages}")
        print(f"Publisher: {self.publisher}")


class DVD(LibraryItem):
    def __init__(self, title, artist, item_id, duration, rating):
        super().__init__(title, artist, item_id)
        self.duration = duration
        self.rating = rating

    def display_info(self):
        super().display_info()
        print(f"Type: DVD")
        print(f"Duration: {self.duration} minutes")
        print(f"Rating: {self.rating}")


class Magazine(LibraryItem):
    def __init__(self, title, publisher, item_id, issue_number, publication_date):
        super().__init__(title, publisher, item_id)
        self.issue_number = issue_number
        self.publication_date = publication_date

    def display_info(self):
        super().display_info()
        print(f"Type: Magazine")
        print(f"Issue Number: {self.issue_number}")
        print(f"Publication Date: {self.publication_date}")




print("=== Book Example ===")
book = Book(title="1984", author="George Orwell", item_id=101, num_pages=142, publisher="NY Times")
book.display_info()
book.check_out()
book.check_out()
book.return_item()
book.return_item()
print()

print("=== DVD Example ===")
dvd = DVD(title="Inception", artist="Christopher Nolan", item_id=202, duration=148, rating="PG-15")
dvd.display_info()
dvd.check_out()
dvd.return_item()
print()

print("=== Magazine Example ===")
magazine = Magazine(title="National Geographic", publisher="National Geographic Partners", item_id=303,
                    issue_number=2021, publication_date="08/2021")
magazine.display_info()
magazine.check_out()
magazine.return_item()
print()

print("=== Base LibraryItem Example ===")
item = LibraryItem(title="Generic Item", author="John", item_id=404)
item.display_info()
item.check_out()
item.return_item()
