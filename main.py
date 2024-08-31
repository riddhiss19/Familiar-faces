import os
from flask import Flask, flash, render_template, url_for, redirect, request
from werkzeug.utils import secure_filename
from database import addUser, getData
from face_detect import recognize_faces
from utilities import (
    allowed_file,
    detectFace,
    getGithubData,
    getLiProfileData,
    getLinkedInProfile,
    getPersona,
)
import variables

UPLOAD_FOLDER = "uploads"

names = ["None", "Dharmaraj", "Vikram"]
app = Flask(__name__, template_folder="templates")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    if variables.loggedin is None:
        return redirect("/signup", code=302)
    face = recognize_faces()
    if face is False:
        return redirect("/", code=302)

    print("Face found : " + str(face))

    return redirect("/profile/" + str(face), code=302)


@app.route("/profile/<int:userid>")
def get_profile(userid):
    if variables.loggedin is None:
        return redirect("/signup", code=302)
    print(userid)
    data = getData(userid)

    print(data)

    print(data[5])
    githubData = getGithubData(data[5])
    linkedin = getLinkedInProfile(data[4])
    url = f"https://api.multiavatar.com/{data[1]}.svg"
    lang_url = f"https://github-readme-stats.vercel.app/api/top-langs?username={data[5]}&show_icons=true&locale=en&layout=compact"
    print("lang url : ", lang_url)
    return render_template(
        "display.html",
        data=data,
        githubData=githubData,
        linkedin=linkedin,
        url=url,
        langurl=lang_url,
    )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if variables.loggedin is not None:
        return redirect("/", code=302)

    if request.method == "POST":
        firstname = request.form["first_name"]
        lastname = request.form["last_name"]
        password = request.form["password"]
        linkedin = request.form["linked_url"]
        github = request.form["git_url"]
        about = request.form["about_user"]
        dob = request.form["dob"]

        if "image" not in request.files:
            return redirect(request.url)
        file = request.files["image"]

        if file.filename == "":
            return redirect(request.url)
        if file and allowed_file(file.filename):
            complete_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(complete_path)
            faces = detectFace(complete_path)
            if faces > 1:
                return redirect(request.url)

            if faces == 0:
                return redirect(request.url)

            print(faces)

            linkedindata = getLinkedInProfile(linkedin)
            liData = getLiProfileData(linkedin)
            loc = liData["geoLocationName"] + "," + liData["geoCountryName"]
            string = ""

            for lk in linkedindata:
                string += lk["commentary"]["text"]["text"]

            [persona, summary, exp] = getPersona(about + string)

            userid = addUser(
                firstname,
                lastname,
                password,
                linkedin,
                github,
                about,
                persona,
                dob,
                summary=summary,
                location=loc,
                expertise=exp,
            )

            extension = file.filename.split(".")[-1]

            os.rename(
                complete_path,
                os.path.join(
                    app.config["UPLOAD_FOLDER"], (str(userid) + "." + extension)
                ),
            )

            variables.loggedin = userid
            return redirect("/", code=302)
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=8000)
