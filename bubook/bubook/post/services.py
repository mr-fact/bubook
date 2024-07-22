from bubook.book.models import Book
from bubook.post.models import Post
from bubook.users.models import BaseUser


def create_new_post(seller: BaseUser, book: Book, title: str, description: str, price: int, links: dict[str],
                    tags: list[str]) -> None:
    return Post.objects.create(seller=seller, book=book, title=title, description=description, price=price, links=links,
                               tags=tags)
