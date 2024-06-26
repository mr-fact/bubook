from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView as TOPV, TokenRefreshView as TRV, TokenVerifyView as TVV


class TokenObtainPairView(TOPV):
    @extend_schema(tags=['jwt authentication'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshView(TRV):
    @extend_schema(tags=['jwt authentication'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyView(TVV):
    @extend_schema(tags=['jwt authentication'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


