from django.urls import path

from app.api.v1.views import CreateAccountAPIView, ImageAPIView, CreateExpiringLinkAPIView

urlpatterns = [
    path('create_account/', CreateAccountAPIView.as_view(), name='create_account'),
    path('images/', ImageAPIView.as_view(), name='images'),
    path('expiring_link_create/', CreateExpiringLinkAPIView.as_view(), name='create_expiring_link'),
]
