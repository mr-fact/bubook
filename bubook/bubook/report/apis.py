from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from bubook.report.selectors import get_technical_reports
from bubook.report.services import create_new_technical_report


class TechnicalReportAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    class TechnicalReportOutputSerializer(serializers.Serializer):
        _id = serializers.CharField(default='66a28a5d1dd2c6911baf4e4f')
        created_at = serializers.DateTimeField()
        status = serializers.CharField(default='created')
        tag = serializers.CharField(default='باگ امنیتی')
        title = serializers.CharField(default='باگ امنیتی بخش فلان')
        description = serializers.CharField(
            default='پس از انجام فلان کار در بخش فلان مشاهده میشود که فلان مشکل به وجود میاید')

    class TechnicalReportInputSerializer(serializers.Serializer):
        tag = serializers.CharField(max_length=125)
        title = serializers.CharField(max_length=125)
        description = serializers.CharField(max_length=125)

        def create(self, validated_data):
            user = self.context.get('request').user
            return create_new_technical_report(user, validated_data['tag'],
                                               validated_data['title'], validated_data['description'])

    @extend_schema(
        summary='create a new technical report',
        description='This endpoint create a technical report.',
        request=TechnicalReportInputSerializer,
        tags=['report', ],
    )
    def post(self, request):
        serializer = self.TechnicalReportInputSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'report_id': str(serializer.instance)}, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary='get all created technical reports',
        description='This endpoint retrieve all created technical reports.',
        responses=TechnicalReportOutputSerializer(many=True),
        tags=['report', ],
    )
    def get(self, request):
        technical_reports = get_technical_reports(user_id=request.user.id)
        return Response(data=technical_reports, status=status.HTTP_200_OK)
