from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify, url_for, send_from_directory, redirect
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/profile', methods=['POST'])
def getValue():
    link = request.json['userLink']
    data = Linked_Link(link)
    return jsonify(data)

def Linked_Link(userLink):
    with open('config.txt') as f:
        contents = f.readlines()

    userEmail = contents[0]
    userPassword = contents[1]

    #user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

    #options = webdriver.ChromeOptions()
    #options.headless = True
    #options.add_argument(f'user-agent={user_agent}')
    #options.add_argument("--window-size=1920,1080")
    #options.add_argument('--ignore-certificate-errors')
    #options.add_argument('--allow-running-insecure-content')
    #options.add_argument("--disable-extensions")
    #options.add_argument("--proxy-server='direct://'")
    #options.add_argument("--proxy-bypass-list=*")
    #options.add_argument("--start-maximized")
    #options.add_argument('--disable-gpu')
    #options.add_argument('--disable-dev-shm-usage')
    #options.add_argument('--no-sandbox')
    #driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/home")

    driver.find_element(By.XPATH,"//input[@id='session_key']").send_keys(userEmail)
    driver.find_element(By.XPATH,"//input[@id='session_password']").send_keys(userPassword)
    driver.find_element(By.XPATH,"//button[normalize-space()='Sign in']").click()
    time.sleep(10)

    userLink = "https://www.linkedin.com/in/atiqur-rahman-rasel-6814871a4/"
    driver.get(userLink)
    time.sleep(10)
    #print(driver.title)

    UIPage = BeautifulSoup(driver.page_source, 'lxml')

    # User personal information
    personalInfo = UIPage.find('div',"mt2 relative")
    name = personalInfo.find('h1',"text-heading-xlarge inline t-24 v-align-middle break-words").text.strip()
    designation = personalInfo.find('div',"text-body-medium").text.strip()
    university = personalInfo.find('div',"inline-show-more-text").text.strip()
    location = personalInfo.find('span',"text-body-small inline t-black--light break-words").text.strip()

    # Skills Collection
    subLink = "details/skills/"
    driver.get(userLink+subLink)
    time.sleep(10)

    SkillPage = BeautifulSoup(driver.page_source, 'lxml')
    skills = SkillPage.find('main').find_all('span', "mr1 hoverable-link-text t-bold")
    all_skill = []
    for skill in skills:
        all_skill.append(skill.find('span').text)
    
    obj = {
        "Name": name,
        "Designation": designation,
        "University": university,
        "Location": location,
        "Skills" : all_skill
    }

    #myFile = open('infirmation.csv','a+')
    #myFile.write("Name: "+name+"\n")
    #myFile.write("Designation: "+designation+"\n")
    #myFile.write("Location: "+location+"\n")
    #myFile.write("Skills: " + str(all_skill))
    #myFile.write("\n\n")
    #myFile.close()
    
    print("This task has been completed!")
    return obj

    #print(name)
    #print(designation)
    #print(university)
    #print(location)
    #print(all_skill)

ALLOWED_EXTENSION = set(['csv'])
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[0] in ALLOWED_EXTENSION

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            new_filename = f'{filename.split(".")[0]}_{str(datetime.now())}.csv'
            save_location = os.path.join('input', new_filename)
            file.save(save_location) 
            
        
            #output_file = process_csv(save_location)
            #return send_from_directory("static", new_filename)
        data = Linked_Multiple(save_location)
        
        js = {
            "Users": data
        }
        return jsonify(js)
        #return "Uploaded"

    return "File uploaded" #render_template("upload.html")


def Linked_Multiple(Currentfile):
    with open('config.txt') as f:
        contents = f.readlines()

    userEmail = contents[0]
    userPassword = contents[1]

    #user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

    #options = webdriver.ChromeOptions()
    #options.headless = True
    #options.add_argument(f'user-agent={user_agent}')
    #options.add_argument("--window-size=1920,1080")
    #options.add_argument('--ignore-certificate-errors')
    #options.add_argument('--allow-running-insecure-content')
    #options.add_argument("--disable-extensions")
    #options.add_argument("--proxy-server='direct://'")
    #options.add_argument("--proxy-bypass-list=*")
    #options.add_argument("--start-maximized")
    #options.add_argument('--disable-gpu')
    #options.add_argument('--disable-dev-shm-usage')
    #options.add_argument('--no-sandbox')
    #driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/home")

    driver.find_element(By.XPATH,"//input[@id='session_key']").send_keys(userEmail)
    driver.find_element(By.XPATH,"//input[@id='session_password']").send_keys(userPassword)
    driver.find_element(By.XPATH,"//button[normalize-space()='Sign in']").click()
    time.sleep(10)

    with open(Currentfile) as f:
        user = f.readlines()
    all_user = []
    for userLink in user:    
        driver.get(userLink)
        time.sleep(10)
        #print(driver.title)

        UIPage = BeautifulSoup(driver.page_source, 'lxml')

        # User personal information
        personalInfo = UIPage.find('div',"mt2 relative")
        name = personalInfo.find('h1',"text-heading-xlarge inline t-24 v-align-middle break-words").text.strip()
        designation = personalInfo.find('div',"text-body-medium").text.strip()
        university = personalInfo.find('div',"inline-show-more-text").text.strip()
        location = personalInfo.find('span',"text-body-small inline t-black--light break-words").text.strip()

        # Skills Collection
        subLink = "details/skills/"
        driver.get(userLink+subLink)
        time.sleep(10)

        SkillPage = BeautifulSoup(driver.page_source, 'lxml')
        skills = SkillPage.find('main').find_all('span', "mr1 hoverable-link-text t-bold")
        all_skill = []
        for skill in skills:
            all_skill.append(skill.find('span').text)
        
        obj = {
            "Name": name,
            "Designation": designation,
            "University": university,
            "Location": location,
            "Skills" : all_skill
        }

        all_user.append(obj)

        #myFile = open(Currentfile,'a+')
        #myFile.write("Name: "+name+"\n")
        #myFile.write("Designation: "+designation+"\n")
        #myFile.write("Location: "+location+"\n")
        #myFile.write("Skills: " + str(all_skill))
        #myFile.write("\n\n")
        #myFile.close()
        print("Single profile has been visited!")
    print("This task has been completed!")
    return all_user


        
if __name__ == '__main__':
    app.run(debug=True,port=3000)
