#! ./.venv/bin/python3
import argparse

def writing():
    """adds a new url to the file new_urls.txt
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('my_list', type=str, nargs='+')
    args = parser.parse_args()
    file = open('new_urls.txt', 'a', encoding=10)
    entry = ' '.join(args.my_list)
    file.write(f'\n{entry}')
    file.close()
