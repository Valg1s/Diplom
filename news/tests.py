from django.test import TestCase

from .models import News


class NewsTestCases(TestCase):
    def setUp(self):
        News.create("Перенесення гри", "Гра переноситься на 15.01")

    def test_add_news_wrong_value(self):
        #We have if block,where if title length lower than 5 chars ?must return False
        self.assertFalse(News.create("Er","Трохи контексту"),"Add wrong news first")
        self.assertFalse(News.create("Eror", "Трохи контексту"), "Add wrong news second")

    def test_get_all(self):
        # I'm testing this function by method len() ,cuz class ,what will be returned, is QuerySet
        news = News.get_all()
        self.assertEqual(len(news),1,f"Length of news is {len(news)} but mest be 1 ")

    def test_filter_by_title(self):
        news = News.objects.filter(title="Перенесення гри").first()
        self.assertEqual(news.title,"Перенесення гри", f"News title is {news.title} ,but must be 'Перенесення гри'")

    def test_get_by_id(self):
        first_news = News.objects.all().first()
        second_news = News.get_by_id(first_news.news_id)

        self.assertEqual(first_news,second_news,f"First news is {first_news} , second news is {second_news}")

    def test_update(self):
        news = News.objects.all().first()

        news.update(content="Змінений контент")

        updated_news = News.objects.all().first()

        self.assertEqual(updated_news.content , "Змінений контент", f"Updated content is {updated_news.content} "
                                                                    f",but must be 'Змінений контент'")

    def test_delete_by_id(self):
        news = News.get_all().first()

        News.delete_by_id(news.news_id)

        updated_news = News.get_all()

        self.assertEqual(len(updated_news),0,f"The QuerySet length is {len(updated_news)} , when must be 0")

