import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
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

        # Print the content of the file for debugging
        print("File Content:")
        for line in current_line:
            print(line)

        # Split the lines into words and check for 'tRF' in each word
        for line in current_line:
            words = line.split()
            for word in words:
                if 'tRF' in word and word[0:3] == 'tRF' and len(word) > 5:
                    word.replace("'", "")
                    word.replace(" ", "")
                    word.replace('"', "")
                    trfs.add(word)
                    print(word+'\n')


def check_genes_for_tRFs(tRFs):
    """
    Checks the genes for the given tRFs.
    :param tRFs: A set of tRFs to check.
    :return: A list of genes.
    """
    genes_dict = {}

    driver = webdriver.Chrome()
    driver.get('http://www.rnanut.net/tRFTar/')

    #push the search button-<button id="nav-search" class="btn orange-hover no-outline-focus text-white flex-fill">SEARCH</button>
    driver.find_element(By.ID, 'nav-search').click()

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

    #time.sleep(5)

    driver.find_element(By.ID, 'search-btn').click()
    time.sleep(10)
    
    

    #print the genes_dict
    for key, value in genes_dict.items():
        print(key, value)









if __name__ == '__main__':
    check_genes_for_tRFs(trfs)

        

