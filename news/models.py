import datetime
from datetime import timedelta

from django.db import models
from django.utils import timezone


# Create your models here.

class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(null=False, max_length=64, verbose_name="Назва")
    content = models.CharField(null=False, max_length=1024, verbose_name="Контент")
    photo_content = models.ImageField(default="default.png", verbose_name="Фотографія")
    date_of_pub = models.DateTimeField(null=False, default=timezone.now(),
                                       verbose_name="Дата публікації")

    class Meta:
        verbose_name_plural = 'Новини'
        verbose_name = "оголошення"

    def __str__(self):
        return f"{self.news_id}) {self.title}: {self.date_of_pub + timedelta(hours=3 if datetime.datetime.fold == 0 else 2)}"

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.news_id})'

    @staticmethod
    def get_by_id(id):
        news = News.objects.filter(news_id=id)[0]

        if news:
            return news
        else:
            raise "Оголошення не знайдено"

    @staticmethod
    def delete_by_id(id):
        if News.objects.filter(news_id=id).delete()[0] == 0:
            return True
        else:
            raise "Оголошення не знайдено"

    @staticmethod
    def create(title, content, image='default.png'):
        if len(title) < 5:
            return None
        else:
            news = News(title=title, content=content, image=image, date_of_pub=timezone.now())
            news.save()

            return True

    def to_dict(self):
        return {
            "id": self.news_id,
            "title": self.title,
            "content": self.content,
            "date_of_pub": self.date_of_pub,
        }

    def update(self, title=None, content=None):
        if title:
            self.title = title

        if content:
            self.content = content

        return None

    @staticmethod
    def get_all():
        return News.objects.all()
