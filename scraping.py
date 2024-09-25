import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os
import warnings
import multiprocessing as mp
import time



def get_trfs_list(file_path):
    """
    Get the list of tRFs from the given file.
    :param file_path: The path to the file containing the tRFs.
    :return: A set of tRFs.
    """
    trfs = set()

    # Check if the file exists first
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            current_line = f.readlines()
            current_line = [x.strip() for x in current_line]  # Strip whitespace from each line

            # Split the lines into words and check for 'tRF' in each word
            for line in current_line:
                words = line.split()
                for word in words:
                    if 'tRF' in word and word[0:3] == 'tRF' and len(word) > 5:
                        word.replace("'", "")
                        word.replace(" ", "")
                        word.replace('"', "")
                        trfs.add(word)
        return trfs

    else:
        warnings.warn('The file does not exist. Please check the file path.')
        return None

def get_miRNA_list(file_path):
    """
    Get the list of miRNAs from the given file.
    :param file_path: The path to the file containing the miRNAs.
    :return: A set of miRNAs.
    """
    mirnas = set()

    # Check if the file exists first
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            current_line = f.readlines()
            current_line = [x.strip() for x in current_line]  # Strip whitespace from each line

            # Split the lines into words and check for 'miR' in each word
            for line in current_line:
                words = line.split()
                for word in words:
                    if 'miR' in word and len(word) > 5 and word[4:7] == 'miR':
                        word.replace("'", "")
                        word.replace(" ", "")
                        word.replace('"', "")
                        mirnas.add(word)
        return mirnas

    else:
        warnings.warn('The file does not exist. Please check the file path.')
        return None
    

def check_genes_for_tRFs(tRFs,output_file, if_save=False):
    """
    Checks the genes for the given tRFs.
    :param tRFs: A set of tRFs to check.
    :return: A list of genes.
    """
    genes_dict = {}

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('http://www.rnanut.net/tRFTar/')
    driver.implicitly_wait(10)

    #push the search button-<button id="nav-search" class="btn orange-hover no-outline-focus text-white flex-fill">SEARCH</button>
    driver.find_element(By.ID, 'nav-search').click() 
    time.sleep(2)

    #put all the trfs in the search box- <textarea id="search-tRF-textarea" class="form-control text-monospace" placeholder="Input tRF MINTBase IDs/sequences here." rows="24"></textarea>
    search_box = driver.find_element(By.ID, 'search-tRF-textarea')

    #put the trfs in the search box and push all the relevant search details
    search_box.send_keys('\n'.join(tRFs))
    driver.find_element(By.ID, 'search-i-tRF-chk').click()
    #driver.find_element(By.ID, 'search-3-tRF-chk').click() #already pushed
    #driver.find_element(By.ID, 'search-5-tRF-chk').click() #already pushed
    driver.find_element(By.ID, 'search-5-half-chk').click()
    driver.find_element(By.ID, 'search-3-half-chk').click()

    #driver.find_element(By.ID, 'search-CDS-chk').click()
    #driver.find_element(By.ID, 'search-3-UTR-chk').click()
    driver.find_element(By.ID, 'search-lncRNA-chk').click()
    driver.find_element(By.ID, 'search-5-UTR-chk').click()


    driver.find_element(By.ID, 'search-btn').click()
    time.sleep(2)

    original_window = driver.current_window_handle
    windows = driver.window_handles
    for window in windows:
        if window != original_window:
            driver.switch_to.window(window)
            break

    driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/div[3]/div[1]/span[2]/span/button/span[1]').click()
    driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/div[3]/div[1]/span[2]/span/div/a[4]').click()

    page = 2
    number_of_pages = driver.find_element(By.CLASS_NAME, 'pagination-info').text.split()[-2]
    number_of_pages = (int(number_of_pages)//100 if int(number_of_pages) % 100 == 0 else int(number_of_pages)//100 + 1)
    for _ in range(number_of_pages):
        for i in range(1,105):
            try:
                search_results = driver.find_element(By.XPATH, '//*[@id="search-table"]/tbody/tr[' + str(i) + ']/td[1]/a')
                if 'tRF' in search_results.text:
                    trf = search_results.text
                    if trf not in genes_dict:
                        genes_dict[trf] = []
                    search_results = driver.find_element(By.XPATH, '//*[@id="search-table"]/tbody/tr[' + str(i) + ']/td[3]/a')
                    gene = search_results.text
                    search_results = driver.find_element(By.XPATH, '//*[@id="search-table"]/tbody/tr[' + str(i) + ']/td[6]')
                    score = search_results.text
                    genes_dict[trf].append((gene, score))

            except:
                break
        page += 1
        time.sleep(2)
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/div[3]/div[2]/ul/li[' + str(page) + ']/a').click()  
    
    if if_save:
        with open(output_file, 'w') as f:
            f.write('tRF gene score' + '\n')
            for trf in genes_dict:
                for gene in genes_dict[trf]:
                    f.write(trf + ' ' + gene[0] + ' ' + gene[1] + '\n')

    return genes_dict

def check_genes_for_miRNAs(miRNAs, output_file, if_save=False):
    """
    Checks the genes for the given miRNAs.
    :param miRNAs: A set of miRNAs to check.
    :return: A list of genes.
    """
    genes_dict = {}

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome()
    driver.get('https://google.com')
    # driver.get('https://ophid.utoronto.ca/mirDIP/index.jsp#r')
    driver.implicitly_wait(10)

    print('driver.current_url)')

    search_box = driver.find_element(By.ID, 'idMicroRna')
    search_box.send_keys(','.join(miRNAs))
    driver.find_element(By.ID, 'submitbutton').click()

    if if_save:
        with open(output_file, 'w') as f:
            f.write('miRNA gene' + '\n')
            for miRna in genes_dict:
                for gene in genes_dict[miRna]:
                    f.write(miRna + ' ' + gene + '\n')

if __name__ == '__main__':
    trf_list = get_trfs_list('conclusion_TRFs.txt')
    check_genes_for_tRFs(trf_list, 'conclusion_TRFs_genes.txt', if_save=True)
    # mirna_list = get_miRNA_list('conclusion_miRNA.txt')
    # for mirna in mirna_list:
    #     print(mirna)
    #print(check_genes_for_miRNAs(mirna_list))
   



        

