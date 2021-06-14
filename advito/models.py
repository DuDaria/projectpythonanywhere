from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from .validators import validate_birth_date


def user_directory_path(instance, filename):
    return f'user_{instance.author.id}/posts/{filename}'

def user_avatar_path(instance, filename):
	return f'user_{instance.user.id}/avatar/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile') 
    birth_date = models.DateField(verbose_name='Дата рождения', blank=True, null=True, validators=[validate_birth_date])
    about = models.TextField(verbose_name="Информация о пользователе", blank=True, max_length=300)
    phone = models.CharField(verbose_name="Телефон", null=True, blank=True, max_length=50)
    avatar = models.ImageField(verbose_name="Фото пользователя", upload_to=user_avatar_path)
    town = models.CharField(verbose_name="Город", null=True, blank=True, max_length=30)
    subscribers = models.ManyToManyField(User, blank=True, verbose_name="Подписчики пользователя", related_name='subscribers') 

    def __str__(self):
        return f'{self.user}'


class CategoryPost(models.Model):
    """Категория объявления"""
    name_category = models.CharField(verbose_name="Категория", max_length=100)

    def __str__(self):
        return f'{self.name_category}'


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryPost, on_delete=models.CASCADE, verbose_name="Категория", related_name='category')
    price = models.FloatField(verbose_name="Цена", blank=True)
    name_descript = models.CharField(max_length=200,  blank=True, verbose_name="Название объявления")
    description = models.TextField(max_length=1000, blank=True, verbose_name="Описание объявления")
    image = models.ImageField(upload_to=user_directory_path, verbose_name="Фото объявления")
    date_pub = models.DateTimeField(default=timezone.now, verbose_name="Дата объявления")
    date_edit = models.DateTimeField(default=timezone.now, verbose_name="Дата редактирования")
    
    def __str__(self):
        return f'Post: {self.name_descript}; {self.category}; Autor: {self.author}'

    class Meta:
        ordering=['-date_pub']


class FavoritePost(models.Model):
    """Избранное объявление"""
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name="Объявление", on_delete=models.CASCADE)
    

class Comment(models.Model):
    """Комментарий к посту"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=700)
    in_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Autor: {self.author}; Date_publish: {self.date_publish}'


class Review(models.Model):
    """Отзыв о пользователе"""
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Автор отзыва")
    to_whom = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Кому отзыв")
    rating = models.IntegerField(verbose_name="Оценка", null=True, blank=True)
    text = models.TextField(verbose_name="Отзыв", blank=True, max_length=300)
    date_pub = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    date_edit = models.DateTimeField(default=timezone.now, verbose_name="Дата редактирования")

    def __str__(self):
        return f'Autor: {self.author}; To whom: {self.to_whom}; Date_publish: {self.date_pub}'
    

class Message(models.Model):
    """Сообщение"""
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Автор сообщения")
    to_whom = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Кому сообщение")
    in_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    text = models.TextField(verbose_name="Сообщение", blank=True, max_length=300)
    date_pub = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    date_edit = models.DateTimeField(default=timezone.now, verbose_name="Дата редактирования")

    def __str__(self):
        return f'Author: {self.author}; To whom: {self.to_whom}; Date_publish: {self.date_pub}'
