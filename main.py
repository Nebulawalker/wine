from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

from datetime_helpers import get_company_age

from pandas import read_excel

from collections import defaultdict

import argparse


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    parser = argparse.ArgumentParser(
        description='Скрипт запускает сайт магазина авторского\
            вина "Новое русское вино".\
            Данные о товарах по умолчанию выгружаются из файла wine.xlsx,\
            либо можно указать свой файл.'
    )
    parser.add_argument(
        '-p', '--path',
        help='Путь до файла с продукцией',
        default='wine.xlsx',
        type=str
    )
    path_to_wines_file = parser.parse_args().path

    df_wines = read_excel(path_to_wines_file, keep_default_na=False)

    wines = df_wines.to_dict(orient="records")

    sorted_wines = defaultdict(list)

    for wine in wines:
        sorted_wines[wine['Категория']].append(wine)

    rendered_page = template.render(
        company_age=f'Уже {get_company_age()} с Вами',
        sorted_wines=sorted_wines,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
