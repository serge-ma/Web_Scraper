import requests
from bs4 import BeautifulSoup
import string
import os


def clean_file_name(text):
    # Remove standard punctuation & long dash, convert space to underscore
    return text.translate(str.maketrans('', '', string.punctuation))\
        .replace('— ', '')\
        .replace(' ', '_')


def clean_body(text):
    # Remove duplicate empty lines
    return '\n\n'.join([line for line in text.split('\n') if line.strip()])


pages = int(input('> '))
article_type = input('> ')

for page in range(pages):
    main_url = 'https://www.nature.com/nature/articles'
    url_params = {'sort': 'PubDate', 'year': '2020', 'page': page+1}
    main_response = requests.get(main_url, params=url_params)

    if not os.access(f'Page_{page+1}', os.F_OK):
        os.mkdir(f'Page_{page+1}')

    if main_response:
        main_soup = BeautifulSoup(main_response.content, 'html.parser')
        articles = main_soup.find_all("article")

        print(f'Saved articles from page {page+1}:')
        for article in articles:
            if article.find('span', {'class': 'c-meta__type'}).text == article_type:
                title = article.a.text
                url = 'https://www.nature.com' + article.a.get('href')
                file_name = f'{clean_file_name(title)}.txt'
                article_response = requests.get(url)
                article_soup = BeautifulSoup(article_response.content, 'html.parser')
                body = clean_body(article_soup.find('div', {'class': 'c-article-body'}).text)

                with open(f'Page_{page+1}/{file_name}', 'wb') as file:
                    file.write(body.encode())
                    print(file_name)
    else:
        print(f'The URL for page {page+1} returned {main_response.status_code}!')
