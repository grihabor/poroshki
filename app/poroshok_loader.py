import vk
import sqlalchemy
from app import Poroshok, db


def process_text(text):

    if len(text) > 1024:
        return False
    text = '\n'.join([line.strip() for line in text.split('<br>')])
    return text

class PoroshokLoader():
    def __init__(self):
        self.group_id = 'sandalporoshki'
        self.session = vk.Session()
        self.api = vk.API(self.session)
        self.group = self.api.groups.getById(
            group_id = self.group_id,
            fields=['description']
        )[0]
        self.group_id = '-{}'.format(self.group['gid'])

    def load_post_list(self, count=None, offset=None):
        if not count:
            count = 100
        elif count > 100:
            raise ValueError('count must be < {}, found: {}'.format(100, count))
        self.post_count, *post_list = self.api('wall.get',
            owner_id=self.group_id,
            filter='owner',
            count=count,
            offset=offset if offset else 0,
            fields=['id', 'name']
        )
        return post_list

    def get_poroshok_list(self, count=None, offset=None):
        post_list = self.load_post_list(count, offset)
        poroshok_list = []
        for post_json in post_list:
            id = post_json['id']
            date = post_json['date']
            text = process_text(post_json['text'])
            like_count = post_json['likes']['count']
            repost_count = post_json['reposts']['count']
            if not text:
                continue
            poroshok = Poroshok(id, text, date, like_count, repost_count)
            poroshok_list.append(poroshok)

        return poroshok_list

    #def get_full_poroshok_list(self):


def load_data():

    def is_in_db(id):
        query = db.session.query(
            Poroshok.id
        ).filter(Poroshok.id==id)
        try:
            query.one()
        except sqlalchemy.orm.exc.NoResultFound:
            return False
        return True

    loader = PoroshokLoader()

    i = 0
    total_count_added = 0
    total_count_loaded = 0

    while True:
        count_added = 0

        poroshok_list = loader.get_poroshok_list(offset=100*i)
        if not poroshok_list:
            break
        count_loaded = len(poroshok_list)

        for poroshok in poroshok_list:
            if not is_in_db(poroshok.id):
                db.session.add(poroshok)
                count_added += 1
        db.session.commit()

        print('iter {}: {} added - {} loaded'.format(i, count_added, count_loaded))
        i += 1
        total_count_added += count_added
        total_count_loaded += count_loaded

    print('Total: {} added - {} loaded'.format(total_count_added, total_count_loaded))
