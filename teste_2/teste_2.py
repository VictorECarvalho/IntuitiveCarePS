import csv
import os
import json
import numpy as np
import zipfile
import shutil
import pathlib
import tabula
import regex as re
import pandas as pd

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ZIP_PATH = os.path.join("../teste_1", "teste_1.zip")
OUTPUT_DIR = os.path.join(DIR_PATH, "temp")
COLUMN_GROUND_TRUTH = ['PROCEDIMENTO', 'RN\r(alteração)', 'VIGÊNCIA', 'OD', 'AMB', 'HCO',
       'HSO', 'REF', 'PAC', 'DUT', 'SUBGRUPO', 'GRUPO', 'CAPÍTULO']
OUTPUT_FILE = "Teste_Victor"
CSV_FILE = "Rol de Procedimentos e Eventos em Saúde"
ABREVIATIONS = {
    'OD': 'Seg. Odontológica',
    'AMB': 'Seg. Ambulatorial',
}


def unzip_file(zip_path, output_dir):
    if os.path.exists(output_dir):
        print(f"File {output_dir} exists.")
    else:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)

def get_table_pdf(pdf_path):
    tables = tabula.read_pdf(pdf_path, pages="all", silent=True, lattice=True)
    return tables

def join_tables(tables, colum_ground_truth):

    joined = pd.DataFrame(columns=pd.Series(colum_ground_truth))
    failed = []
    for table in tables:
        joined = pd.concat([joined, table], ignore_index=True)

    joined.drop_duplicates(inplace=True)
    joined.dropna(how='all', inplace=True)
    joined.reset_index(drop=True, inplace=True)
    return joined

def filter_tables(tables, filter):
    i = 0
    while i < len(tables):
        if tables[i].columns.tolist() != filter:
            tables.pop(i)
            i -= 1
        else:
            i += 1
    return tables

def process_table(table):
    table = table.replace(r';', ' ', regex=True)
    table = table.replace(r'OD', ABREVIATIONS['OD'], regex=True)
    table = table.replace(r'AMB', ABREVIATIONS['AMB'], regex=True)
    table = table.rename(columns={
        'OD': ABREVIATIONS['OD'],
        'AMB': ABREVIATIONS['AMB'],
    })
    return table

def delete_temp(folder_name):
    if os.path.isdir(folder_name):
        folder = pathlib.Path(folder_name)
        for file in folder.iterdir():
            os.unlink(os.path.join(folder_name, file.name))
        shutil.rmtree(folder_name)

def zip_files(file_to_zip, zip_name=OUTPUT_FILE):
    if not os.path.isfile(os.path.join(OUTPUT_FILE + ".zip")):
        with zipfile.ZipFile(os.path.join(OUTPUT_FILE + ".zip"), 'w') as zipf:
            zipf.write(file_to_zip, arcname=CSV_FILE + ".csv")    
    else:
        print(f"File {OUTPUT_FILE}.zip already exists.")    

if __name__ == "__main__":

    unzip_file(ZIP_PATH, OUTPUT_DIR)
    
    reg = r"(Anexo_I_).+(\.pdf)"
    folder = pathlib.Path(OUTPUT_DIR)
    for file in folder.iterdir():    
        if re.search(reg, file.name):
            print(f"Reading file: {file.name}")
            tables = get_table_pdf(file)

    #filtra tabelas incorretas com base em um header harcoded
    filtered_tables = filter_tables(tables, COLUMN_GROUND_TRUTH)

    #junta todas as tabelas com base no header
    joined = join_tables(tables, COLUMN_GROUND_TRUTH)

    #processa as informações
    processed = process_table(joined)

    if not os.path.isfile(os.path.join(OUTPUT_DIR, CSV_FILE + ".csv")):
        processed.to_csv(os.path.join(OUTPUT_DIR, CSV_FILE + ".csv"), index=False)
    else:
        print(f"File {CSV_FILE}.csv already exists.")
    
    zip_files(os.path.join(OUTPUT_DIR, CSV_FILE + ".csv"), OUTPUT_FILE)
        
    delete_temp(OUTPUT_DIR)