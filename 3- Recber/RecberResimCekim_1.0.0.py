from bs4 import BeautifulSoup as soup
import requests
import urllib.request
from requests.utils import requote_uri
from os import path
import os

######################################## SITEYE GORE AYARLANMASI GEREK baslangic ########################################
#SITEMIZIN KÖK LINKI
base_url = "https://www.recber.com.tr/"
######################################## SITEYE GORE AYARLANMASI GEREK bitis     ########################################

def createDir(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("%s - klasör zaten var" % path)
    else:
        print ("%s - klasör olusturuldu" % path)

def downloadImage(filename, url):
    if not path.exists(filename):
        url = requote_uri(url)
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, filename)
        print(filename,"- resim indirildi")
    else:
        print(filename,"- resim zaten var")

def getImages(dirname,page):
    response = None
    while response == None:
        try:
            response = requests.get(page, timeout=10)
        except Exception as e:
            print(page,e)
            print("Tekrar deneniyor...")
            response = None
    page = soup(response.content, "lxml")
######################################## SITEYE GORE AYARLANMASI GEREK baslangic ########################################
    for div in page.find("div","product_boxes").find_all("div","box"):
        filename = dirname +'/' + div.find("a")['title'].replace('…','-').replace('/',"'") + '.jpg'
        img = '-'.join(div.find("img")['src'].split('-')[:-1])+'.jpg'
        downloadImage(filename,img)

    #BU KISIM RECURSIVE KISIMDIR. SITEDE URUNLER 2-3 SAYFA OLABILIYOR, YENI SAYFA VARSA ORAYA GECIS ICIN KULLANILIR, SON SAYFAYA KADAR
    next_page = page.find("a","next")
    if next_page:
        getImages(dirname,next_page['href'])
######################################## SITEYE GORE AYARLANMASI GEREK bitis     ########################################
       

def getAllImages():
######################################## SITEYE GORE AYARLANMASI GEREK baslangic ########################################
    #SITEMIZDE KATEGORILERIN LISTELENDIGI SAYFA
    url = "https://www.recber.com.tr/urunlerimiz/"
######################################## SITEYE GORE AYARLANMASI GEREK bitis     ########################################
    response = None
    while response == None:
        try:
            response = requests.get(url, timeout=5)
        except Exception as e:
            print(url,e)
            print("Tekrar deneniyor...")
            response = None
    page = soup(response.content, "lxml")
######################################## SITEYE GORE AYARLANMASI GEREK baslangic ########################################
    #KATEGORI LISTESININ YAKALANMASI
    for div in page.find("div","product_boxes").find_all("div","box"):
        #KATEGORININ SAYFALARININ CEKILMESI
        link = div.find("a")["href"]
        category = div.find("a")["title"]
        createDir(category)
        getImages(category, link)
######################################## SITEYE GORE AYARLANMASI GEREK bitis     ########################################

def main():
    getAllImages()

if __name__ == "__main__":
    main()
