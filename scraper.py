#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import time
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

TEMPLATE = 'https://spravy.pravda.sk/domace/clanok/'
# as of 04 september 2021, the highest article id on pravda.sk is around 599463, ta3 around 211018
MAX_ARTICLE_ID = 1000
OUTPUT_FILE = 'pravda_sk.txt'
LOG_FILE = 'pravda_sk_log.txt'
ARTICLE_DESCRIPTION_HTML_CLASS = 'article-detail-perex'
ARTICLE_BODY_HTML_CLASS = 'article-detail-body'


def configure(arguments):
    global TEMPLATE, MAX_ARTICLE_ID, OUTPUT_FILE, LOG_FILE, ARTICLE_BODY_HTML_CLASS, ARTICLE_DESCRIPTION_HTML_CLASS

    for i in range(0, len(arguments)):
        arg_name, arg_value = arguments[i].split('=')
        if arg_name == '--template':
            TEMPLATE = arg_value
        elif arg_name == '--max-article-id':
            MAX_ARTICLE_ID = int(arg_value)
        elif arg_name == '--output-file':
            OUTPUT_FILE = arg_value
        elif arg_name == '--log-file':
            LOG_FILE = arg_value
        elif arg_name == '--desc-html-class':
            ARTICLE_DESCRIPTION_HTML_CLASS = arg_value
        elif arg_name == '--body-html-class':
            ARTICLE_BODY_HTML_CLASS = arg_value
        else:
            print('Invalid arguments present!')
            exit()

    print('Scraper configured:')
    print(f'TEMPLATE: {TEMPLATE}')
    print(f'MAX_ARTICLE_ID: {MAX_ARTICLE_ID}')
    print(f'OUTPUT_FILE: {OUTPUT_FILE}')
    print(f'LOG_FILE: {LOG_FILE}')
    print(f'DESC_HTML_CLASS: {ARTICLE_DESCRIPTION_HTML_CLASS}')
    print(f'BODY_HTML_CLASS: {ARTICLE_BODY_HTML_CLASS}')


def truncate_files():
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.truncate()
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.truncate()


def log_error(url):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        i = url.split('/')[-1]
        f.write(f'Error processing article {i}.')


def write_clean_text(clean_text):
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        f.write(clean_text)
        f.write('\n')


def extract_clean_text(r):
    page = requests.get(r.url)
    soup = BeautifulSoup(page.content, 'html.parser')
    article_description = soup.find(
        'div', class_=ARTICLE_DESCRIPTION_HTML_CLASS)
    article_body = soup.find('div', class_=ARTICLE_BODY_HTML_CLASS)
    text = f'{article_body.text}{article_description.text}'
    # remove all characters not present in this list
    clean_text = re.sub(
        r"[^a-zA-ZÀ-ž0-9\.,„“!?:\-]+", ' ', text).lstrip(' ')
    return clean_text


def main():
    configure(sys.argv[1:])
    urls = []

    for i in range(1, MAX_ARTICLE_ID):
        urls.append(f'{TEMPLATE}{i}')

    truncate_files()

    urls_with_progress_bar = tqdm(urls)
    for url in urls_with_progress_bar:
        urls_with_progress_bar.set_description("Processing %s" % url[:50])

        request = requests.head(url, allow_redirects=True)
        if request.status_code == 200:
            clean_text = extract_clean_text(request)
        else:
            log_error(url)
            continue

        write_clean_text(clean_text)

        # don't spam the site, so we're not blocked
        time.sleep(1)


if __name__ == '__main__':
    main()



