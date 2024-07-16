from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class PkSlugRelatedField(serializers.RelatedField):
    default_error_messages = {
        'does_not_exist': _('Object with {slug_name}={value} does not exist.'),
        'invalid': _('Invalid value.'),
    }

    def __init__(self, slug_field=None, **kwargs):
        assert slug_field is not None, 'The `slug_field` argument is required.'
        self.slug_field = slug_field
        super().__init__(**kwargs)

    def to_internal_value(self, slug):
        queryset = self.get_queryset()
        try:
            return queryset.get(**{self.slug_field: slug}).pk
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_str(slug))
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, pk):
        queryset = self.get_queryset()
        try:
            return getattr(queryset.get(pk=pk), self.slug_field)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_str(pk))
        except (TypeError, ValueError):
            self.fail('invalid')
        return
