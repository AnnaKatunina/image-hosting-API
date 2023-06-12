# Image-hosting-API

## Installing and usage
- Clone the repository
```
git clone git@github.com:AnnaKatunina/image-hosting-API.git
```
- Build a docker container
```
docker-compose up --build
```
- Create superuser to access the admin panel
```
docker exec -ti image_hosting_app python manage.py createsuperuser
```
- Navigate to http://localhost:8000/admin/ to view the admin panel