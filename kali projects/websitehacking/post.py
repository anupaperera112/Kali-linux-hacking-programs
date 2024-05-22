import requests

target_url = "http://192.168.175.140/dvwa/login.php"
data_dic = {"username":"admin", "password":"password", "Login":"submit"}
response = requests.post(target_url, data=data_dic)
print(response.content)
