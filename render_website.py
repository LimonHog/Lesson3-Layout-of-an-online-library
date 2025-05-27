import os
import json
import argparse

from livereload import Server
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape


def on_reload():

    parser = argparse.ArgumentParser(
        description = 'Создаёт онлайн билиотеку'
    )
    parser.add_argument('--book_file', default='media/meta_data.json', help='задаёт нужный файл')
    args = parser.parse_args()
    

    with open(args.book_file, 'r', encoding='utf-8') as my_file:
        all_books_json = my_file.read()

    all_books = json.loads(all_books_json)
    books_per_page = list(chunked(all_books, 10))

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')


    for cycle_step, ten_books in enumerate(books_per_page, 1):
        books_per_line = list(chunked(ten_books, 2))
        rendered_page = template.render(
            books_per_line = books_per_line,
            this_page_num = cycle_step,
            pages_quanity = len(books_per_page)+1
        )
        
        with open(f'pages/index{cycle_step}.html', 'w', encoding='utf8') as file:
            file.write(rendered_page)


def main():

    if os.path.isdir('pages') == False:
        os.makedirs('pages')
    on_reload()


    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename='pages/index1.html')


if __name__ == '__main__':
    main()