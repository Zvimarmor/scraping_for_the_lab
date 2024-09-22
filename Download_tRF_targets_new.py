import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import warnings
import multiprocessing as mp
import time


PROCESS_NUMBER = 1  # adjust this if you want to enable multiprocessing

def download_targets_for_all(tissue, prediction_threshold):
    """
    Gets the arguments and runs the inner loop in parallel as the number of the cores.
    :param tissue: The wanted tissue out of the 'tissue_options.csv' file. Can also be 'All' for no tissue filtration.
    :param prediction_threshold: Float describing the wanted threshold for prediction by DIANA.
    :return: file of the predicted targets and file of the Cholinergic targets above the given threshold of
    the tRFs in the list.
    """
    if not os.path.exists('tRF_targets'):
        os.makedirs('tRF_targets')
    
    tissue_path = os.path.join('tRF_targets', tissue)
    if not os.path.exists(tissue_path):
        os.makedirs(tissue_path)
    
    trfs = list(pd.read_csv(r'tRF_AD_Meitar_030924.csv')['tRF'])
    new_trfs = []
    
    for trf in trfs:
        if not os.path.exists(os.path.join(tissue_path, f'{trf}_{prediction_threshold}.csv')):
            new_trfs.append(trf)
    
    download_targets_for_sublist(new_trfs, tissue, prediction_threshold)


def download_targets_for_sublist(trf_sublist, tissue, prediction_threshold):
    """
    Runs the loop for the single tRF on a sublist of tRFs, given for parallel running.
    :param trf_sublist: A list holding a subgroup of tRFs.
    :param tissue: The tissue that was given as an argument.
    :param prediction_threshold: Float describing the wanted threshold for prediction by DIANA.
    :return: file of the predicted targets and file of the Cholinergic targets above the given threshold of
    the tRFs in the list.
    """
    meta = pd.read_csv(r'metadat_tRF_AD_Meitar.csv')
    meta = meta[meta['tRF'].isin(trf_sublist)].reset_index(drop=True)

    diana_url = 'https://dianalab.e-ce.uth.gr/tarbasev9/interactions'
    options = webdriver.ChromeOptions()
    
    # Uncomment below to run in headless mode
    # options.add_argument('headless')
    
    driver = webdriver.Chrome(options=options)
    
    for trf in trf_sublist:
        try:
            start_time = time.time()
            download_targets_for_tRF(diana_url, driver, meta, prediction_threshold, trf, tissue)
            
            # Enforcing a 1-minute wait between requests
            delta_time = time.time() - start_time
            if delta_time < 61:
                time.sleep(61 - delta_time)
            
            print(f"Elapsed Time = {time.time() - start_time}")
        except Exception as e:
            print(f"Error for {trf}: {str(e)}")
            continue


def download_targets_for_tRF(diana_url, driver, meta, prediction_threshold, trf, tissue):
    """
    Download the targets for a single tRF.
    :param diana_url: The DIANA url for each tRFs.
    :param driver: The driver object for downloading the targets from DIANA.
    :param meta: The updated meta for the tRFs.
    :param prediction_threshold: Float describing the wanted threshold for prediction by DIANA.
    :param trf: The current tRF.
    :param tissue: The tissue that was given as an argument.
    :return:
    """
    seq = meta.loc[meta['tRF'] == trf, 'tRF sequence'].values[0]
    driver.get(diana_url)
    
    # Send the tRF sequence to the textarea
    textarea = driver.find_element(By.TAG_NAME, "textarea")
    textarea.send_keys(seq)
    
    # Click submit
    driver.find_element(By.NAME, ".submit").click()
    
    try:
        # Wait for results to load (using table1 as indicator)
        WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.ID, "table1")))
        html_str = driver.find_element(By.ID, "table1").get_attribute("outerHTML")
        
        # Parse the table
        df = pd.read_html(html_str)[0]
        
        # Assign columns and filter results by Target Score
        df.columns = df.iloc[0]  # Use the first row as header
        df = df[1:]  # Skip the header row
        
        # Filter by threshold and save results
        df_filtered = df[df['Target Score'].astype(float) >= float(prediction_threshold)]
        output_path = os.path.join('tRF_targets', tissue, f'{trf}_{prediction_threshold}.csv')
        df_filtered.to_csv(output_path, index=False)
        
        print(f"Finished downloading targets for {trf}")
    
    except Exception as e:
        print(f"Error processing {trf}: {e}")
        time.sleep(900)  # Wait 15 minutes in case of error before retrying the next one


def main():
    tissue = "AD_tRFs"
    prediction_threshold = 80
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    
    download_targets_for_all(tissue, prediction_threshold)


if __name__ == '__main__':
    main()
