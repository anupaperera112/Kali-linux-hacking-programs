import requests, re, urllib.parse as urlparse
# urlparse for python 2


def extract_links_from(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))  # response.content => for python 2


def crawl(url):
    links = extract_links_from(url)
    for link in links:
        link = urlparse.urljoin(url, link)
        if "#" in link:
            link = link.split("#")[0]
        if url in link and link not in target_links:
            target_links.append(link)
            crawl(link)
            print(link)


target_url = "http://192.168.175.140/mutillidae/"
target_links = []
crawl(target_url)