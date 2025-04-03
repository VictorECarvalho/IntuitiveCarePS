import os
import requests
import regex as re
from bs4 import BeautifulSoup
import zipfile
import shutil
import pandas as pd
import os
import sys
import pathlib
sys.path.append(os.path.abspath("/home/victor/dev/ps/IntuitiveCarePS/teste_1"))
from teste_1 import delete_temp


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
LINK = ["https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/", "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"]
TEMP_DIR = os.path.join(DIR_PATH, "temp")

DB_FILE_DIR = "/var/lib/mysql-files/"

def scrape(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

def download_file(link, file_list, complement = ""):
    for file in file_list:
        response = requests.get(link + file)
        if response.status_code == 200:
            file_path = os.path.join(TEMP_DIR, os.path.basename(file))
            if not os.path.isfile(file_path):
                with open(file_path, "wb") as file:
                    print(f"Downloaded {file}")
                    file.write(response.content)
            else:
                print(f"File {file} already exists.")
        else:
            print(f"Failed to download {link}")

def unzip_files(zip_path, output_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)


if __name__ == "__main__":
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    soup = scrape(LINK[0])
    years = r"2023|2024"
    scraped = soup.find_all("a", string = re.compile(r'20\d{2}\/'))
    new_links = [LINK[0] + s["href"] for s in scraped if re.search(years, s["href"])] 

    for link in new_links:
        soup = scrape(link)
        scraped = soup.find_all("a", string = re.compile(r'\dT20\d{2}\.zip'))
        download_file(link, [s["href"] for s in scraped])

    soup = scrape(LINK[1])
    scraped = soup.find_all("a", attrs={"href": re.compile(r"Relatorio_cadop.csv")})
    download_file(LINK[1], [s["href"] for s in scraped])

    folder = pathlib.Path(TEMP_DIR)
    for file in folder.iterdir():    
        if re.search(r".*\.zip", file.name):
            unzip_files(os.path.join(TEMP_DIR, file.name), TEMP_DIR)
    

    folder = pathlib.Path(TEMP_DIR)   
    for file in folder.iterdir():
        if not re.search(r".*\.csv", file.name):
            os.unlink(os.path.join(TEMP_DIR, file.name))
        else:
            shutil.copyfile(os.path.join(TEMP_DIR, file.name), os.path.join(DB_FILE_DIR,file.name))
    