import argparse

def writing():
    parser = argparse.ArgumentParser()
    parser.add_argument('my_list', type=str, nargs='+')
    args = parser.parse_args()
    file = open('new_urls.txt', 'a')
    entry = ' '.join(args.my_list)
    file.write(f'\n{entry}')
    file.close()

