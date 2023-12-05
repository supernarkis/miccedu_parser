import requests
from bs4 import BeautifulSoup
import time
import csv
import json
from dadata import Dadata
row = []
token = "Your_DADATA_TOKEN"
secret = "Your_DADATA_SECRET"
header = ['monId','branch', 'inn', 'kpp',  'Organization', 'total_count', 'ochno_count', 'vech_count', 'dpo', 'spo', 'vedomstvo', 'site','budget']
URL = "https://monitoring.miccedu.ru/?m=vpo&year=2022/"
page = requests.get(URL)
with open('Instinutes.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames = header)
        writer.writeheader()
f.close()
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="tregion")
regions = results.find_all("p", class_="MsoListParagraph")

for region in regions:
    region_URL = "https://monitoring.miccedu.ru/" + region.a["href"]
    region_page = requests.get(region_URL)
    region_page_soup = BeautifulSoup(region_page.content, "html.parser")
    insts = region_page_soup.find_all("td", class_="inst")
    
    for inst in insts:
        table = inst.parent.parent
        if(table["class"]==['an']):
            print(inst.a["href"])
            print(table["class"])
            time.sleep(3)
            inst_page = requests.get("https://monitoring.miccedu.ru/iam/2022/_vpo/" + inst.a["href"])
            inst_page_soup = BeautifulSoup(inst_page.content, "html.parser")

            organization = inst_page_soup.find("div", id="inst_name").text.replace('"','')
            total_count = ''
            ochno_count = ''
            vech_count = ''
            zaochno_count = ''
            dpo = ''
            spo = ''
            vedomstvo = ''
            site = ''
            budget = ''
            dadata_name = ''
            dadata_data = ''
            branch_type = ''
            inn =  ''
            kpp =  ''
            
            if(len(inst_page_soup.findAll("td", style="vertical-align:bottom;")))>0:
                total_count = int(inst_page_soup.findAll("td", style="vertical-align:bottom;")[1].text.replace(" ",""))
                ochno_count = int(inst_page_soup.findAll("td", style="vertical-align:bottom;")[3].text.replace(" ",""))
                vech_count = int(inst_page_soup.findAll("td", style="vertical-align:bottom;")[5].text.replace(" ",""))
                zaochno_count = int(inst_page_soup.findAll("td", style="vertical-align:bottom;")[7].text.replace(" ",""))
                dpo = int(inst_page_soup.findAll("td", style="vertical-align:bottom;")[17].text.replace(" ",""))
                spo = int(inst_page_soup.findAll("td", style="vertical-align:bottom;")[19].text.replace(" ",""))
                vedomstvo = inst_page_soup.findAll("td", class_="tt")[2].parent.findAll("td")[1].text
                site = inst_page_soup.findAll("td", class_="tt")[3].parent.findAll("td")[1].text
                budget = int(inst_page_soup.findAll("td", style="vertical-align:bottom;")[103].text.replace(" ","").split(",")[0] + "000")
                    
            dadata = Dadata(token, secret)
            suggestions = dadata.suggest(name="party", query=organization)
            dadata.close()

            if(len (suggestions) > 0):
                suggestion = suggestions[0]
                dadata_name = suggestion["value"]
                dadata_data = suggestion["data"]
                branch_type = dadata_data["branch_type"]
                inn =  dadata_data["inn"]
                kpp = dadata_data["kpp"]

            row = ({
                    'monId' : inst.a["href"].split('=')[1],
                    'branch' : branch_type,
                    'inn' : inn,
                    'kpp' : kpp,
                    'Organization': organization,
                    'total_count' : total_count,
                    'ochno_count': ochno_count,
                    'vech_count': vech_count,
                    'dpo' : dpo,
                    'spo': spo,
                    'vedomstvo': vedomstvo,
                    'site' : site,
                    'budget': budget
                    })
            with open('Instinutes.csv', 'a') as f:
                writer = csv.DictWriter(f, fieldnames = header)
                writer.writerow(row)

            f.close()
        else:
            print ("href error")
    print( "region " + region.a["href"] + "done")    
print("well done")
