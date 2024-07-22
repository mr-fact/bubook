from drf_spectacular.utils import extend_schema
from rest_framework import status, serializers
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from bubook.book.models import Book
from bubook.post.selectors import get_published_posts
from bubook.post.services import create_new_post
from bubook.users.models import BaseUser
from bubook.utils.serializers import PkSlugRelatedField


class PostApi(APIView):
    def get_permissions(self):
        if self.request and self.request.method == 'POST':
            return [IsAdminUser(), ]
        return []

    def get_authenticators(self):
        if self.request and self.request.method == 'POST':
            return [JWTAuthentication(), ]
        super().get_authenticators()
        return []

    class PostInputSerializer(serializers.Serializer):
        seller = PkSlugRelatedField(slug_field='phone', queryset=BaseUser.objects.all())
        book = PkSlugRelatedField(slug_field='slug', queryset=Book.objects.all())
        title = serializers.CharField()
        description = serializers.CharField(max_length=255)
        price = serializers.IntegerField()
        links = serializers.DictField(child=serializers.CharField(max_length=255))
        tags = serializers.ListSerializer(child=serializers.CharField(max_length=255))

        def create(self, validated_data):
            return create_new_post(**validated_data)

    class PostOutputSerializer(serializers.Serializer):
        id = serializers.CharField(max_length=255)
        seller = PkSlugRelatedField(slug_field='phone', queryset=BaseUser.objects.all())
        book = PkSlugRelatedField(slug_field='slug', queryset=Book.objects.all())
        title = serializers.CharField()
        description = serializers.CharField(max_length=255)
        price = serializers.IntegerField()
        links = serializers.DictField(child=serializers.CharField(max_length=255))
        tags = serializers.ListSerializer(child=serializers.CharField(max_length=255))

        def get_seller(self, seller):
            return BaseUser.objects.get(pk=seller).phone
        # class Meta:
        #     model = Post
        #     fields = ('title', )

    @extend_schema(
        summary='create a new post',
        description='This endpoint create a new post for exists book.',
        request=PostInputSerializer,
        tags=['post', ],
    )
    def post(self, request):
        serializer = self.PostInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(
        summary='get post list',
        description='This endpoint get post list.',
        responses=PostOutputSerializer(many=True),
        tags=['post', ],
    )
    def get(self, request):
        serializer = self.PostOutputSerializer(instance=get_published_posts(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
