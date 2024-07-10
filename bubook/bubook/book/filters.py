import django_filters
from django_filters import FilterSet

from bubook.book.models import Book


class CategoryFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    parent = django_filters.CharFilter(method='filter_parent')

    def filter_parent(self, queryset, name, value):
        return queryset.filter(parent__name=value)


class TagFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')


class BookFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(method='filter_category')
    tag = django_filters.CharFilter(method='filter_tag')
    price = django_filters.RangeFilter()

    class Meta:
        model = Book
        fields = ('name', 'category', 'tag', 'price')

    def filter_category(self, queryset, name, value):
        return queryset.filter(category__name=value)

    def filter_tag(self, queryset, name, value):
        return queryset.filter(tags__name=value)
