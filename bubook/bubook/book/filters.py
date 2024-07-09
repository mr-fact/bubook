import django_filters
from django_filters import FilterSet


class CategoryFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    parent = django_filters.CharFilter(method='filter_parent')

    def filter_parent(self, queryset, name, value):
        return queryset.filter(parent__name=value)


class TagFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')


class BookFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
