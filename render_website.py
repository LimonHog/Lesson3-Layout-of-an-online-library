import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

def on_reload():
    with open("books/meta_data.json", "r", encoding="utf-8") as my_file:
        all_books_json = my_file.read()

    all_books = json.loads(all_books_json)
    two_books_each = list(chunked(all_books, 2))

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    rendered_page = template.render(
        two_books_each = two_books_each
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    # for one in two_books_each:
    #     for i in one:
    #         print(i['title'])


on_reload()

server = Server()
server.watch('template.html', on_reload)

server.serve(root='.')