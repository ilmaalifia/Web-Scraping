# Bookstore Web Scraping Using Python with Beautiful Soup Library
# By Ilma Alifia Mahardika

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import json

header = {'user-agent' : 'Mozilla/60.0 (X11; Windows x86_64); Ilma Alifia Mahardika/Mahasiswa Teknik Informatika ITB/13516036@std.stei.itb.ac.id'}
url = "http://www.bukukita.com/katalogbukuatribut.php?atrId=1&page=1"
page = 1

# Get data of a book
def bukukitaSmallPic(url):
    result = []
    r = urlopen(Request(url, None, header)).read()
    soup = BeautifulSoup(r, "html5lib")
    #content = soup.find_all("div", class_="product-info col-sm-8 col-md-4 col-lg-6")

    title = soup.find("div", class_="product-info__title")
    penulis = soup.find("a", class_="penulis")
    penerbit = soup.find("a", class_="penerbit")

    info = soup.find("div", class_="divider divider--xs product-info__divider")
    
    tanggal = ((info.find_all_next("div", class_="row"))[4]).find("div", class_="col-xs-7 col-md-9")
    hlm = ((info.find_all_next("div", class_="row"))[5]).find("div", class_="col-xs-7 col-md-9")
    cover = ((info.find_all_next("div", class_="row"))[7]).find("div", class_="col-xs-7 col-md-9")
    kategori = ((info.find_all_next("div", class_="row"))[9]).find("div", class_="col-xs-7 col-md-9")
    bonus = ((info.find_all_next("div", class_="row"))[10]).find("div", class_="col-xs-7 col-md-9")
    bahasa = ((info.find_all_next("div", class_="row"))[11]).find("div", class_="col-xs-7 col-md-9")
    price_old = soup.find("span", class_="price-box__old")
    price_new = soup.find("span", class_="price-box__new")
    
    result.append(title.get_text(strip=True))
    result.append(penulis.get_text(strip=True))
    result.append(penerbit.get_text(strip=True))
    result.append(tanggal.get_text(strip=True))
    result.append(hlm.get_text(strip=True))
    result.append(cover.get_text(strip=True))
    result.append(kategori.get_text(strip=True))
    result.append(bonus.get_text(strip=True))
    result.append((bahasa.get_text(strip=True)).replace('\xa0', ' '))
    result.append(price_old.get_text(strip=True))
    result.append(price_new.get_text(strip=True))

    return result

# Get data of a page
def bukukitaBigPic(url, result, page):
    base_address = "http://www.bukukita.com/"

    r = urlopen(Request(url, None, header)).read()
    soup = BeautifulSoup(r, "html5lib")
    books = soup.find_all("div", class_="product-preview-wrapper")

    for book in books:
        link = book.find("a")['href']
        result.append(base_address+link)
    
    page += 1
    temp = (soup.find("li", class_="active")).find_next_sibling("li")
    if temp != None:
        next = temp.find("a")['href']
        bukukitaBigPic(base_address+next, result, page)
	
# Main
		
result = []
data = {}
bukukitaBigPic(url, result, page)

print("Retrieving urls done ...")

# Save as dictionary
x = []
for link in result:
    temp = bukukitaSmallPic(link)
    isi = {
        "judul" : temp[0],
        "penulis" : temp[1],
        "penerbit" : temp[2],
        "tanggal_terbit" : temp[3],
        "jumlah_halaman" : temp[4],
        "cover" : temp[5],
        "kategori" : temp[6],
        "bonus" : temp[7],
        "bahasa" : temp[8],
        "harga_lama" : temp[9],
        "harga_baru" : temp[10],
        }
    x.append(isi)
data.update({ "buku" : x })

print("Dumping data to JSON ...")

# Export to JSON
name = input('Insert filename: ')
with open(name, 'w') as outfile:
    json.dump(data, outfile)

