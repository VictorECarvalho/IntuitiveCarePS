from bs4 import BeautifulSoup
import requests
import regex
import os
import zipfile
import pathlib
import shutil

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ZIP_NAME = os.path.join(DIR_PATH, "teste_1.zip")
OUTPUT_DIR = os.path.join(DIR_PATH, "temp")

def scrape(regex_pattern):
    page = requests.get("https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos")
    soup = BeautifulSoup(page.text, "html.parser")
    pdf_link_list = soup.find_all("a", attrs={"class": "internal-link"})

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

def zip_files(output_dir):
    folder = pathlib.Path(output_dir)
    if not os.path.isfile(ZIP_NAME):
        with zipfile.ZipFile(ZIP_NAME, "w") as zipf:
            for file in folder.iterdir():
                zipf.write(file, arcname=file.name)
    else:
        print(f"File {ZIP_NAME} already exists.")
                
def delete_temp(folder_name):
    #for deleting the temporary files
    folder = pathlib.Path(folder_name)   
    for file in folder.iterdir():
        os.unlink(os.path.join(folder_name, file.name))
    shutil.rmtree(folder_name)

if __name__ == "__main__":
    print("Starting the scraping process...")
    scrape(r"(Anexo_I|Anexo_II).+(\.pdf)")
    zip_files(OUTPUT_DIR)
    print(f"Files downloaded and zipped into {ZIP_NAME}")
    delete_temp(OUTPUT_DIR)
