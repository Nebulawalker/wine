from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

from datetime_helpers import company_age

from pandas import read_excel

from collections import defaultdict

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

df_wines = read_excel("wine.xlsx", keep_default_na=False)

wines = df_wines.to_dict(orient="records")

sorted_wines = defaultdict(list)

for wine in wines:
    sorted_wines[wine['Категория']].append(wine)


rendered_page = template.render(
    company_age=f"Уже {company_age()} с вами",
    sorted_wines=sorted_wines,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
