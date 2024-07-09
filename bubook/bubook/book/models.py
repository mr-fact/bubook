from django.db import models

from bubook.common.models import BaseModel


class Category(BaseModel):
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='children', null=True, blank=True
    )
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{str(self.parent.name) + " > " if self.parent else ""}{self.name}'


class Book(BaseModel):
    name = models.CharField(max_length=64, name='name')
    price = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tag', name='tags', related_name='books')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='books')
    published = models.BooleanField(default=False)

    def upload_location(self, filename):
        base, extension = filename.split('.')
        return f'main-images/{self.id}.{extension}'
    image = models.ImageField(null=True, upload_to=upload_location)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=64, name='name')

    def __str__(self):
        return f'{self.name}'
