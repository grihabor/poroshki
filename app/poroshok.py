from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app import Base


class Poroshok(Base):
    __tablename__ = 'poroshki'

    id = Column(Integer, primary_key=True)
    text = Column(String(1024, convert_unicode=True), nullable=False)
    posted = Column(DateTime)
    like_count = Column(Integer)
    repost_count = Column(Integer)

    def __init__(self, id, text, timestamp, like_count, repost_count):
        if not isinstance(id, int):
            raise TypeError('id must be int, found: {}'.format(type(id)))
        if not isinstance(text, str):
            raise TypeError('text must be str, found: {}'.format(type(text)))
        if not isinstance(timestamp, int):
            raise TypeError('timestamp must be int, found: {}'.format(type(timestamp)))
        if not isinstance(like_count, int):
            raise TypeError('like_count must be int, found: {}'.format(type(like_count)))
        if not isinstance(repost_count, int):
            raise TypeError('repost_count must be int, found: {}'.format(type(repost_count)))

        self.like_count = like_count
        self.repost_count = repost_count
        self.text = text
        self.posted = datetime.fromtimestamp(timestamp)
        self.id = id

    def __repr__(self):
        return '<Poroshok [id:{}]>'.format(self.id)

