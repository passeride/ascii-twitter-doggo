from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = "http://www.nrk.no"

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#parse html
page = soup(page_html, "html.parser");
containers = page.findAll("div",  {"class":"kur-room"})

for container in containers:

    print(container.get_text())

