import os
import time
import requests
import string
from bs4 import BeautifulSoup
valid_chars = "-_() {}{}".format(string.ascii_letters, string.digits)

# get proceedings 2000 to 2014
for v in range(22, 37):
    directory = 'pdfs/volume_' + str(v)
    if not os.path.exists(directory):
        os.makedirs(directory)
    volume_response = requests.get('https://escholarship.org/uc/cognitivesciencesociety/' + str(v) + '/' + str(v))
    volume_soup = BeautifulSoup(volume_response.text, 'html.parser')
    section_heads = volume_soup.find_all('h3', {'class': 'o-heading1a'})
    for h in section_heads:
        if h.text in ['Papers', 'Posters']:
            paperdiv = h
            while paperdiv.next_sibling is not None:
                paperdiv = paperdiv.next_sibling
                href = paperdiv.h4.a['href']
                title = paperdiv.h4.text
                title = ''.join(c for c in title if c in valid_chars)
                time.sleep(1)
                paper_response = requests.get('https://escholarship.org' + href)
                paper_soup = BeautifulSoup(paper_response.text, 'html.parser')
                pdf_href = paper_soup.find('a', {'class': 'o-download__button'})['href']
                time.sleep(1)
                pdf_response = requests.get('https://escholarship.org' + pdf_href)
                with open(directory + '/' + title + '.pdf', 'wb') as f:
                    f.write(pdf_response.content)


# get proceedings 2015 to 2017
for v in range(37, 40):
    y = v - 37 + 2015
    directory = 'pdfs/volume_' + str(v)
    if not os.path.exists(directory):
        os.makedirs(directory)
    len_until_number = len('https://mindmodeling.org/cogsci201x/papers/')
    volume_response = requests.get('https://mindmodeling.org/cogsci' + str(y) + '/')
    volume_soup = BeautifulSoup(volume_response.text, 'html.parser')
    section_heads = volume_soup.find_all('li', {'id': 'session'})
    for h in section_heads:
        if h.text in ['Papers', 'Talks: Papers', 'Posters: Papers']:
            papers = h.next_sibling.next_sibling
            papers = papers.find_all('a')
            for p in papers:
                href = p['href']
                title = p.text
                num = href[len_until_number:len_until_number+4]
                time.sleep(1)
                pdf_response = requests.get('https://mindmodeling.org/cogsci{}/papers/{}/paper{}.pdf'.format(
                    str(y), num, num))
                with open(directory + '/' + title + '.pdf', 'wb') as f:
                    f.write(pdf_response.content)

# get proceedings before 2000
for v in range(3, 22):
    response = requests.get('https://mindmodeling.org/cogscihistorical/cogsci_' + str(v) + '.pdf')
    with open('pdfs/cogsci_' + str(v) + '.pdf', 'wb') as f:
        f.write(response.content)
