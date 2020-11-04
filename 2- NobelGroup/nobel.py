from bs4 import BeautifulSoup as soup
import requests
import urllib.request
from os import path
import os

######################################## SITEYE GORE AYARLANMASI GEREK baslangic ########################################
#SITEMIZIN KÖK LINKI
base_url = "http://www.nobelgroup.com.tr/"
######################################## SITEYE GORE AYARLANMASI GEREK bitis     ########################################

def createDir(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s already exist" % path)
    else:
        print ("Successfully created the directory %s " % path)

def downloadImage(filename, url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, filename)

def getImages(filename,page):
    name = 1
    response = None
    while response == None:
        try:
            response = requests.get(page, timeout=10)
        except Exception as e:
            print(page,e)
            print("Tekrar deneniyor...")
            response = None
    page = soup(response.content, "lxml")

    for img in page.select("li a"):
        if '/UploadedImages/Products/' in img['href']:
            imgurl = base_url[:-1] + img['href']
            if not path.exists(filename + str(name) + '.png'):
                downloadImage(filename + str(name) + '.png',imgurl)
                print(filename + str(name),"downloaded")
            else:
                print(filename + str(name),"already exist_________________________________________________")
            name += 1

def getSubCategories(category, url):
    response = None
    while response == None:
        try:
            response = requests.get(url, timeout=5)
        except Exception as e:
            print(url,e)
            print("Tekrar deneniyor...")
            response = None
    page = soup(response.content.decode('utf-8'), "lxml")
    for a in page.select("table[width='110'] a"):
        img = base_url[:-1] + a.find("img")['src']
        for filename in page.select("a[class='linkler_urun2']"):
            if filename['href'] == a['href']:
                filename = str(category)+'/'+filename.text.strip()
                if not path.exists(filename + '.png'):
                    downloadImage(filename + '.png',img)
                    print(filename,"indirildi")
                else:
                    print(filename,"zaten var_________________________________________________")
                getImages(filename,base_url + a['href'])

def getAllImages():
######################################## SITEYE GORE AYARLANMASI GEREK baslangic ########################################
    #SITEMIZDE KATEGORILERIN LISTELENDIGI SAYFA
    url = "http://www.nobelgroup.com.tr/Products.aspx"
    category = 1
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
    for div in page.select("td[width='235'] a"):
        #KATEGORININ SAYFALARININ CEKILMESI
        createDir(str(category))
        getSubCategories(category, base_url + div['href'])
        category += 1
######################################## SITEYE GORE AYARLANMASI GEREK bitis     ########################################

def main():
    getAllImages()

if __name__ == "__main__":
    main()
