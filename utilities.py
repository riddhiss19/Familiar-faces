import json
from linkedin_api import Linkedin
import requests as req
import cv2
import google.generativeai as genai
import sys


def getLinkedInProfile(profileid):
    password = open("secret.key").read()
    api = Linkedin("riddhiss19@gmail.com", "sakshi@pn")

    recent_post = api.get_profile_posts(profileid)

    return recent_post[:4]


def getLiProfileData(profileid):
    password = open("secret.key").read()
    api = Linkedin("riddhiss19@gmail.com", "sakshi@pn")

    recent_post = api.get_profile(profileid)
    with open("sample.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(recent_post))
    return recent_post


def getGithubData(profileid):
    projects = req.get(
        f"https://api.github.com/users/{profileid}/repos?sort=created&direction=desc"
    ).json()

    return projects[:10]


def detectFace(imagePath) -> int:

    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = faceCascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=3, minSize=(30, 30)
    )

    return len(faces)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def getPersona(text):
    genai.configure(api_key="AIzaSyBAESdw0y1QQancJ7Bb9ICpc-rUxi2cHrY")
    model = genai.GenerativeModel("gemini-pro")
    if text != "":
        print(f"Processing string:   {text}")
        res = f' By using give statement :  "{ text }", categorize user into "Gym Freak", "Social Butterfly", "Knowledge Seeker" and only give me in output'
        print(res)
        response = model.generate_content(res)
        gen_text = ""
        for chunk in response:
            print(chunk.text)
            gen_text += chunk.text

        summary = ""
        print(f"Processing string:   {text}")
        res = f' By using give statement :  "{ text }", give 3 lines short summary about personality of user and only give me summary'
        print(res)
        response = model.generate_content(res)
        for chunk in response:
            print(chunk.text)
            summary += chunk.text

        exp = ""
        print(f"Processing string:   {text}")
        res = f' By using give statement :  "{ text }", give Area of Interests and just return one'
        print(res)
        response = model.generate_content(res)
        for chunk in response:
            print(chunk.text)
            exp += chunk.text

        return [gen_text, summary, exp]
