from io import BytesIO
from PIL import Image as ImagePil

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.api.v1.tests.factories import UserFactory, PlanBasicFactory, AccountFactory, ImageFactory, \
    PlanEnterpriseFactory
from app.models import Account, Image


class TestCreateAccount(APITestCase):
    def setUp(self):
        self.url = reverse('create_account')
        self.user = UserFactory()
        self.plan = PlanBasicFactory()

    def test_create_account_unauthorized(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_create_account(self):
        self.client.force_authenticate(self.user)
        data_create_account = {
            'plan_id': self.plan.id,
        }
        response = self.client.post(
            self.url,
            data=data_create_account,
        )
        account = Account.objects.filter(user_id=self.user.id, plan_id=self.plan.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(account.count(), 1)


class TestCreateImage(APITestCase):
    def setUp(self):
        self.url = reverse('images')
        self.account = AccountFactory()

    def generate_image_file(self):
        up_file = BytesIO()
        img = ImagePil.new('RGB', (100, 100))
        img.save(fp=up_file, format='PNG')
        image = SimpleUploadedFile('image.png', up_file.getvalue(), content_type='image/png')
        return image

    def test_create_image(self):
        self.client.force_authenticate(self.account.user)
        data_create_image = {
            'image': self.generate_image_file(),
        }
        response = self.client.post(
            self.url,
            data=data_create_image,
        )
        image = Image.objects.filter(account=self.account)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(image.count(), 1)


class TestListImage(APITestCase):
    def setUp(self):
        self.url = reverse('images')
        self.account = AccountFactory()
        self.images = [ImageFactory(image__filename=f'image_name_{i}', account=self.account) for i in range(5)]

    def test_list_images(self):
        self.client.force_authenticate(self.account.user)
        response = self.client.get(self.url)
        images = Image.objects.filter(account=self.account)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(images.count(), 5)


class TestPermissionCreateExpiringLink(APITestCase):
    def setUp(self):
        self.url = reverse('create_expiring_link')
        self.account = AccountFactory()
        self.image = ImageFactory(image__filename='image__test_name', account=self.account)

    def test_no_permission(self):
        self.client.force_authenticate(self.account.user)
        data_create_expiring_link = {
            'image_id': self.image.id,
            'number_of_seconds': 300
        }
        response = self.client.post(
            self.url,
            data=data_create_expiring_link
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You can not create expiring links to images on your current plan.')


class TestCreateExpiringLink(APITestCase):
    def setUp(self):
        self.url = reverse('create_expiring_link')
        self.plan = PlanEnterpriseFactory()
        self.account = AccountFactory(plan=self.plan)
        self.image = ImageFactory(image__filename='image__test_name', account=self.account)

    def test_create_expiring_link(self):
        self.client.force_authenticate(self.account.user)
        data_create_expiring_link = {
            'image_id': self.image.id,
            'number_of_seconds': 300
        }
        response = self.client.post(
            self.url,
            data=data_create_expiring_link
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
