import vk

from app.poroshok import Poroshok


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

    def load_post_list(self, count=None):
        if not count:
            count = 100
        elif count > 100:
            raise ValueError('count must be < {}, found: {}'.format(100, count))
        self.post_count, *post_list = self.api('wall.get',
            owner_id=self.group_id,
            filter='owner',
            count=100,
            offset=1,
            fields=['id', 'name']
        )
        return post_list

    def get_poroshok_list(self, count=None):
        post_list = self.load_post_list(count)
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
