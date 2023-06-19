import factory
from django.contrib.auth.models import User

from app.models import Account, Plan, Image


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('first_name')
    password = factory.PostGenerationMethodCall('set_password', 'admin')


class PlanBasicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Plan

    name = 'Basic'


class PlanEnterpriseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Plan

    name = 'Enterprise'
    is_presence_original_image = True
    is_expiring_link = True


class AccountFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Account

    user = factory.SubFactory(UserFactory)
    plan = factory.SubFactory(PlanBasicFactory)


class ImageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Image

    account = factory.SubFactory(AccountFactory)
    image = factory.django.ImageField()
