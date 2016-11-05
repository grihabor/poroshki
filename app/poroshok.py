from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app import Base


class Poroshok(Base):
    __tablename__ = 'poroshki'

    id = Column(Integer, primary_key=True)
    text_length = Column(Integer)
    text = Column(String(512, convert_unicode=True), nullable=False)
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
        self.text = self.process_text(text)
        self.text_length = len(self.text)
        self.posted = datetime.fromtimestamp(timestamp)
        self.id = id

    def __repr__(self):
        return '<Poroshok [id:{}]>'.format(self.id)

    def process_text(self, text):
        """
        Takes poroshok text and performs formatting.
        :param text:
            poroshok text
        :return: str:
            returns formatted poroshok text or empty string for non-poroshok
        """

        # skip if long text
        if len(text) > 512:
            return ''

        lines = []
        ok = False

        for line in text.split('<br>'):
            line = line.strip()
            if not line:
                continue

            lines.append(line)
            # if author in the line then break the loop
            if '©' in line or '(c)' in line or '(с)' in line:
                if len(lines) < 5:
                    break
                ok = True
                break

        text = '\n'.join(lines) if ok else ''
        return text

