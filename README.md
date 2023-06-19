# Image-hosting-API

## Description
The Image Hosting API project is a Django-based application that allows users to upload an image in PNG or JPG format.
It supports three account plans (Basic, Premium, and Enterprise) with varying privileges, including different thumbnail sizes, access to the original image, and the ability to generate expiring links. Admins have the flexibility to create plans with configurable attributes, such as thumbnail sizes and the inclusion of expiring links for uploaded images.

## Requirements
- Python 3.10
- Docker

## Installing and usage
- Clone the repository
```
git clone git@github.com:AnnaKatunina/image-hosting-API.git
```
- Build the Docker container
```
docker-compose up --build
```
- Create a superuser to access the admin panel
```
docker exec -ti image_hosting_app python manage.py createsuperuser
```
- Access the Django admin panel by navigating to http://localhost:8000/admin/ in your web browser. Log in using the credentials of the superuser account created in the previous step.
- Run tests
```
docker exec -ti image_hosting_app python manage.py test
```

## API

The API provides the following endpoints:

- [POST] ```/api/v1/create_account/```: Creates a new account where the user can choose a plan.
- [POST] ```/api/v1/images/```: Creates a new image.
- [GET] ```/api/v1/images/```: Retrieves all images with their thumbnails.
- [POST] ```/api/v1/expiring_link_create/```: Creates a new expiring image link according to the user's plan.

#### Example of GET ```/api/v1/images/``` endpoint:
```
[
    {
        "original_image": "http://localhost:8000/media/images/file_name_1.png",
        "versions": [
            {
                "height": 200,
                "link": "http://localhost:8000/media/thumbnails/images/file_name_1.png"
            },
            {
                "height": 400,
                "link": "http://localhost:8000/media/thumbnails/images/file_name_1_LVNAGRi.png"
            }
        ]
    },
    {
        "original_image": "http://localhost:8000/media/images/file_name_2.jpg",
        "versions": [
            {
                "height": 200,
                "link": "http://localhost:8000/media/thumbnails/images/file_name_2.jpg"
            },
            {
                "height": 400,
                "link": "http://localhost:8000/media/thumbnails/images/file_name_2_C9eVQjP.jpg"
            }
        ]
    }
]
```