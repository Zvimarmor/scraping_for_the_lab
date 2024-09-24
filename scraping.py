import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import os
import warnings
import multiprocessing as mp
import time



trfs = set()

# Check if the file exists first
file_path = 'conclusion_TRFs.txt'
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
                    print(word)


def check_genes_for_tRFs(tRFs):
    """
    Checks the genes for the given tRFs.
    :param tRFs: A set of tRFs to check.
    :return: A list of genes.
    """
    genes_dict = {}

    driver = webdriver.Chrome()
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
                    genes_dict[trf].append(search_results.text)
            except:
                break
        page += 1
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/div[3]/div[2]/ul/li[' + str(page) + ']/a').click()  

    print(genes_dict)

if __name__ == '__main__':
    check_genes_for_tRFs(trfs)



        

