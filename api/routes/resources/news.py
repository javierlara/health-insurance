from flask_restful import Resource
from flask import abort, make_response, request
import flask as f
import api.models as models
from datetime import datetime
from api.db import db_session as session


class News(Resource):
    @staticmethod
    def get_news(news_id):
        return session.query(models.News).get(news_id)

    @staticmethod
    def delete_news(news):
        news.deleted_at = datetime.utcnow()
        session.commit()

    @staticmethod
    def update_news(news, data):
        news.update(data)
        session.commit()

    def get(self, news_id):
        news = self.get_news(news_id)
        if news is None:
            abort(404)
        return news.serialize()

    def put(self, news_id):
        news = self.get_news(news_id)
        if news is None:
            abort(404)
        data = request.get_json()
        self.update_news(news, data)
        f.flash('La noticia "' + news.title + '" fue editada con éxito')
        return news.serialize()

    def delete(self, news_id):
        news = self.get_news(news_id)
        if news is None:
            abort(404)
        self.delete_news(news)
        f.flash('La noticia "' + news.title + '" fue borrada con éxito')
        return make_response()


class NewsCollection(Resource):
    def get(self):
        newses = self.get_all_news()
        return [r.serialize() for r in newses]

    def post(self):
        data = request.get_json()
        new_news = self.add_new_news(data)
        f.flash('La noticia "' + new_news.title + '" fue creada con éxito')
        return new_news.serialize()

    @staticmethod
    def get_all_news():
        query = session.query(models.News).filter(models.News.deleted_at == None)
        return query.all()

    @staticmethod
    def add_new_news(data):
        news = models.News(
            title=data.get('title'),
            image=data.get('image'),
            content=data.get('content'),
            author_id=data.get('author_id')
        )

        session.add(news)
        session.commit()

        return news