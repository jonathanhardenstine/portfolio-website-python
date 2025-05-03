from flask import Flask, render_template, request
import os
import smtplib
import requests
from datetime import datetime

def set_json_vars(endpoint):
    response = requests.get(endpoint)
    return response.json()

getJSONdata = True
skill_pages_json = ""
skill_types_contactform_json = ""
skill_types_json = ""
skills_list_json = ""

app = Flask(__name__)


@app.route('/')
def home():
    global getJSONdata, skill_pages_json, skill_types_contactform_json, skill_types_json, skills_list_json
    if getJSONdata:
        skill_pages_json = set_json_vars("https://api.npoint.io/3afde83d436a472e10fd")
        skill_types_contactform_json = set_json_vars("https://api.npoint.io/8b977176889f22eafcc3")
        skill_types_json = set_json_vars("https://api.npoint.io/adb8fcc1072339519069")
        skills_list_json = set_json_vars("https://api.npoint.io/702326b83c75afe88d45")
        getJSONdata = False

    data = {
        "pageTitle": "Home",
        "UpdatedDate": datetime.now().strftime(format='%Y')
    }
    return render_template(template_name_or_list="index.html", all_posts=data)

@app.route('/about')
def about():
    data = {
        "pageTitle": "About",
        "UpdatedDate": datetime.now().strftime(format='%Y')
    }
    return render_template(template_name_or_list="about.html", all_posts=data)

##################
# contact routing
##################

#def send_email(requestedProjectVal, requestorNameVal, requestorEmailVal, requestorCompanyVal, requestorPositionVal, skillTypeCheckedVal, skillCheckedVal):
    #email_message = f"Subject:New Message\n\nName: {}\nEmail: {}\nPhone: {}\nMessage:{}"
    #with smtplib.SMTP("smtp.gmail.com") as connection:
        #connection.starttls()
        #connection.login(os.environ['env_email'], os.environ['env_email_password'])
        #connection.sendmail(os.environ['env_email'], os.environ['env_email'], email_message)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    global skill_pages_json, skill_types_contactform_json
    data = {
        "pageTitle": "Contact",
        "UpdatedDate": datetime.now().strftime(format='%Y'),
        "SkillTypes": skill_types_contactform_json,
        "SkillPages": sorted([{"skillName": skill_pages_json[skill_page]["skillName"],
                               "display": "No" if skill_pages_json[skill_page]["skillPageDetail"] == "" else "Yes"} for
                              skill_page in skill_pages_json], key=lambda x: x["skillName"])
    }

    if request.method == "POST":
        formdata = request.form
        print(formdata)
        skillTypeChecked = [skillType for skillType in formdata if skillType == "skillTypeCheck*"]
        skillChecked = [skill for skill in formdata if skill == "skillCheck*"]
        print(skillTypeChecked)
        print(skillChecked)
        #send_email(formdata["requestedProject"], formdata["requestorName"], formdata["requestorEmail"], formdata["requestorCompany"], formdata["requestorPosition"], skillTypeChecked, skillChecked)
        return render_template(template_name_or_list="contact.html", all_posts=data, msg_sent=True)

    return render_template(template_name_or_list="contact.html", all_posts=data, msg_sent=False)


##################
# skills routing
##################
@app.route(rule='/skillslist-<string:path>')
def skillslist(path):
    global skill_types_json, skills_list_json
    if (path == ""):
        path == "analytics"

    data = {
        "/skillslist-analytics": {
            "pageTitle": "Skills",
            "UpdatedDate": datetime.now().strftime(format='%Y'),
            "skillTypeName": "Data Analytics",
            "skillTypeData": skill_types_json,
            "skillCards": skills_list_json["Data Analytics"]["SkillsList"],
            "Certifications": skills_list_json["Data Analytics"]["Certifications"]},
        "/skillslist-databases": {
            "pageTitle": "Skills",
            "UpdatedDate": datetime.now().strftime(format='%Y'),
            "skillTypeName": "Database Architecture",
            "skillTypeData": skill_types_json,
            "skillCards": skills_list_json["Database Architecture"]["SkillsList"],
            "Certifications": skills_list_json["Database Architecture"]["Certifications"]},
        "/skillslist-websites": {
            "pageTitle": "Skills",
            "UpdatedDate": datetime.now().strftime(format='%Y'),
            "skillTypeName": "Web Development",
            "skillTypeData": skill_types_json,
            "skillCards": skills_list_json["Web Development"]["SkillsList"],
            "Certifications": skills_list_json["Web Development"]["Certifications"]},
        "/skillslist-software": {
            "pageTitle": "Skills",
            "UpdatedDate": datetime.now().strftime(format='%Y'),
            "skillTypeName": "Software Development",
            "skillTypeData": skill_types_json,
            "skillCards": skills_list_json["Software Development"]["SkillsList"],
            "Certifications": skills_list_json["Software Development"]["Certifications"]}
    }

    return render_template(template_name_or_list="skills-list.html", all_posts=data["/skillslist-"+path])

##################
# individual skill page routing
##################
@app.route(rule='/skillpage-<string:path>')
def skillpage(path):
    global skill_pages_json, skill_types_json
    data = {
        "pageTitle": "Skills",
        "UpdatedDate": datetime.now().strftime(format='%Y'),
        "skillTypeName": "N/A",
        "skillTypeData": skill_types_json,
        "skillName": skill_pages_json["/skillpage-"+path]["skillName"],
        "skillPageDetail": skill_pages_json["/skillpage-"+path]["skillPageDetail"],
        "Functionality": skill_pages_json["/skillpage-"+path]["Functionality"],
        "ProjectDocumentation": skill_pages_json["/skillpage-"+path]["Project Documentation"],
        "Video": skill_pages_json["/skillpage-"+path]["Video"],
        "CertificationPrimary": skill_pages_json["/skillpage-"+path]["Primary Certification"],
        "Certifications": skill_pages_json["/skillpage-"+path]["Additional Certifications"]
    }

    return render_template(template_name_or_list="skill-page.html", all_posts=data)


if __name__ == "__main__":
    app.run(debug=True)
