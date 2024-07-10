from django.core.cache import cache
from django.utils.text import slugify
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from bubook.book.filters import CategoryFilter, TagFilter, BookFilter
from bubook.book.models import Category, Tag, Book
from bubook.book.services import create_category, create_tag, create_book
from config.django.base import CACHE_TTL


class CategoryApi(APIView):
    def get_permissions(self):
        if self.request and self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    def get_authenticators(self):
        if self.request and self.request.method == 'POST':
            return [JWTAuthentication(), ]
        super().get_authenticators()
        return []

    class FilterSerializer(serializers.Serializer):
        parent = serializers.CharField(max_length=65, required=False)
        name = serializers.CharField(max_length=65, required=False)

    class OutPutCategorySerializer(serializers.ModelSerializer):
        parent = serializers.SlugField(source='parent.name', read_only=True)

        class Meta:
            model = Category
            fields = ('name', 'parent')

    class InputCategorySerializer(serializers.Serializer):
        parent = serializers.CharField(max_length=64, required=False)
        name = serializers.CharField(max_length=64)

        def validate_parent(self, parent):
            if not Category.objects.filter(name=parent).exists():
                raise serializers.ValidationError('this parent category does not exist')
            return parent

        def validate_name(self, name):
            if Category.objects.filter(name=name).exists():
                raise serializers.ValidationError('this category already exist')
            return name

        def create(self, validated_data):
            try:
                return create_category(validated_data.get('name'), validated_data.get('parent'))
            except ValueError as ex:
                raise serializers.ValidationError(str(ex))

    @extend_schema(
        summary='Retrieve a list of categories',
        description='This endpoint returns a list of categories with optional filtering based on the name and parent '
                    'fields.',
        parameters=[FilterSerializer, ],
        responses=OutPutCategorySerializer(many=True),
        tags=['category', ],
    )
    def get(self, request):
        name_filter = self.request.GET.get('name', '')
        parent_filter = self.request.GET.get('parent', '')
        cache_key = f'all_categories_name_{name_filter}_parent_{parent_filter}'
        cache_result = cache.get(cache_key)
        if cache_result:
            return Response(cache_result, status=status.HTTP_200_OK)
        else:
            all_categories = Category.objects.all()
            filtered_categories = CategoryFilter(data=request.GET, queryset=all_categories).qs
            serialized_categories = self.OutPutCategorySerializer(filtered_categories, many=True,
                                                                  context={"request": request}).data
            cache.set(cache_key, serialized_categories, CACHE_TTL)
            return Response(serialized_categories, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Create a new category',
        description='This endpoint allows for the creation of a new category.'
                    'It expects a payload with the category details and saves it to the database.',
        request=InputCategorySerializer,
        responses=InputCategorySerializer,
        tags=['category', ],
    )
    def post(self, request):
        category_serializer = self.InputCategorySerializer(data=request.data)
        category_serializer.is_valid(raise_exception=True)
        try:
            category_serializer.save()
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(category_serializer.data)


class TagApi(APIView):
    def get_permissions(self):
        if self.request and self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    def get_authenticators(self):
        if self.request and self.request.method == 'POST':
            return [JWTAuthentication(), ]
        super().get_authenticators()
        return []

    class FilterSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=64, required=False)

    class OutPutTagSerializer(serializers.ModelSerializer):
        class Meta:
            model = Tag
            fields = ('name',)

    class InputTagSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=64)

        def validate_name(self, name):
            if Tag.objects.filter(name=name).exists():
                raise serializers.ValidationError('this tag already exist')
            return name

        def create(self, validated_data):
            try:
                return create_tag(validated_data.get('name'))
            except ValueError as ex:
                raise serializers.ValidationError(str(ex))

    @extend_schema(
        summary='Retrieve a list of tags',
        description='This endpoint returns a list of tags with optional filtering based on the name.',
        parameters=[FilterSerializer, ],
        responses=OutPutTagSerializer(many=True),
        tags=['tag', ],
    )
    def get(self, request):
        name_filter = self.request.GET.get('name', '')
        cache_key = f'all_tags_name_{name_filter}'
        cache_result = cache.get(cache_key)
        if cache_result:
            return Response(cache_result, status=status.HTTP_200_OK)
        else:
            all_tags = Tag.objects.all()
            filtered_tags = TagFilter(data=request.GET, queryset=all_tags).qs
            serialized_tags = self.OutPutTagSerializer(filtered_tags, many=True, context={"request": request}).data
            cache.set(cache_key, serialized_tags, CACHE_TTL)
            return Response(serialized_tags, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Create a new tag',
        description='This endpoint allows for the creation of a new tag.',
        request=InputTagSerializer,
        responses=InputTagSerializer,
        tags=['tag', ],
    )
    def post(self, request):
        tag_serializer = self.InputTagSerializer(data=request.data)
        tag_serializer.is_valid(raise_exception=True)
        try:
            tag_serializer.save()
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(tag_serializer.data, status=status.HTTP_201_CREATED)


class BookApi(APIView):
    def get_permissions(self):
        if self.request and self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    def get_authenticators(self):
        if self.request and self.request.method == 'POST':
            return [JWTAuthentication(), ]
        super().get_authenticators()
        return []

    class FilterSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=64, required=False)
        category = serializers.CharField(max_length=64, required=False)
        tag = serializers.CharField(max_length=64, required=False)
        price_min = serializers.IntegerField(required=False)
        price_max = serializers.IntegerField(required=False)

    class OutPutBookSerializer(serializers.ModelSerializer):
        category = serializers.SlugRelatedField(slug_field='name', read_only=True)
        tags = serializers.ListSerializer(child=serializers.SlugRelatedField(slug_field='name', read_only=True))

        class Meta:
            model = Book
            fields = ('slug', 'name', 'price', 'tags', 'category')

    class InputBookSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=64)
        price = serializers.IntegerField()
        tags = serializers.ListSerializer(child=serializers.CharField(max_length=54))
        category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

        def validate(self, attrs):
            if Book.objects.filter(slug=slugify(attrs.get('name', ''), allow_unicode=True)).exists():
                raise serializers.ValidationError('this book already exist')
            return attrs

        def create(self, validated_data):
            try:
                return create_book(validated_data.get('name'), validated_data.get('price'),
                                   validated_data.get('category'), validated_data.get('tags'))
            except ValueError as ex:
                raise serializers.ValidationError(str(ex))

    @extend_schema(
        summary='Retrieve a list of books',
        description='This endpoint returns a list of books with optional filtering based on the name.',
        parameters=[FilterSerializer, ],
        responses=OutPutBookSerializer(many=True),
        tags=['book', ],
    )
    def get(self, request):
        name_filter = self.request.GET.get('name', '')
        category_filter = self.request.GET.get('category', '')
        tag_filter = self.request.GET.get('tag', '')
        price_min_filter = self.request.GET.get('price_min', '')
        price_max_filter = self.request.GET.get('price_max', '')
        print(price_min_filter, price_max_filter)
        cache_key = f'all_books_{name_filter}_{category_filter}_{tag_filter}_{price_min_filter}_{price_max_filter}'
        cache_result = cache.get(cache_key)
        if cache_result:
            return Response(cache_result, status=status.HTTP_200_OK)
        else:
            all_books = Book.objects.filter(published=True)
            filtered_books = BookFilter(data=request.GET, queryset=all_books).qs
            serialized_books = self.OutPutBookSerializer(filtered_books, many=True, context={"request": request}).data
            cache.set(cache_key, serialized_books, CACHE_TTL)
            return Response(serialized_books, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Create a new book',
        description='This endpoint allows for the creation of a new book.',
        request=InputBookSerializer,
        responses=InputBookSerializer,
        tags=['book', ],
    )
    def post(self, request):
        book_serializer = self.InputBookSerializer(data=request.data)
        book_serializer.is_valid(raise_exception=True)
        try:
            book_serializer.save()
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(book_serializer.data, status=status.HTTP_201_CREATED)
