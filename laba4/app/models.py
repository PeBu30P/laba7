"""
Definition of models.
"""
from datetime import datetime
from django.db import models
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    title = models.CharField(
        max_length=100,
        unique_for_date="posted",
        verbose_name= u"Заголовок",
    )
    descripstion = models.TextField(verbose_name = u"Краткое содержание")
    content = models.TextField(verbose_name = u"Полное содержание")
    posted = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name=u"Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")

    image = models.FileField(default="temp.jpg", verbose_name="Путь к картинке")

    def get_absolute_url(self):
        """Возвращает уникальный url адрес записи"""

        return reverse("blogpost", args=[str(self.id)])
    
    def __str__(self):
        """В качестве представления статей используются их названия"""
        
        return self.title

    class Meta:
        db_table = "Posts"
        ordering = ["-posted"] # сортировка данных по убыванию даты публикатсии
        verbose_name = u"статья блога"
        verbose_name_plural = u"статья блога"
    
class Comment(models.Model):
    text = models.TextField(verbose_name="Комментарий")
    date = models.DateTimeField(
        default=datetime.now(), db_index=True, verbose_name="Дата"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья")

    def __str__(self):
        return f"Комментарий {self.author} к {self.post}"

    class Meta:
        db_table = "Comments"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии к статьям блога"
        ordering = ["-date"]

admin.site.register(Blog)
admin.site.register(Comment)