from flask import render_template, session, request, redirect, current_app, url_for
from passlib.hash import pbkdf2_sha256 as hasher
import json
from login_management import User
from models import Entry
from helpers.questions import (
    range_questions,
    negative_tags,
    positive_tags,
    questions_multiple_answers,
)
from helpers import read_img_files


def home_page():
    db = current_app.config["dbconfig"]
    session.clear()

    if "newsession" not in session:
        session["newsession"] = True
        session["password"] = ""
        session["username"] = ""
        session["logged_in"] = False
        # 0-> Only unlabeled, 1 -> All images labeled by me, 2 -> All images
        session["labeling_mode"] = ""

    if request.method == "GET":
        if not session["logged_in"]:
            return render_template("home.html")
        else:
            return "You've logged in!!!!"

    else:
        if db.getPassword(request.form["username"]) == None:
            return "Wrong username"
        elif not hasher.verify(
            request.form["password"], db.getPassword(request.form["username"])
        ):
            return "Wrong password"

        session["username"] = request.form["username"]
        session["password"] = request.form["password"]

        session["logged_in"] = True

        # Kullanıcının son labelladığı resimden bir sonrakini göstereceğiz:
        image_id = db.getNextImage(session["username"])

        if image_id is None:
            print("NONE")
            return redirect(url_for("thankyou"))
        else:
            print("NOT NONE")
            return redirect(
                url_for(
                    "image_page", image_id=image_id, language=request.form["language"]
                )
            )


def thankyou():
    return render_template("thankyou.html")


def logout():
    session.clear()
    return redirect(url_for("home_page"))


def image_page(image_id, language):
    # Türkçe İngilizce config
    db = current_app.config["dbconfig"]

    # Image id'ye göre database'den path bulunuyor
    image_path = db.getImagePath(image_id)
    return render_template(
        "image_page.html",
        image_path=image_path,
        image_id=image_id,
        lang=language,
        range_questions=range_questions,
        questions_multiple_answers=list(questions_multiple_answers.values()),
        negatives=negative_tags,
        positives=positive_tags,
        color_theme="light",
        color_theme2="dark",
    )


def register_user():
    db = current_app.config["dbconfig"]

    if request.method == "GET":
        return render_template("register.html")

    else:
        if db.getPassword(request.form["username"]) != None:
            return "Username already exists"
        new_user = User(
            username=request.form["username"],
            password=hasher.hash(request.form["password"]),
        )
        db.addUser(new_user)
        return redirect(url_for("home_page"))


def handle_form():
    db = current_app.config["dbconfig"]

    if request.method == "POST":
        jsdata = request.form["jsdata"]
        negative_samples = request.form["negative_samples"]
        positive_samples = request.form["positive_samples"]
        image_id = request.form["image_id"]
        lang = request.form["language"]
        form_data_list = json.loads(jsdata)
        neg_samples_list = str(json.loads(negative_samples))
        pos_samples_list = str(json.loads(positive_samples))

        ### Prints ###
        print("neg samples : ", neg_samples_list)
        print("pos samples : ", pos_samples_list)
        print("User : ", session["username"])
        for item in form_data_list:
            print(item["name"], item["value"])

        default_value = -100

        newEntry = Entry(
            username=session["username"],
            image_id=image_id,
            pleasant=form_data_list[0]["value"],
            interesting=form_data_list[1]["value"],
            beautiful=form_data_list[2]["value"],
            normal=form_data_list[3]["value"],
            calm=form_data_list[4]["value"],
            spacious=form_data_list[5]["value"],
            bright=form_data_list[6]["value"],
            opennes=form_data_list[7]["value"],
            simpleness=form_data_list[8]["value"],
            safe=form_data_list[9]["value"],
            firstFloorUse=default_value
            if len(form_data_list) == 13
            else form_data_list[10]["value"],
            prop1FloorWind=default_value
            if len(form_data_list) == 13
            else form_data_list[11]["value"],
            pavementQuality=default_value
            if len(form_data_list) == 13
            else form_data_list[12]["value"],
            scenery=default_value
            if len(form_data_list) == 13
            else form_data_list[13]["value"],
            pavementContinuity=default_value
            if len(form_data_list) == 13
            else form_data_list[14]["value"],
            streetLink=default_value
            if len(form_data_list) == 13
            else form_data_list[15]["value"],
            buildingScale=default_value
            if len(form_data_list) == 13
            else form_data_list[16]["value"],
            propStreetWall=default_value
            if len(form_data_list) == 13
            else form_data_list[17]["value"],
            propSkyAcross=default_value
            if len(form_data_list) == 13
            else form_data_list[18]["value"],
            streetWidth=default_value
            if len(form_data_list) == 13
            else form_data_list[19]["value"],
            vivid=default_value
            if len(form_data_list) == 13
            else form_data_list[20]["value"],
            damagedBuilding=default_value
            if len(form_data_list) == 13
            else form_data_list[21]["value"],
            humanPopulation=default_value
            if len(form_data_list) == 13
            else form_data_list[22]["value"],
            carParking=default_value
            if len(form_data_list) == 13
            else form_data_list[23]["value"],
            allStreetFurn=default_value
            if len(form_data_list) == 13
            else form_data_list[24]["value"],
            smallPlant=default_value
            if len(form_data_list) == 13
            else form_data_list[25]["value"],
            histBuildings=default_value
            if len(form_data_list) == 13
            else form_data_list[26]["value"],
            contemporaryBuildings=default_value
            if len(form_data_list) == 13
            else form_data_list[27]["value"],
            urbanFeat=default_value
            if len(form_data_list) == 13
            else form_data_list[28]["value"],
            greenness=default_value
            if len(form_data_list) == 13
            else form_data_list[29]["value"],
            accentColor=default_value
            if len(form_data_list) == 13
            else form_data_list[30]["value"],
            publicSpaceUsage=default_value
            if len(form_data_list) == 13
            else form_data_list[31]["value"],
            community=default_value
            if len(form_data_list) == 13
            else form_data_list[32]["value"],
            trafficVol=default_value
            if len(form_data_list) == 13
            else form_data_list[33]["value"],
            walkability=default_value
            if len(form_data_list) == 13
            else form_data_list[34]["value"],
            pedAccessibilityWalkability=default_value
            if len(form_data_list) == 13
            else form_data_list[35]["value"],
            aestheticWalkability=default_value
            if len(form_data_list) == 13
            else form_data_list[36]["value"],
            posSamples=pos_samples_list,
            negSamples=neg_samples_list,
        )

        db.addEntry(newEntry)

        # Random image id alınıyor:
        next_image_id = db.getNextImage(username=session["username"])

        # Aşağıdaki redirect AJAX nedeniyle çalışmıyor
        if next_image_id is None:
            return url_for("thankyou")
        else:
            return url_for("image_page", image_id=next_image_id, language=lang)
