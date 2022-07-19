import requests
from bs4 import BeautifulSoup
import re


def getData(url):
    title = ''
    year = 0
    publisher = ''
    number_of_volumes = 0
    description = ''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Get title
    title = soup.find('a', class_='wiki-title').text

    # Get year and remove whitespace
    year = soup.find('table', class_='table').find_all('td')[1].find('div').text
    year = int(''.join(year.split()))

    # Get publisher and remove excess whitespace
    publisher = soup.find('table', class_='table').find_all('td')[2].find('div').text
    publisher = ' '.join(publisher.split())

    # Get number of volumes and remove excess
    number_of_volumes = soup.find('span', class_='volume-issue-count').text
    number_of_volumes = int(re.sub('\D', '', number_of_volumes))

    # Get description
    description = ''

    print(title, year, publisher, number_of_volumes)
    return 
    