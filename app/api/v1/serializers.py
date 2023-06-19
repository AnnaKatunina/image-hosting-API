from rest_framework import serializers

from app.models import Account, Plan, Image, ImageVersion, ExpiringLink
from app.utils import create_copy


class CreateAccountSerializer(serializers.ModelSerializer):
    plan_id = serializers.CharField()

    class Meta:
        model = Account
        fields = ('plan_id',)

    def create(self, validated_data):
        user = self.context['request'].user
        plan = Plan.objects.get(id=validated_data.get('plan_id'))
        return Account.objects.create(user=user, plan=plan)


class ImageVersionsSerializer(serializers.ModelSerializer):
    height = serializers.IntegerField(source='thumbnail.height')
    link = serializers.SerializerMethodField()

    class Meta:
        model = ImageVersion
        fields = ('height', 'link')

    def get_link(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.thumbnail_link.url)


class ImageSerializer(serializers.ModelSerializer):

    original_image = serializers.SerializerMethodField()
    versions = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('original_image', 'versions')

    def get_original_image(self, obj):
        user = self.context.get('request').user
        request = self.context.get('request')
        if user.account.plan.is_presence_original_image:
            return request.build_absolute_uri(obj.image.url)

    def get_versions(self, obj):
        user = self.context.get('request').user
        request = self.context.get('request')
        thumbnails = user.account.plan.thumbnails.all()
        versions_queryset = obj.versions.select_related('thumbnail').filter(thumbnail__in=thumbnails)
        return ImageVersionsSerializer(versions_queryset, many=True, context={'request': request}).data


class CreateImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('image',)

    def validate(self, data):
        if data['image'].content_type not in ('image/jpeg', 'image/png'):
            raise serializers.ValidationError("Image must be JPG or PNG format.")
        return data

    def create(self, validated_data):
        account = self.context['request'].user.account
        return Image.objects.create(account=account, **validated_data)


class CreateExpiringLinkSerializer(serializers.ModelSerializer):
    image_id = serializers.CharField()

    class Meta:
        model = ExpiringLink
        fields = ('image_id', 'number_of_seconds')

    def create(self, validated_data):
        image = Image.objects.get(id=validated_data.get('image_id'))
        link = create_copy(image.image)
        return ExpiringLink.objects.create(image=image, link=link, **validated_data)
