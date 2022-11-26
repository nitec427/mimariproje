from flask import Flask, render_template, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from helpers import read_img_files
import json


     
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mimari-proje'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/arch_db"
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pleasant = db.Column(db.Integer)
    interesting = db.Column(db.Integer)
    beautiful = db.Column(db.Integer)
    normal = db.Column(db.Integer)
    calm = db.Column(db.Integer)
    spacious = db.Column(db.Integer)
    bright = db.Column(db.Integer)
    open = db.Column(db.Integer)
    simple = db.Column(db.Integer)
    safe = db.Column(db.Integer)

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
]

questions_multiple_answers = {
1:("First floor use", "How good is the ground floor use of the buildings on the street in the image?", "Görseldeki sokaktaki binaların zemin kat kullanımını değerlendiriniz?", True),
2:("Proportion first floor with windows", "Is the proportion of the first floor windows of the buildings on the street sufficient in the image?", "Görseldeki cadde binalarının zemin katlarındaki pencere oranını yeterlilik açısından değerlendiriniz", True),
3:("Pavement Qualities", "How is the pavement quality (damage condition, continuity, width, etc.) of the street in the image?", "Görseldeki sokağın kaldırım kalitesini (hasar durumu, eni vs) değerlendiriniz", True),
4:("Scenery (Landscape, natural)", "Is the street in the image sufficient in terms of scenery, landscape and naturalness?", "Görseldeki sokağı; manzara ve peyzaj açısından değerlendiriniz", True),
5:("Pavement Continuity", "How is the continuity of the pavements on the street in the image?", "Görseldeki sokakta kaldırımların sürekliliği(kesintisizliği) nasıldır?", True),
6:("Street Linkage", "Is the linkage of the street in the image with other streets sufficient?", "Görseldeki sokağın diğer sokaklarla bağlantısını yeterlilik açısından değerlendiriniz", True),
7:("Building Scale", "Is the scale of the buildings on the street in the image compatible with the street?", "Görseldeki sokakta binaların ölçeği ile insan ölçeği arasındaki uyumu değerlendiriniz", True),
8:("Proportion Street Wall", "What is the proportion of the street wall in the image?", "Görüntüdeki sokak bina bloğunun kesintisiz uzunluğunu değerlendiriniz", True),
9:("Proportion Sky Across", "How much can you view the sky on the street in the image?", "Görseldeki sokakta gökyüzünü ne kadar görüntüleye biliyorsunuz?", True),
10:("Street Width", "Is the width of the street in the image sufficient?", "Görseldeki sokağın genişliği sizce yeterli midir? ", True),
11:("Vividness", "How vivid is the street in the image?", "Görüntüdeki sokağı canlı/yaşayan ve dinamik olması bakımından değerlendiriniz", True),
12:("Damaged Building", "What is the density of the damaged building on the street in the image?", "Görseldeki sokakta hasarlı yapı yoğunluğu ne kadardır?", False),
13:("Human Population", "Is the street in the image sufficient in terms of human density?", "Görseldeki caddede insan yoğunluğu nasıldır?", False),
14:("Car parking", "What is the density of cars parked on the street in the image?", "Görseldeki sokakta park halindeki araba yoğunluğu nasıldır?", False),
15:("All Street Furniture", "Does the street in the image have enough urban furniture?", "Görseldeki sokak, yeterli kent mobilyasına sahip midir?", False),
16:("Small Planters", "Is the density of small plants on the street in the image sufficient?", "Görseldeki sokakta küçük bitkilerin oranı nedir", False),
17:("Historical Buildings", "Are there historical buildings on the street in the image?", "Görseldeki sokakta tarihi binalar bulunmakta mıdır?", False),
18:("Contemporary building", "Are there contemporary buildings on the street in the image?", "Görseldeki sokakta çağdaş binalar var mıdır?", False),
19:("Urban Features (Courtyards/Plazas/Park)", "To what extent does the street in the image have urban features (Courtyards/Plazas/Park)?", "Görseldeki sokak kentsel özelliklere (Avlular/Plazalar/Park) ne ölçüde sahiptir?", False),
20:("Greenness", "Does the street in the image have enough greenery?", "Görseldeki sokakta yeşil oranı nasıldır", False),
21:("Accent Colour", "How intense are the accent colors on the street in the image?", "Resimde sokaktaki ön plana çıkan ve dikkat çeken renkli unsurların varlığını değerlendiriniz", False),
22:("Public space usage", "Is the available public space on the street in the image sufficient?", "Görseldeki sokakta kullanılabilir kamusal alan yeterli midir?", False),
23:("Community", "Evaluate the density of people interacting and spending time in the open area on the street in the image.", "Görseldeki sokakta açık alanda etkileşimde olan ve vakit geçiren insan yoğunluğunu değerlendiriniz?", False),
24:("Traffic Volume", "What is the traffic volume on the street in the image?", "Görselde cadde üzerindeki trafik yoğunluğunu değerlendiriniz", False)
}
q_list = list(questions_multiple_answers.values())

@app.route('/imageshow/<int:image_id>', methods=['GET', 'POST'])
def image_page(image_id):
        
    return render_template('image_page.html', image_id=image_id, range_questions=range_questions, questions_multiple_answers=q_list, color_theme="light", color_theme2 = "dark"  )


@app.route('/logout')
def logout_page():
    session.clear()
    return render_template('log_out.html')

@app.route('/postmethod', methods=['POST'])
def handle_form():
    if request.method == 'POST':
        jsdata = request.form['jsdata']     
        negative_samples = request.form['negative_samples']
        positive_samples = request.form['positive_samples']
        form_data_list = json.loads(jsdata)
        print(type(form_data_list))
        neg_samples_list = json.loads(negative_samples)
        pos_samples_list = json.loads(positive_samples)
        newEntry = Entry(pleasant=form_data_list[0]['value'], interesting=form_data_list[1]['value'],
                        beautiful=form_data_list[2]['value'], normal=form_data_list[3]['value'],
                        calm=form_data_list[4]['value'], spacious=form_data_list[5]['value'],
                        bright=form_data_list[6]['value'], open=form_data_list[7]['value'],
                        simple=form_data_list[8]['value'], safe=form_data_list[9]['value'])
        db.session.add(newEntry)
        db.session.commit()
        return redirect('/')

@app.route('/', methods=['GET', 'POST'])
def home_page():
    print('imdi geldin')
    session.clear()

    if "newsession" not in session:
        session['newsession'] = True
        session['password'] = ""
        session['username'] = ""
        session['logged_in'] = False
        session['labeling_mode'] = ""  # 0-> Only unlabeled, 1 -> All images labeled by me, 2 -> All images


    if request.method == 'GET':

        print(session)

        if not session['logged_in']:
            return render_template('home.html')
        else:
            return "You've logged in!!!!"
    else:
        print('post request geldi')
        if request.form['username'] != "a" or request.form['password'] != "a" :
            return "Wrong password or username"

        session['username'] = request.form['username']
        session['password'] = request.form['password']
        session['logged_in'] = True
        session['labeling_mode'] = request.form['image_classes']

        print(session)

        return redirect('/imageshow/1')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
