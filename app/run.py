
from app import db, PoroshokView, Poroshok
from flask import Flask, redirect
from flask_admin import Admin
from app.poroshok_loader import load_data

app = Flask(__name__)
app.jinja_env.trim_blocks = False
app.jinja_env.lstrip_blocks = False
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
admin = Admin(app, name='Poroshki', template_mode='bootstrap3')

admin.add_view(PoroshokView(Poroshok, db.session))

@app.route('/')
def admin():
    return redirect('/admin')

#load_data()

app.run(debug=False)