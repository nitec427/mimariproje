from flask import Flask, render_template, session, request, redirect, current_app, url_for
from helpers import read_img_files
import json
import os
from database import Database
from models import Entry
import sqlite3 as dbapi2
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import LoginManager
from login_management import get_user, User

# İstenen şeyler

# Back-endde tutulacak kullanıcıların username ve passwordları
# Kullanıcıya güncelleme seçeneği koyulmadı.


# TODOs
# Read unprocessed images only
# Resimler işlendiğinde unprocessed kısmından kaldırma çünkü serverde tek bir klassörde tutuluyor. (Bunu yapmak için database'de bir column daha olabilir. (Image id, user id combined. Böylelikle sürekli kontrol edip eğer kullanıcı işlemişe labeled kısmında gösterebilirim.))
#

lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)



app = Flask(__name__)
app.config.from_object("settings")
app.config['SECRET_KEY'] = 'mimari-proje'
home_dir = os.getcwd()
db = Database(os.path.join(home_dir, "archDB.db"))

lm.init_app(app)
lm.login_view = "login_page"

# CREATE Database if not exist
if (os.path.exists('./archDB.db') == False):
    con = dbapi2.connect("archDB.db")

    con.execute(
        """CREATE TABLE ENTRIES (ID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, pleasant INTEGER, interesting INTEGER, beautiful INTEGER,
        normal INTEGER, calm INTEGER, spacious INTEGER, bright INTEGER, opennes INTEGER, simpleness INTEGER, safe INTEGER,
        firstFloorUse INTEGER, prop1FloorWind INTEGER, pavementQuality INTEGER, scenery INTEGER, pavementContinuity INTEGER,
        streetLink INTEGER, buildingScale INTEGER, propStreetWall INTEGER, propSkyAcross INTEGER, streetWidth INTEGER,
        vivid INTEGER, damagedBuilding INTEGER, humanPopulation INTEGER, carParking INTEGER, allStreetFurn INTEGER,
        smallPlant INTEGER, histBuildings INTEGER, contemporaryBuildings INTEGER, urbanFeat INTEGER, greenness INTEGER,
        accentColor INTEGER, publicSpaceUsage INTEGER, community INTEGER, trafficVol INTEGER, posSamples CLOB, negSamples CLOB)""")
    con.execute("CREATE TABLE USERS (Username TEXT PRIMARY KEY, Password TEXT)")
    username = "admin"
    password = hasher.hash("admin")
    print(username, password)
    new_user = User(username, password)
    db.addUser(new_user)
    con.close()

app.config["dbconfig"] = db

range_questions = [
    ("Unpleasant", "Pleasant"),
    ("Boring", "Interesting"),
    ("Ugly", "Beautiful"),
    ("Strange", "Normal"),
    ("Arousing", "Calm"),
    ("Narrow", "Spacious"),
    ("Dark", "Bright"),
    ("Enclosed", "Open"),
    ("Caotic", "Simple"),
    ("Unsafe", "Safe"),
    ("Not Walkable", 'Walkable'),
]

negative_tags = [(False, 'Graffiti'),
                 (True, 'Narrow'),
                 (False, 'Human'),
                 (True, 'Rubbish'),
                 (False, 'Traffic'),
                 (True, 'Stray Animal'),
                 (False, 'Lack of pavement'),
                 (True, 'Ruin'),
                 (False, 'Dark'),
                 (True, 'Lamp Post'),
                 (False, 'Obstacle'),
                 (True, 'Deserted'),
                 (False, 'Car')]
positive_tags = [(False, 'Tree'),
                 (True, 'Scenery'),
                 (False, 'Seaside/Waterways'),
                 (True, 'Human'),
                 (False, 'Landmark'),
                 (True, 'Street furniture'),
                 (False, 'Accent Colour'),
                 (True, 'Cultural Heritage'),
                 (False, 'Cultural Facilities'),
                 (True, 'Home'),
                 (False, 'Cafe/Restaurant'),
                 (True, 'Bright'),
                 (False, 'Shop/Market'),
                 (True, 'Landscape'),
                 (False, 'Animals'),
                 (True, 'Flower'),
                 (False, 'Public art')]

questions_multiple_answers = {1: ['Birinci kat kullanımı',
                                  'How good is the ground floor use of the buildings on the street in the image?',
                                  'Görseldeki sokaktaki binaların zemin kat kullanımını değerlendiriniz?',
                                  True,
                                  1],
                              2: ['Zemin kat cam yeterliliği',
                                  'Is the proportion of the first floor windows of the buildings on the street sufficient in the image?',
                                  'Görseldeki cadde binalarının zemin katlarındaki pencere oranını yeterlilik açısından değerlendiriniz',
                                  True,
                                  2],
                              3: ['Kaldırım Kalitesi',
                                  'How is the pavement quality (damage condition, continuity, width, etc.) of the street in the image?',
                                  'Görseldeki sokağın kaldırım kalitesini (hasar durumu, eni vs) değerlendiriniz',
                                  True,
                                  3],
                              4: ['Manzara ve Peyzaj',
                                  'Is the street in the image sufficient in terms of scenery, landscape and naturalness?',
                                  'Görseldeki sokağı; manzara ve peyzaj açısından değerlendiriniz',
                                  True,
                                  4],
                              5: ['Kaldırımların Sürekliliği(Kesintisizliği)',
                                  'How is the continuity of the pavements on the street in the image?',
                                  'Görseldeki sokakta kaldırımların sürekliliği(kesintisizliği) nasıldır?',
                                  True,
                                  5],
                              6: ['Sokaklar Arası Bağlantılar',
                                  'Is the linkage of the street in the image with other streets sufficient?',
                                  'Görseldeki sokağın diğer sokaklarla bağlantısını yeterlilik açısından değerlendiriniz',
                                  True,
                                  6],
                              7: ['Bina Ölçeği',
                                  'Is the scale of the buildings on the street in the image compatible with the street?',
                                  'Görseldeki sokakta binaların ölçeği ile insan ölçeği arasındaki uyumu değerlendiriniz',
                                  True,
                                  7],
                              8: ['Orantılı Sokak Duvarı',
                                  'What is the proportion of the street wall in the image?',
                                  'Görüntüdeki sokak bina bloğunun kesintisiz uzunluğunu değerlendiriniz',
                                  True,
                                  8],
                              9: ['Gökyüzü Oranı',
                                  'How much can you view the sky on the street in the image?',
                                  'Görseldeki sokakta gökyüzünü ne kadar görüntüleye biliyorsunuz?',
                                  True,
                                  9],
                              10: ['Cadde Genişliği',
                                   'Is the width of the street in the image sufficient?',
                                   'Görseldeki sokağın genişliği sizce yeterli midir? ',
                                   True,
                                   10],
                              11: ['Canlılık',
                                   'How vivid is the street in the image?',
                                   'Görüntüdeki sokağı canlı/yaşayan ve dinamik olması bakımından değerlendiriniz',
                                   True,
                                   11],
                              12: ['Hasarlı Yapı Yoğunluğu',
                                   'What is the density of the damaged building on the street in the image?',
                                   'Görseldeki sokakta hasarlı yapı yoğunluğu ne kadardır?',
                                   False,
                                   12],
                              13: ['İnsan Yoğunluğu',
                                   'Is the street in the image sufficient in terms of human density?',
                                   'Görseldeki caddede insan yoğunluğu nasıldır?',
                                   False,
                                   13],
                              14: ['Park halindeki arabalar',
                                   'What is the density of cars parked on the street in the image?',
                                   'Görseldeki sokakta park halindeki araba yoğunluğu nasıldır?',
                                   False,
                                   14],
                              15: ['Kent Mobilyası Oranı',
                                   'Does the street in the image have enough urban furniture?',
                                   'Görseldeki sokak, yeterli kent mobilyasına sahip midir?',
                                   False,
                                   15],
                              16: ['Küçük Bitkiler',
                                   'Is the density of small plants on the street in the image sufficient?',
                                   'Görseldeki sokakta küçük bitkilerin oranı nedir',
                                   False,
                                   16],
                              17: ['Tarihi Binalar',
                                   'Are there historical buildings on the street in the image?',
                                   'Görseldeki sokakta tarihi binalar bulunmakta mıdır?',
                                   False,
                                   17],
                              18: ['Çağdaş Binalar',
                                   'Are there contemporary buildings on the street in the image?',
                                   'Görseldeki sokakta çağdaş binalar var mıdır?',
                                   False,
                                   18],
                              19: ['Kentsel Özellikler (Courtyards/Plazas/Park)',
                                   'To what extent does the street in the image have urban features (Courtyards/Plazas/Park)?',
                                   'Görseldeki sokak kentsel özelliklere (Avlular/Plazalar/Park) ne ölçüde sahiptir?',
                                   False,
                                   19],
                              20: ['Yeşillik',
                                   'Does the street in the image have enough greenery?',
                                   'Görseldeki sokakta yeşil oranı nasıldır',
                                   False,
                                   20],
                              21: ['Ön Plandaki Renkli Unsurlar',
                                   'How intense are the accent colors on the street in the image?',
                                   'Resimde sokaktaki ön plana çıkan ve dikkat çeken renkli unsurların varlığını değerlendiriniz',
                                   False,
                                   21],
                              22: ['Kamusal Alan',
                                   'Is the available public space on the street in the image sufficient?',
                                   'Görseldeki sokakta kullanılabilir kamusal alan yeterli midir?',
                                   False,
                                   22],
                              23: ['Topluluk',
                                   'Evaluate the density of people interacting and spending time in the open area on the street in the image.',
                                   'Görseldeki sokakta açık alanda etkileşimde olan ve vakit geçiren insan yoğunluğunu değerlendiriniz?',
                                   False,
                                   23],
                              24: ['Trafik Yoğunluğu',
                                   'What is the traffic volume on the street in the image?',
                                   'Görselde cadde üzerindeki trafik yoğunluğunu değerlendiriniz',
                                   False,
                                   24]}
q_list = list(questions_multiple_answers.values())





@app.route('/imageshow/<int:image_path>/<int:image_id>', methods=['GET', 'POST'])
def image_page(image_path, image_id):
    print(image_path, image_id)
    path_dict = {
        1: "ahlat",
        2: 'foca',
        3: 'gerze',
        4: 'gokceada',
    }
    place = path_dict[image_path]

    return render_template('image_page.html', image_path=place, image_id=image_id, range_questions=range_questions, questions_multiple_answers=q_list, negatives=negative_tags, positives=positive_tags, color_theme="light", color_theme2="dark")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_page'))


@app.route('/postmethod', methods=['POST'])
def handle_form():
    if request.method == 'POST':
        jsdata = request.form['jsdata']
        negative_samples = request.form['negative_samples']
        positive_samples = request.form['positive_samples']
        form_data_list = json.loads(jsdata)
        neg_samples_list = str(json.loads(negative_samples))
        pos_samples_list = str(json.loads(positive_samples))
        print(neg_samples_list)
        print(pos_samples_list)
        print(session['username'])
        for item in form_data_list:
            print(item['name'], item['value'])

        myDB = current_app.config["dbconfig"]
        # create also user id
        newEntry = Entry(username=session['username'], pleasant=form_data_list[0]['value'], interesting=form_data_list[1]['value'], beautiful=form_data_list[2]['value'],
                         normal=form_data_list[3]['value'], calm=form_data_list[4]['value'], spacious=form_data_list[5]['value'],
                         bright=form_data_list[6]['value'], opennes=form_data_list[
                             7]['value'], simpleness=form_data_list[8]['value'],
                         safe=form_data_list[9]['value'], firstFloorUse=form_data_list[
                             10]['value'], prop1FloorWind=form_data_list[11]['value'],
                         pavementQuality=form_data_list[12]['value'], scenery=form_data_list[
                             13]['value'], pavementContinuity=form_data_list[14]['value'],
                         streetLink=form_data_list[15]['value'], buildingScale=form_data_list[
                             16]['value'], propStreetWall=form_data_list[17]['value'],
                         propSkyAcross=form_data_list[18]['value'], streetWidth=form_data_list[
                             19]['value'], vivid=form_data_list[20]['value'],
                         damagedBuilding=form_data_list[21]['value'], humanPopulation=form_data_list[
                             22]['value'], carParking=form_data_list[23]['value'],
                         allStreetFurn=form_data_list[24]['value'], smallPlant=form_data_list[
                             25]['value'], histBuildings=form_data_list[26]['value'],
                         contemporaryBuildings=form_data_list[27]['value'], urbanFeat=form_data_list[
                             28]['value'], greenness=form_data_list[29]['value'],
                         accentColor=form_data_list[30]['value'], publicSpaceUsage=form_data_list[
                             31]['value'], community=form_data_list[32]['value'],
                         trafficVol=form_data_list[33]['value'], posSamples=pos_samples_list, negSamples=neg_samples_list)
        db.addEntry(newEntry)
        print("go to next img")
        return redirect('/imageshow/1/2')


@app.route('/', methods=['GET', 'POST'])
def home_page():
    session.clear()

    if "newsession" not in session:
        session['newsession'] = True
        session['password'] = ""
        session['username'] = ""
        session['logged_in'] = False
        # 0-> Only unlabeled, 1 -> All images labeled by me, 2 -> All images
        session['labeling_mode'] = ""

    if request.method == 'GET':

        if not session['logged_in']:
            return render_template('home.html')
        else:
            return "You've logged in!!!!"
    else:
        print("Password = ", db.getPassword(request.form['username']))
        if db.getPassword(request.form['username']) == None:
            return "Wrong username"
        elif not hasher.verify(request.form['password'], db.getPassword(request.form['username'])):
            return "Wrong password"


        session['username'] = request.form['username']
        session['password'] = request.form['password']
        session['logged_in'] = True
        session['labeling_mode'] = request.form['image_classes']

        return redirect('/imageshow/1/1')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
