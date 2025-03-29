from bs4 import BeautifulSoup
import requests
import regex
import os
import zipfile
import pathlib
import shutil

ZIP_NAME = "teste_1.zip"
OUTPUT_DIR = "./temp"

page = requests.get("https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos")
soup = BeautifulSoup(page.text, "html.parser")
pdf_link_list = soup.find_all("a", attrs={"class": "internal-link"})

regex_pattern = r"(Anexo_I|Anexo_II).+(\.pdf)"
pdf_link_list = [link for link in pdf_link_list if regex.search(regex_pattern, link["href"])]


if not os.path.isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)
else:
    print(f"Directory {OUTPUT_DIR} already exists.")

for link in pdf_link_list:
    if not os.path.isfile(os.path.join(OUTPUT_DIR, os.path.basename(link["href"]))):
        response = requests.get(link["href"])
        if response.status_code != 200:
            print(f"Failed to download {link['href']}")
            continue
        file_path = os.path.join(OUTPUT_DIR, os.path.basename(link["href"]))        
        with open(file_path, "wb") as file:
            file.write(response.content)
    else:
        print(f"File {os.path.basename(link['href'])} already exists.")


folder = pathlib.Path(OUTPUT_DIR)
if not os.path.isfile(ZIP_NAME):
    with zipfile.ZipFile(ZIP_NAME, "w") as zipf:
        for file in folder.iterdir():
            zipf.write(file, arcname=file.name)
else:
    print(f"File {ZIP_NAME} already exists.")
            
#for deleting the temporary files   
for file in folder.iterdir():
    os.unlink(os.path.join(OUTPUT_DIR, file.name))
shutil.rmtree(OUTPUT_DIR)

