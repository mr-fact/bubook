from django.urls import path

from bubook.report.apis import TechnicalReportAPIView

urlpatterns = [
    path('technical/', TechnicalReportAPIView.as_view(), name="post_report"),
]
