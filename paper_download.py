import csv
import os
import argparse
import requests
import json
from urllib.parse import urljoin

from bs4 import BeautifulSoup


def schoolarParser(html):
    result = []
    soup = BeautifulSoup(html, "html.parser")
    for element in soup.findAll("div", class_="gs_r gs_or gs_scl"):
        if not isBook(element):
            title = None
            link = None
            link_pdf = None
            cites = None
            year = None
            authors = None
            for h3 in element.findAll("h3", class_="gs_rt"):
                found = False
                for a in h3.findAll("a"):
                    if not found:
                        title = a.text
                        link = a.get("href")
                        found = True
            for a in element.findAll("a"):
                if "Cited by" in a.text:
                    cites = int(a.text[8:])
                if "[PDF]" in a.text:
                    link_pdf = a.get("href")
            for div in element.findAll("div", class_="gs_a"):
                try:
                    authors, source_and_year, source = div.text.replace('\u00A0', ' ').split(" - ")
                except ValueError:
                    continue

                if not authors.strip().endswith('\u2026'):
                    # There is no ellipsis at the end so we know the full list of authors
                    authors = authors.replace(', ', ';')
                else:
                    authors = None
                try:
                    year = int(source_and_year[-4:])
                except ValueError:
                    continue
                if not (1000 <= year <= 3000):
                    year = None
                else:
                    year = str(year)
            if title is not None:
                result.append({
                    'title': title,
                    'link': link,
                    'cites': cites,
                    'link_pdf': link_pdf,
                    'year': year,
                    'authors': authors})
    return result


def isBook(tag):
    result = False
    for span in tag.findAll("span", class_="gs_ct2"):
        if span.text == "[B]":
            result = True
    return result


def getSchiHubPDF(html):
    result = None
    soup = BeautifulSoup(html, "html.parser")

    iframe = soup.find(id='pdf')
    plugin = soup.find(id='plugin')

    if iframe is not None:
        result = iframe.get("src")

    if plugin is not None and result is None:
        result = plugin.get("src")

    if result is not None and result[0] != "h":
        result = "HTTPS:" + result

    return result


def SciHubUrls(html):
    result = []
    soup = BeautifulSoup(html, "html.parser")

    for ul in soup.findAll("ul"):
        for a in ul.findAll("a"):
            link = a.get("href")
            if link.startswith("HTTPS://sci-hub.") or link.startswith("HTTP://sci-hub."):
                result.append(link)

    return result

class NetInfo:
    SciHub_URL = None
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    SciHub_URLs_repo = "HTTPS://sci-hub.41610.org/"


parser = argparse.ArgumentParser(description='Download papers from Sci-Hub.')
parser.add_argument('--txt', type=str, required=True, help='The txt file containing the DOIs.')
args = parser.parse_args()

def setSciHubUrl():
    r = requests.get(NetInfo.SciHub_URLs_repo, headers=NetInfo.HEADERS)
    links = SciHubUrls(r.text)
    NetInfo.SciHub_URL = "HTTPS://sci-hub.hkvisa.net"  
    print("\nUsing {} as Sci-Hub instance".format(NetInfo.SciHub_URL))

def saveFile(folder, file_name, content):
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(os.path.join(folder, file_name), 'wb') as f:
        f.write(content)

def getDownloadedDois(dwnl_dir):
    progress_file = os.path.join(dwnl_dir, 'progress.json')
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as file:
            return json.load(file)
    return []

def saveDownloadedDoi(dwnl_dir, doi):
    progress_file = os.path.join(dwnl_dir, 'progress.json')
    downloaded_dois = getDownloadedDois(dwnl_dir)
    downloaded_dois.append(doi)
    with open(progress_file, 'w') as file:
        json.dump(downloaded_dois, file)

def downloadPapers(doi_l, dwnl_dir):
    def URLjoin(*args):
        return "/".join(map(lambda x: str(x).rstrip('/'), args))

    setSciHubUrl()

    downloaded_dois = set(getDownloadedDois(dwnl_dir))
    if not os.path.exists(dwnl_dir):
        os.makedirs(dwnl_dir)

    total_dois = len(doi_l)
    processed_dois = 0

    csv_file = os.path.join(dwnl_dir, os.path.splitext(args.txt)[0] + '_doi_status.csv')
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['DOI', 'Modified DOI', 'Status'])

        for doi in doi_l:
            processed_dois += 1
            print(f"Processing {processed_dois} of {total_dois}: {doi}")

            if doi in downloaded_dois:
                print(f"{doi} already downloaded.")
                writer.writerow([doi, doi.replace('/', '_'), 'True'])
                continue

            url = URLjoin(NetInfo.SciHub_URL, doi)
            r = requests.get(url, headers=NetInfo.HEADERS)
            content_type = r.headers.get('content-type')

            if 'application/pdf' in content_type:
                saveFile(dwnl_dir, doi.replace('/', '_') + '.pdf', r.content)
                print(f"Successfully downloaded {doi}")
                writer.writerow([doi, doi.replace('/', '_'), 'True'])
                saveDownloadedDoi(dwnl_dir, doi)
            elif 'application/pdf' not in content_type:
                pdf_url = getSchiHubPDF(r.text)
                if pdf_url is not None:
                    print(f"Extracted PDF URL: {pdf_url}")
                    
                    if not pdf_url.startswith('HTTP'):
                        pdf_url = urljoin(NetInfo.SciHub_URL, pdf_url)

                    try:
                        r = requests.get(pdf_url, headers=NetInfo.HEADERS)
                        if 'application/pdf' in r.headers.get('content-type'):
                            saveFile(dwnl_dir, doi.replace('/', '_') + '.pdf', r.content)
                            print(f"Successfully downloaded {doi}")
                            writer.writerow([doi, doi.replace('/', '_'), 'True'])
                            saveDownloadedDoi(dwnl_dir, doi)
                        else:
                            print(f"Failed to download {doi}")
                            writer.writerow([doi, doi.replace('/', '_'), 'False'])
                    except Exception as e:
                        print(f"Error occurred: {e}")
                        writer.writerow([doi, doi.replace('/', '_'), 'Error'])
                else:
                    print(f"Failed to download {doi}")
                    writer.writerow([doi, doi.replace('/', '_'), 'False'])

        print("All tasks have been completed!")


def get_doi_l(doi_file):
    DOIs = []
    with open(doi_file) as file_in:
        DOIs = [line.strip() for line in file_in]
    return DOIs

def main():
    parser = argparse.ArgumentParser(description='Download papers from Sci-Hub.')
    parser.add_argument('--txt', type=str, required=True, help='The txt file containing the DOIs.')
    args = parser.parse_args()

    folder_name = os.path.splitext(args.txt)[0]
    DOIs = get_doi_l(args.txt)
    downloadPapers(DOIs, folder_name)

if __name__ == "__main__":
    main()