import sqlalchemy
from database import db
from flask import Flask, redirect
from flask_admin import Admin
from poroshok_loader import PoroshokLoader
from poroshok_view import PoroshokView
from app.poroshok import Poroshok

app = Flask(__name__)
app.jinja_env.trim_blocks = False
app.jinja_env.lstrip_blocks = False
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
admin = Admin(app, name='Poroshki', template_mode='bootstrap3')


admin.add_view(PoroshokView(Poroshok, db.session))

loader = PoroshokLoader()
poroshok_list = loader.get_poroshok_list()

def is_in_db(id):
    query = db.session.query(
        Poroshok.id
    ).filter(Poroshok.id==id)
    try:
        query.one()
    except sqlalchemy.orm.exc.NoResultFound:
        return False
    return True

for poroshok in poroshok_list:
    if not is_in_db(poroshok.id):
        db.session.add(poroshok)
db.session.commit()


@app.route('/')
def admin():
    return redirect('/admin')

app.run(debug=True)