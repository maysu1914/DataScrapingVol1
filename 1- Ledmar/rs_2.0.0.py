from bs4 import BeautifulSoup as soup
import requests
import urllib.request
from os import path

######################################## SITEYE GORE AYARLANMASI GEREK baslangic ########################################
#SITEMIZIN KÖK LINKI
base_url = "https://www.ledmar.com"
######################################## SITEYE GORE AYARLANMASI GEREK bitis     ########################################

def downloadImage(filename, url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, filename)

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

######################################## SITEYE GORE AYARLANMASI GEREK baslangic ########################################
    #ÜRÜN LISTESININ YAKALANMASI
    for div in page.find_all("div","col-6 col-md-4 col-lg-51"):
        #ÜRÜN FIYATININ YAKALANMASI, ZORUNLU DEGIL
        price = div.find("div","showcase-price-new").getText().split()[0].replace(',','.')
        #ÜRÜN RESIM BLOGUNUN YAKALANMASI
        img = div.find("img")
        #ÜRÜN ISMININ BELIRLENMESI, DIKKAT, URUN ISMI BASKA ÜRÜNLERLE AYNI OLABILIR, EK BILGILER YERLESTIRILMELIDIR, BURADA FIYAT VE ÜRÜN ID EKLENIYOR
        filename = img["alt"].replace("/","-") + '_' + price + '_' + img["src"].split('=')[-1] + ".jpg"
        #RESIM URL'SININ YAKALANMASI, DIKKAT, RESIM LINKINDE BIRKAC DEGISIKLIK ILE BÜYÜK SÜRÜMÜ YAKALANABILIR
        url = "https:" + img["src"].replace('min','max')
######################################## SITEYE GORE AYARLANMASI GEREK bitis     ########################################
        
        if not path.exists(filename):
            downloadImage(filename,url)
            print(filename,"downloaded!")
        else:
            print(filename,"already exist_________________________________________________")

def getPages(category):
    response = None
    while response == None:
        try:
            response = requests.get(category, timeout=5)
        except Exception as e:
            print(category,e)
            print("Trying again...")
            response = None
    page = soup(response.content, "lxml")
    getImages(category)
######################################## SITEYE GORE AYARLANMASI GEREK baslangic ########################################
    #SAYFALAMA BÖLÜMÜNÜN YAKALANMASI
    if page.find("div","paginate-content"):
        #SAYFA SAYILARININ YAKALANMASI
        for div in page.find("div","paginate-content").find_all("a"):
            #BIRINCI SAYFANIN ES GECILMESI - YUKARIDA ILK SAYFA ZATEN CEKILDI - getImages(category)
            if div["href"] != "javascript:void(0);":
                #DIGER SAYFALARIN OLUSTURULMASI VE RESIMLERIN CEKILMESI
                getImages(base_url + div["href"])
######################################## SITEYE GORE AYARLANMASI GEREK bitis     ########################################

def getAllImages():
######################################## SITEYE GORE AYARLANMASI GEREK baslangic ########################################
    #SITEMIZDE KATEGORILERIN LISTELENDIGI SAYFA
    url = "https://www.ledmar.com/kategoriler.html"
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
    for div in page.find("div","category-list").find_all("a"):
        #KATEGORININ SAYFALARININ CEKILMESI
        getPages(base_url + div["href"])
######################################## SITEYE GORE AYARLANMASI GEREK bitis     ########################################

def main():
    getAllImages()

if __name__ == "__main__":
    main()
