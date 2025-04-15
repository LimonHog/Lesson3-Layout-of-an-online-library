import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

def on_reload():
    with open("books/meta_data.json", "r", encoding="utf-8") as my_file:
        all_books_json = my_file.read()

    all_books = json.loads(all_books_json)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    rendered_page = template.render(
        all_books = all_books
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

server = Server()
server.watch('template.html', on_reload)

server.serve(root='.')