from bubook.book.models import Book
from bubook.users.models import BaseUser


def create_new_post(seller: BaseUser, book: Book, title: str, description: str, price: int, links: list[str]) -> None:
    pass
