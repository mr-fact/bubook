from bubook.book.models import Category, Tag


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


def create_tag(name: str) -> Tag:
    try:
        tag = Tag(name=name)
        tag.save()
    except Exception as e:
        raise ValueError('tag already exists')
    return tag
