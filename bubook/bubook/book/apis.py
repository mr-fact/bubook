from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from bubook.book.filters import CategoryFilter, TagFilter
from bubook.book.models import Category, Tag
from bubook.book.services import create_category, create_tag
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
        categories = CategoryFilter(data=request.GET, queryset=Category.objects.all()).qs
        return Response(self.OutPutCategorySerializer(categories, many=True, context={"request": request}).data)

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
