from bs4 import BeautifulSoup as soup
import requests
import urllib.request
from requests.utils import requote_uri
from os import path
import os

######################################## SITEYE GORE AYARLANMASI GEREK baslangic ########################################
#SITEMIZIN KÖK LINKI
base_url_tr = "https://lstr.panasonic.com/tr/"
base_url = "https://lstr.panasonic.com"
######################################## SITEYE GORE AYARLANMASI GEREK bitis     ########################################

def createDir(path):
    newPath = ''
    for tempPath in path.split('\\'):
        newPath +=  tempPath + '\\'
        try:
            os.mkdir(newPath)
        except OSError:
            if path.split('\\').index(tempPath) == len(path.split('\\'))-1:
                print ("%s - folder already exist!" % newPath)
        else:
            print ("%s - folder created!" % newPath)

def downloadImage(filename, url):
    if not path.exists(filename):
        url = requote_uri(url)
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, filename)
        print(filename,"- image downloaded.")
    else:
        print(filename,"- image already exist.")

def getImages(category,url):
    response = None
    while response == None:
        try:
            response = requests.get(url, timeout=10)
        except Exception as e:
            print(url,e)
            print("Trying again...")
            response = None
    page = soup(response.content, "lxml")
######################################## SITEYE GORE AYARLANMASI GEREK baslangic ########################################
    for tab in page.find("div",id="tabslider_product_category_list").find("ul").find_all("a"):
        newCategory = category + '\\' + tab.text
        createDir(newCategory)
        for product in page.find("div", id=tab["href"].replace("#",'')).find_all("article"):
            filename = newCategory + '\\' + product.find("header").text.strip().replace('/','-') + '.png'
            img = base_url + product.find("img")["src"].strip()
            downloadImage(filename,img)
######################################## SITEYE GORE AYARLANMASI GEREK bitis     ########################################
       
def getAllLinks():
######################################## SITEYE GORE AYARLANMASI GEREK baslangic ########################################
    #SITEMIZDE KATEGORILERIN LISTELENDIGI SAYFA
    url = "https://lstr.panasonic.com/tr/urunler/liste/viko/anahtar-priz/linnera-63/"
######################################## SITEYE GORE AYARLANMASI GEREK bitis     ########################################
    response = None
    while response == None:
        try:
            response = requests.get(url, timeout=5)
        except Exception as e:
            print(url,e)
            print("Trying again...")
            response = None
    page = soup(response.content, "lxml")
######################################## SITEYE GORE AYARLANMASI GEREK baslangic ########################################
    #KATEGORI LISTESININ YAKALANMASI
    for div in page.find_all("a","title"):
        #KATEGORININ SAYFALARININ CEKILMESI
        categoryName = div.find("span").text
        div2 = div.find_parent('li').find("ul")
        category = categoryName
        if div['href'] != "javascript:;":
            getImages(category,base_url_tr+div['href'])
        else:
            for sub in div2.find_all("li","product-kat-2"):
                category2Name = sub.find("span").text
                category = categoryName+"\\"+category2Name
                if sub.find("a")["href"] != "javascript:;":
                    getImages(category,base_url_tr+sub.find("a")["href"])
                else:
                    for last in sub.find("ul").find_all("a"):
                        category3Name = last.text
                        category = categoryName+"\\"+category2Name+"\\"+category3Name
                        getImages(category,base_url_tr+last["href"])
######################################## SITEYE GORE AYARLANMASI GEREK bitis     ########################################

def main():
    getAllLinks()
    
if __name__ == "__main__":
    main()
