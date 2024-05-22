import requests

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "google.com"
with open("subdomains.txt", "r") as word_list:
    for line in word_list:
        word = line.strip()
        test_url = word +"." + target_url
        response = request(test_url)
        if response:
            print("[+] Discoverd subdomain -->" + test_url)

# discover directory
# target_url = "google.com"
# with open("subdomains.txt", "r") as word_list:
#     for line in word_list:
#         word = line.strip()
#         test_url = target_url +"/"+word
#         response = request(test_url)
#         if response:
#             print("[+] Discoverd URL -->" + test_url)