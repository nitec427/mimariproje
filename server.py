from flask import Flask
from flask_login import LoginManager
import os
# To-Do
# Türkçe İngilizce seçeneği koy.
# Other seçeneğini ekle (Other seçeneği seçildiğinde bir input alanı açılacak)
# not walkableı kaldır
# tag page 7 olacak
# ilk sayfadaki yazı büyüyecek
# 
import views
from database import Database
from login_management import get_user, User
from helpers import read_img_files

lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    app.config['SECRET_KEY'] = 'mimari-proje'

    app.add_url_rule('/', methods=['GET', 'POST'], view_func=views.home_page)
    app.add_url_rule('/logout', view_func=views.logout)
    app.add_url_rule('/imageshow/<int:image_id>/<string:language>',
                     methods=['GET', 'POST'], view_func=views.image_page)
    app.add_url_rule(
        '/postmethod', methods=['POST'], view_func=views.handle_form)
    app.add_url_rule(
        '/register', methods=['GET', 'POST'], view_func=views.register_user)
    app.add_url_rule('/thankyou', view_func=views.thankyou)
    lm.init_app(app)
    lm.login_view = "login_page"

    home_dir = os.getcwd()
    db = Database(os.path.join(home_dir, "archDB.db"))
    app.config["dbconfig"] = db

    # Create database if not exists
    if (os.path.exists('./archDB.db') == False):
        db.create()
    return app


if __name__ == '__main__':
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host='0.0.0.0', port=port)
