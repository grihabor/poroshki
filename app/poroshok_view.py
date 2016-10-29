from flask_admin.contrib.sqla import ModelView
from flask import Markup


class PoroshokView(ModelView):
    column_searchable_list = ['text']
    column_formatters = dict(text=lambda v, c, m, p: Markup(m.text.replace('\n', '<br/>')).unescape())

    def render(self, template, **kwargs):
        kwargs['text'] = 'bal'
        r = super().render(template, **kwargs)
        r = Markup(r).unescape()
        return r