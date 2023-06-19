from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from app.api.v1.serializers import CreateAccountSerializer, ImageSerializer, CreateImageSerializer, \
    CreateExpiringLinkSerializer
from app.models import Image
from app.permissions import IsExpiringLinkCreate


class CreateAccountAPIView(CreateAPIView):
    serializer_class = CreateAccountSerializer
    permission_classes = (IsAuthenticated, )


class ImageAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateImageSerializer
        return ImageSerializer

    def get_queryset(self):
        account = self.request.user.account
        return Image.objects.filter(account=account)


class CreateExpiringLinkAPIView(CreateAPIView):
    serializer_class = CreateExpiringLinkSerializer
    permission_classes = (IsExpiringLinkCreate, )
