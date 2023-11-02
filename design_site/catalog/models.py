from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from datetime import datetime

from django.template.backends import django


# Create your models here.
class CustomUser(AbstractUser):
    fio = models.CharField(max_length=100)
    email =  models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class DesignCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Request(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        max_size = 2.0
        if filesize > max_size * 1024 * 1024:
            raise ValidationError("Максимальный размер файла 2 МБ")
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(DesignCategory, on_delete=models.CASCADE, verbose_name='Категория')
    status = models.CharField(max_length=20, default="Новая", verbose_name='Статус')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    is_completed = models.BooleanField(default=False)
    # photo_of_room = models.ImageField(max_length=254, upload_to="media/", verbose_name="Фотография",
    #                                   help_text="Разрешается формата файла только jpg, jpeg, png, bmp",
    #                                   validators=[
    #                                       FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp']),
    #                                       validate_image])
    date_create = models.DateField(default=datetime.now(), verbose_name="Дата создания")
    time_create = models.TimeField(default=datetime.now(), verbose_name="Время создания")
    # date = models.DateTimeField(default=django.utils.timezone.now)
    def __str__(self):
        return self.title

    # def get_absolute_url(self):

    # """Returns the URL to access a detail record for this book."""
    #     return reverse('book-detail', args=[str(self.id)])
