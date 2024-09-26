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

def get_trfs_set(file_path):
    """
    Get the list of tRFs from the given file.
    :param file_path: The path to the file containing the tRFs.
    :return: A set of tRFs.
    """
    # Check if the file exists first
    if os.path.exists(file_path):
        trfs = pd.read_csv(file_path, header=None)
        trfs = set(trfs.iloc[:,0])
        return trfs

    else:
        warnings.warn('The trf file does not exist. Please check the file path.')
        return None

def get_miRNA_set(file_path):
    """
    Get the list of miRNAs from the given file.
    :param file_path: The path to the file containing the miRNAs.
    :return: A set of miRNAs.
    """

    # Check if the file exists first
    if os.path.exists(file_path):
        miRNAs = pd.read_csv(file_path, header=None)
        miRNAs = set(miRNAs.iloc[:,0])
        return miRNAs

    else:
        warnings.warn('The miRNA file does not exist. Please check the file path.')
        return None
    
def check_genes_for_tRFs(tRFs,output_file='conclusion_TRFs_genes', if_save=False):
    """
    Checks the genes for the given tRFs.
    :param tRFs: A set of tRFs to check.
    :return: A list of genes.
    """
    genes_dict = {}

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
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

    try:
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/div[3]/div[1]/span[2]/span/button/span[1]').click()
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/div[3]/div[1]/span[2]/span/div/a[4]').click()
        time.sleep(2)
        page = 2
        number_of_pages = driver.find_element(By.CLASS_NAME, 'pagination-info').text.split()[-2]
        number_of_pages = (int(number_of_pages)//100 if int(number_of_pages) % 100 == 0 else int(number_of_pages)//100 + 1)
        for _ in range(number_of_pages):
            for i in range(1, 105):
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
            driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/div[3]/div[2]/ul/li[' + str(page) + ']/a').click()
            time.sleep(2)
    
    except:
        page = 1
        number_of_pages = 1
        search_results = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr/td[1]/a')
        if 'tRF' in search_results.text:
            trf = search_results.text
            if trf not in genes_dict:
                genes_dict[trf] = []
            search_results = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr/td[3]/a')
            gene = search_results.text
            search_results = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr/td[6]')
            score = search_results.text
            genes_dict[trf].append((gene, score)) 
    
    ### Save the results to a file if needed ###
    if if_save:
        df = pd.DataFrame(columns=['tRF', 'gene', 'score'])
        for trf in genes_dict:
            for gene in genes_dict[trf]:
                new_row = {'tRF': trf, 'gene': gene[0], 'score': gene[1]}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(output_file, index=False)

    return genes_dict

def check_genes_for_miRNAs(miRNAs, output_file='conclusion_miRNAs_genes', if_save=False, min_score=0.8, min_sources=10):
    """
    Checks the genes for the given miRNAs, using the mirDIP website.
    :param miRNAs: A list of miRNAs to check.
    :return: A list of genes. 
    """
    genes_dict = {}

    ### Set up the web driver and go to the website ###
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://ophid.utoronto.ca/mirDIP/index.jsp#r')
    driver.implicitly_wait(10)

    search_box = driver.find_element(By.ID, 'idMicroRna')
    search_box.send_keys(','.join(miRNAs))
    driver.find_element(By.XPATH,'/html/body/div[2]/div/form/div[3]/table/tbody/tr/td/div[1]/input[3]').click()

    ### Download the file and save it as a csv file ###
    current_dir = os.path.dirname(os.path.realpath(__file__))
    prefs = {"download.default_directory": current_dir} #set the download directory. CHANGE THIS TO YOUR DESIRED DIRECTORY
    chrome_options.add_experimental_option("prefs", prefs)

    before_download = set(os.listdir(current_dir))
    driver.find_element(By.XPATH,'/html/body/div[2]/div/form/div[3]/table/tbody/tr/td/div[2]/input[2]').click()
    driver.find_element(By.XPATH,'/html/body/div[2]/div/form/div[3]/table/tbody/tr/td/div[1]/input[3]').click() #download the txt file
    time.sleep(5)
    after_download = set(os.listdir(current_dir))

    new_files = after_download - before_download
    downloaded_file = new_files.pop()
    target_name = "mirDIP_result.txt"  # Rename the file to a new name
    os.rename(os.path.join(current_dir, downloaded_file), os.path.join(current_dir, target_name))
    lines_to_skip = 1
    for line in open(target_name):
        if line.startswith('Results'):
            break
        lines_to_skip += 1
    df = pd.read_csv(target_name, sep='\t', skiprows= lines_to_skip)
    df.to_csv('mirDIP_result.csv', index=False)

    ### Read the csv file and get the genes for each miRNA after filtering ###
    df = pd.read_csv('mirDIP_result.csv')
    df = df[df['Integrated Score']>=min_score]
    df = df[df['Number of Sources'] >= min_sources]

    for index, row in df.iterrows():
        miRNA = row['MicroRNA']
        gene = row['Gene Symbol']
        score = row['Integrated Score']
        if miRNA not in genes_dict:
            genes_dict[miRNA] = []
        genes_dict[miRNA].append((gene, score))
    os.remove(target_name)
    os.remove('mirDIP_result.csv')

    ### Save the results to a file if needed ###
    if if_save:
        df = pd.DataFrame(columns=['miRNA', 'gene', 'score'])
        for miRNA in genes_dict:
            for gene in genes_dict[miRNA]:
                new_row = {'miRNA': miRNA, 'gene': gene[0], 'score': gene[1]}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(output_file + '.csv', index=False)

    return genes_dict

if __name__ == '__main__':
    trf_list = get_trfs_set('tRF_AD_Meitar_030924.csv')
    check_genes_for_tRFs(trf_list, 'conclusion_TRFs_genes.csv', if_save=True)
    mirna_list = ['hsa-miR-125a-5p', 'hsa-miR-146a', 'hsa-miR-150-5p', 'hsa-miR-191-5p', 'hsa-miR-199a-3p', 'hsa-miR-200a', 'hsa-miR-203a-3p', 'hsa-miR-223-3p', 'hsa-miR-372', 'hsa-miR-375', 'hsa-miR-499a-5p', 'hsa-miR-663b', 'hsa-miR-885-5p']
    check_genes_for_miRNAs(mirna_list, if_save=True)
        

        

