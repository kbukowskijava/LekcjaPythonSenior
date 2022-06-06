from bs4 import BeautifulSoup
import requests
import pandas
import glob
from collections import OrderedDict

pages_csv = 'characters_pages.csv'
characters_csv = 'characters_dataset.csv'


def get_all_links():
    page = requests.get('https://www.marvel.com/characters')
    soup = BeautifulSoup(page.content, 'html.parser')

    pages = []
    mvl_cards = soup.find('div', {'class': 'full-content'}).find_all('div', {'class': 'mvl-card mvl-card--explore'})
    for i in range(len(mvl_cards)-1):
        link = mvl_cards[i]
        page = link.find('a')
        print(i, page['href'], page.text)
        pages.append(page['href'])

    df = pandas.DataFrame({'Link': pages})
    write_csv_file(df, pages_csv)


def create_characters_df():
    base_url = 'https://www.marvel.com'
    pages = pandas.read_csv(pages_csv)
    links = pages['Link']
    marvel_list = []
    columns = []

    for link in links:
        marvel_characters = OrderedDict()
        request = requests.get(base_url + str(link))

        content = request.content
        soup = BeautifulSoup(content, 'html.parser')

        marvel_characters['Name'] = soup.find("h1").text.replace("\n", "").strip()
        marvel_characters['Link'] = link
        print(soup.find('h1').text.replace("\n", "").strip(), base_url + str(link))

        label = soup.findAll('p', {'class': 'bioheader__label'})
        stat = soup.findAll('p', {'class': 'bioheader__stat'})

        for i in range(len(label)):
            column = label[i].text.title()
            if column not in columns:
                columns.append(column)
            try:
                marvel_characters[column] = stat[i].text.replace('\n', '').strip()
            except:
                marvel_characters[column] = ''

        marvel_list.append(marvel_characters)
    df = pandas.DataFrame(marvel_list)
    write_csv_file(df, characters_csv)


def write_csv_file(df, name):
    df.to_csv(name, index=False)
    print('Success \n')


def read_csv_file(name):
    df = pandas.read_csv(name)
    return df


def main():
    files = glob.glob('*.csv')

    if characters_csv not in files:
        if pages_csv not in files:
            print('Create characters_pages.csv')
            get_all_links()
        print('Create characters_dataset.csv')
        create_characters_df()

    df = read_csv_file(characters_csv)
    df = df.fillna('')
    print('Columns: ', df.columns.values)
    print(df[['Link', 'Eyes']])


if __name__ == '__main__':
    main()
