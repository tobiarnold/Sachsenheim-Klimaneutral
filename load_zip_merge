import urllib.request
import os
import zipfile

#Holen der Zip Files von der Webseite des DWD und Unzippen der Dateien
def load_and_unzip():
    try:
        links = []
        url = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/annual/kl/historical/{}"
        ending = [line.strip() for line in open("jahreswerte.txt")]
        for i in ending:
            url_new = url.format(i)
            links.append(url_new)
            search_str = ".zip"
            links_new = []
            for item in links:
                new_item = item.split(search_str)[0] + search_str
                links_new.append(new_item)
        #print(links_new)
        for n in links_new:
            if not os.path.isfile(os.path.basename(n)):
                urllib.request.urlretrieve(n, os.path.basename(n))
        for m in links_new:
            with zipfile.ZipFile(os.path.basename(m), 'r') as zip_ref:
                zip_ref.extractall()
        print("Alle extrahiert")
    except:
        print("Daten konnten nicht geladen werden")
load_and_unzip()

#Merging der Text Files
def merging():
    keyword = "produkt_klima_jahr"
    files=[]
    for x in os.listdir():
        if keyword in x:
            files.append(x)
    with open("output_file.csv", "w") as outfile:
        for filename in files:
            with open(filename) as infile:
                contents = infile.read()
                outfile.write(contents)
merging()
