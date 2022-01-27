#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 09:49:40 2022

@author: michel
"""

from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import bibtexparser
from pyzotero import zotero
import configparser

# Reading Configurations
config = configparser.ConfigParser()
cfg = config.read('configuration.cfg')

## Zotero API configuration
zotero_api_key=config['zotero']['api_key']
zotero_user_id=config['zotero']['user_id']
zotero_library_id=config['zotero']['library_id']
zotero_library_type=config['zotero']['library_type']

zot = zotero.Zotero(zotero_library_id, zotero_library_type, zotero_api_key)

## Studies from where we start the snowballing round
primary_studies=config['studies']['file']

## Default publisher
publisher='ACM' # ACM, IEEE, Elsevier (so far)

# Configuring Browser
options = Options()

options.add_argument("--disable-extensions")
options.add_argument("--disable-blink-features=AutomationControlled")

browser = webdriver.Chrome(executable_path='./driver/chromedriver',options=options)
browser.implicitly_wait(5)
papers = []

def bib_to_zotero(text, l):
    # Here, it would be nice to have the pyzotero creating a collection inside the selected Zotero group (forward or backward) if they are not created yet.
    # Since we can have multiple rounds, it would be nice to have subcollections, for instance: forward/round1, forward/round2...
    # We can do it manually by now...
    bib_database = bibtexparser.loads(text)
    entries = bib_database.entries
    bib = entries[0]
    print(bib)
    template=''
    bibtype=bib['ENTRYTYPE']
    # This part needs to be improved. I just supposed some types. We need to check in the bibtex we get...
    # Check this; https://api.zotero.org/schema
    # We need to check whether this is exported correctly from Zotero.
    if  bibtype=='article':
        template = zot.item_template('journalArticle')
        template['publicationTitle'] = bib['journal']
        template['publisher'] = bib['journal']
    elif bibtype=='incollection':
        template = zot.item_template('book')
        template['series'] = bib['booktitle']
        template['publisher'] = bib['publisher']
    elif bibtype=='inproceedings':
        template = zot.item_template('conferencePaper')
        template['conferenceName'] = bib['booktitle']
    else:
        template = zot.item_template('conferencePaper')
    
    template['creators'][0]['lastName'] = bib['author']
    template['title'] = bib['title']
    template['url'] = l
    template['date'] =  bib['year']
    return template

def crawl_scholar(links):
    # Accessing the Scholar pages
    for l in links:
        browser.get(l)
        time.sleep(5)
        # Please, improve this (I just added xpaths to see how it could work.)
        try:
            xpath='/html/body/div/div[11]/div[2]/div[3]/div[2]/div/div[2]/h3/a'
            element = browser.find_element_by_xpath(xpath)
        except:
            xpath='/html/body/div/div[11]/div[2]/div[3]/div[2]/div/div/h3'
            element = browser.find_element_by_xpath(xpath)
        # Study Title
        value=element.text
        print(value)
        # Study Link
        p_link=element.get_attribute('href')
        papers.append(value)
        # Study Bibtex
        bibtex_xpath='/html/body/div/div[11]/div[2]/div[3]/div[2]/div/div/div[3]/a[2]'
        bibtex_element=browser.find_element_by_xpath(bibtex_xpath)
        bibtex_element.click()
        time.sleep(5)
        bibfile_xpath='/html/body/div/div[4]/div/div[2]/div/div[2]/a[1]'
        bibfile_element=browser.find_element_by_xpath(bibfile_xpath)
        bibfile_element.click()
        bibfile_content_xpath='/html/body/pre'
        bibfile_content_element=browser.find_element_by_xpath(bibfile_content_xpath)
        bibfile_text=bibfile_content_element.text
        template = bib_to_zotero(bibfile_text, p_link)
        zot.create_items([template])
        time.sleep(5)
    for p in papers:
        print(p)
        
def crawl_acm():
    # I had some issues with a recurrent popup, that's why this exception threatment is here.
    try:
        # Cookies warning
        xpath='//*[@id="pb-page-content"]/div/div[3]/div[2]/a'
        element = browser.find_element_by_xpath(xpath)
        element.click()
    except:
        print('Nothing to click...')
        
    time.sleep(5)
 
    ref_elements = browser.find_elements_by_class_name('google-scholar')
    
    number_of_elements=int(len(ref_elements)/2)
    print("Number of references: ",number_of_elements)
    links = []
    
    for i in range(number_of_elements):
        ref=i+1
        if (ref<10):
            ref_txt="0{}".format(ref)
        else:
            ref_txt=ref
        ref_xpath="//*[@id='ref-000{}']/span/span/a".format(ref_txt)
        try:
            ref_element=browser.find_element_by_xpath(ref_xpath)
            link=ref_element.get_attribute('href')
            links.append(link)
        except:
            print('Out of range...')
    crawl_scholar(links)

def forward_snowballing():
    print("Forward snowballing has not been implemented yet...")
    # This is simpler.
    # 1) Go to Scholar
    # 2) Click on citations (if they exist)
    # 3) For all the pages on Scholar, get each bibtex and add to Zotero

def backward_snowballing():
    # FORWARD
    with open(primary_studies) as f:
        lines = f.readlines()
        for study in lines:
            # forward (who cites the paper)
                # if it is cited
            # backward (whi is cited in the paper)
            browser.get(study)
            xpath=''

            ## Checking the publisher / Here, it would be nice to have a search less "solid" - xpath is too rigid.
            # We also need to cover other publishers. At least the ones that will appear in your snowballing.
            try:
                xpath='//*[@id="pb-page-content"]/div/header/div[1]/div[1]/div[1]/div[2]/a/img'
                browser.find_element_by_xpath(xpath)
                publisher='ACM'
            except:
                try:
                    xpath='//*[@id="LayoutWrapper"]/div/div/div/div[3]/div/xpl-root/div/xpl-document-details/div/div[1]/section[2]/div/xpl-document-header/section/div[2]/div/div/div[1]/div/div[1]/div/div[1]/xpl-publisher/span/span/span/span[2]'
                    browser.find_element_by_xpath(xpath)
                    publisher='IEEE'
                except:
                    try:
                        xpath='//*[@id="gh-branding"]/svg'
                        browser.find_element_by_xpath(xpath)
                        publisher='ScienceDirect'
                    except:
                        publisher='none'
                        
            print("############## Only ACM so far #################")
                  
            if publisher == 'ACM':
                # Show All References
                crawl_acm()

forward_snowballing()

backward_snowballing()
browser.close()