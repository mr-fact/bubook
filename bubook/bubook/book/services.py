from django.db import transaction

from bubook.book.models import Category, Tag, Book


def create_category(name: str, parent: str = None) -> Category:
    if parent:
        try:
            category = Category(name=name, parent=Category.objects.get(name=parent))
        except Category.DoesNotExist:
            raise ValueError(f"parent category with name {name} does not exist")
    else:
        category = Category(name=name)
    category.save()
    return category


def get_or_create_category(name: str, parent: str = None) -> Category:
    if Category.objects.filter(name=name).exists():
        category = Category.objects.get(name=name)
    else:
        category = create_category(name, parent)
    return category


def create_tag(name: str) -> Tag:
    try:
        tag = Tag(name=name)
        tag.save()
    except Exception as e:
        raise ValueError('tag already exists')
    return tag


def get_or_create_tag(name: str) -> Tag:
    try:
        tag = create_tag(name)
    except Exception as e:
        tag = Tag.objects.get(name=name)
    return tag


@transaction.atomic
def create_book(name: str, price: int, category: Category, tags: list[str]) -> Book:
    book = Book(name=name, price=price, category=category)
    book.save()
    for tag_name in tags:
        tag = get_or_create_tag(tag_name)
        book.tags.add(tag)
    return book
