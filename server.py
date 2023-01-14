from flask import Flask
from flask_login import LoginManager
from passlib.hash import pbkdf2_sha256 as hasher
import sqlite3 as dbapi2
import os

import views
from database import Database
from login_management import get_user, User
from helpers import read_img_files

# İstenen şeyler

# Back-endde tutulacak kullanıcıların username ve passwordları
# Kullanıcıya güncelleme seçeneği koyulmadı.


# TODO:
# Read unprocessed images only
# Resimler işlendiğinde unprocessed kısmından kaldırma çünkü serverde tek bir klassörde tutuluyor. (Bunu yapmak için
# database'de bir column daha olabilir. (Image id, user id combined. Böylelikle sürekli kontrol edip eğer kullanıcı
# işlemişe labeled kısmında gösterebilirim.))#

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
    app.add_url_rule('/imageshow/<int:image_path>/<int:image_id>', methods=['GET', 'POST'], view_func=views.image_page)
    app.add_url_rule('/postmethod', methods=['POST'], view_func=views.handle_form)

    lm.init_app(app)
    lm.login_view = "login_page"

    home_dir = os.getcwd()
    db = Database(os.path.join(home_dir, "archDB.db"))
    app.config["dbconfig"] = db

    # CREATE Database if not exist
    if (os.path.exists('./archDB.db') == False):
        con = dbapi2.connect("archDB.db")

        con.execute(
            """CREATE TABLE ENTRIES (ID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, pleasant INTEGER, interesting INTEGER,
            beautiful INTEGER, normal INTEGER, calm INTEGER, spacious INTEGER, bright INTEGER, opennes INTEGER, simpleness INTEGER, 
            safe INTEGER, firstFloorUse INTEGER, prop1FloorWind INTEGER, pavementQuality INTEGER, scenery INTEGER, pavementContinuity INTEGER,
            streetLink INTEGER, buildingScale INTEGER, propStreetWall INTEGER, propSkyAcross INTEGER, streetWidth INTEGER,
            vivid INTEGER, damagedBuilding INTEGER, humanPopulation INTEGER, carParking INTEGER, allStreetFurn INTEGER,
            smallPlant INTEGER, histBuildings INTEGER, contemporaryBuildings INTEGER, urbanFeat INTEGER, greenness INTEGER,
            accentColor INTEGER, publicSpaceUsage INTEGER, community INTEGER, trafficVol INTEGER, posSamples CLOB, negSamples CLOB)""")

        con.execute("CREATE TABLE USERS (Username TEXT PRIMARY KEY, Password TEXT)")

        # Create first user
        username = "admin"
        password = hasher.hash("admin")

        new_user = User(username, password)
        db.addUser(new_user)
        con.close()

    return app


if __name__ == '__main__':
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host='0.0.0.0', port=port)
