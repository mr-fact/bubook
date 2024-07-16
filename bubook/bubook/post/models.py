import mongoengine


class Post(mongoengine.Document):
    title = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    price = mongoengine.IntField(required=True)
    published = mongoengine.BooleanField(default=False)
    seller = mongoengine.IntField(required=True)
    book = mongoengine.IntField(required=True)
    links = mongoengine.DictField(required=True)
    tags = mongoengine.ListField(mongoengine.StringField())

    def __str__(self):
        return f'{self.title}'
