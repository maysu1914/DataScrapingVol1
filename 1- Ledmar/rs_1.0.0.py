from bs4 import BeautifulSoup as soup
import requests
import urllib.request
from os import path

base_url = "https://www.ledmar.com"
    
def downloadImage(json):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(json["url"], json["filename"])

def getAllImages():
    print("Tüm sayfalar cekiliyor...")
    tum_sayfalar = getAllPages()
    tum_resimler = []
    print("Tüm resimler cekiliyor...")
    for sayfa in tum_sayfalar:
        tum_resimler += getImages(sayfa)
    return tum_resimler

def getImages(page):
    response = None
    while response == None:
        try:
            response = requests.get(page, timeout=10)
        except Exception as e:
            print(page,e)
            print("Tekrar deneniyor...")
            response = None
    page = soup(response.content, "lxml")
    images = []

    for div in page.find_all("div","col-6 col-md-4 col-lg-51"):
        json = {"filename":"", "url":""}
        price = div.find("div","showcase-price-new").getText().split()[0].replace(',','.')
        img = div.find("img")
        json["filename"] = img["alt"].replace("/","-") + '_' + img["src"].split('=')[-1] + '_' + price + ".jpg"
        json["url"] = "https:" + img["src"].replace('min','max')
        images.append(json)
    return images

def getPages(category):
    response = None
    while response == None:
        try:
            response = requests.get(category, timeout=5)
        except Exception as e:
            print(category,e)
            print("Tekrar deneniyor...")
            response = None
    page = soup(response.content, "lxml")
    pages = []
    pages.append(category)
    if page.find("div","paginate-content"):
        for div in page.find("div","paginate-content").find_all("a"):
            if div["href"] != "javascript:void(0);":
                pages.append(base_url + div["href"])
    return pages    

def getAllPages():
    url = "https://www.ledmar.com/kategoriler.html"
    all_pages = []
    response = None
    while response == None:
        try:
            response = requests.get(url, timeout=5)
        except Exception as e:
            print(url,e)
            print("Tekrar deneniyor...")
            response = None
    page = soup(response.content, "lxml")
    for div in page.find("div","category-list").find_all("a"):
        all_pages += getPages(base_url + div["href"])
    return all_pages

def main():
    tum_resimler = getAllImages()
    for resim in tum_resimler:
        if not path.exists(resim["filename"]):
            downloadImage(resim)
            print(resim["filename"],"indirildi")
        else:
            print(resim["filename"],"zaten var_________________________________________________")

if __name__ == "__main__":
    main()
##    downloadImage({"url":"https://st1.myideasoft.com/idea/fo/89/myassets/products/001/hls-2020_min.png?revision=1579117565","filename":"30 x 30 Backlight Clip-in Panel Led Armatür"})
