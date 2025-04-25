import os

import django
from django.contrib.auth.models import User
from dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
django.setup()


load_dotenv()
username = os.getenv("USERNAME")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Суперпользователь создан")
else:
    print("Суперпользователь уже существует")
