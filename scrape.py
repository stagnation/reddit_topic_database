#!/bin/python3

from bs4 import BeautifulSoup as bs
import re
import csv
import requests
import time
import copy
import subprocess
import os
from progress.bar import Bar


def get_page_dictio(content):
    if not content:
        return None
    soup = bs(content, 'html.parser')
    ret = {}

    try:
        _title = soup.title.string
    except:
        _title = None

    ret['title'] = _title
    ret['topic_link'] = get_topic_link(soup)
    ret['description'] = get_description(soup)
    ret['votes'] = get_votes(soup)
    ret['comments'] = comments_dictio(ret)
    # ret['comments'] = get_comments(soup)

    return ret


def ensure_list(input):
    if isinstance(input, list):
        return input
    else:
        return [input]


def write_csv_output(outputfile, page_list, *args, **kwargs):

    # default_delim = ','
    # if 'delimiter' not in kwargs.keys():
    #     kwargs['delimiter'] = default_delim

    page_list = ensure_list(page_list)
    with open(outputfile, 'wt') as csvfile:
        csvwriter = csv.writer(csvfile, *args, delimiter=',',
                               quotechar='"',
                               quoting=csv.QUOTE_MINIMAL, **kwargs)
        for page in page_list:
            dict_csv_output(page, csvwriter)


def dict_csv_output(page_dict, csvwriter):
    title = page_dict['title']
    votes = page_dict['votes']
    comments = page_dict['comments']
    topic_link = page_dict['topic_link']

    # title = bytes(title, 'UTF-8')
    # votes = bytes(votes, 'UTF-8')
    # comments = bytes(comments, 'UTF-8')

    csvwriter.writerow([votes, comments, title, topic_link])


def get_description(soup):
    desc = None

    tags = soup.find_all('meta')
    for tag in tags:
        try:
            attribute = tag['property']
            if attribute == 'og:description':
                desc = tag['content']
        except KeyError:
            pass
    return desc


def get_topic_link(soup):
    redditbase = 'http://www.reddit.com'
    link = None

    tags = soup.find_all('a')
    for tag in tags:
        try:
            attribute = tag['class']
            if attribute == ['title', 'may-blank', '']:
                link = tag['href']
        except KeyError:
            pass

    if str(link).startswith('/r/'):
        link = redditbase + link

    return link


def get_comments(soup):
    comments = None

    tags = soup.find_all('a')
    for tag in tags:
        try:
            attribute = tag['class']
        except:
            pass

    return comments


def get_votes(soup):
    votes = -1

    tags = soup.find_all('div')
    for tag in tags:
        try:
            attribute = tag['class']
            if attribute == ['score', 'unvoted']:
                votes = tag.string
                votes = int(votes)
        except:
            pass

    return votes


def comments_dictio(dictio):
    return comments(dictio['description'])


def number_from_left(instring):
    if not instring:
        return None
    base = instring.lstrip('0123456789')
    nums = instring[:len(instring) - len(base)]
    return int(nums), base


def comments(description):
    if not description:
        return -1

    pat = '(\d+) comments'
    match = re.search(pat, description)
    if match:
        return match.group(1)
    else:
        return -1


def parse_bookmarks(bookmark_html):
    with open(bookmark_html, 'r') as book:
        content = book.read()
    soup = bs(content, 'html.parser')
    retlinks = []
    links = soup.find_all('a')
    for link in links:
        retlinks.append(link['href'])
    return retlinks


# def get_webpage(link):
#     r = requests.get(link)
#     content = r.text
#     return content


def get_webpage(link, outputfile=None):

    if not outputfile:
        outputfile = 'index.html'
    if not isinstance(outputfile, str):
        outputfile = str(outputfile)

    if not os.path.isfile(outputfile):
        wait()
        args = ['wget', link, '-O', outputfile, '-o', outputfile + '.log']
        stdout, stderr = subprocess.Popen(args).communicate()
        if stderr:
            print(stderr)

    try:
        with open(outputfile, 'r') as op:
            content = op.read()
    except:
        print("\nerror reading: ", outputfile)
        print(link)
        return None

    return content


def sort_insert(inlist, inelem, sort=None):
    # TODO : binatu search
    insertflag = False
    li = inlist

    if sort:
        for idx, e in enumerate(li):
            if sort(inelem) >= sort(e):
                li.insert(idx, inelem)
                insertflag = True
                break

    # catches input that had he least sort value
    # acts as default for when no sort is given
    if not insertflag:
        li.append(inelem)

    return li


def test_sort():
    li = [1, 2, 3, 4, 5, 6, 7, 8]
    e = 3
    s = None
    s = lambda x:  x
    ll = sort_insert(li, e, s)
    print(li)
    print(ll)


def wait():
    time.sleep(3)


def build_database(links, max_items=None):
    if not max_items:
        max_items = len(links)

    li = []
    sort = lambda d: d['votes']

    bar = Bar("processing", max=max_items)
    for idx, url in enumerate(links):
        if idx >= max_items:
            break

        outname = str(idx) + '.html'
        content = get_webpage(url, outname)
        dictio = get_page_dictio(content)

        if dictio:
            li = sort_insert(li, dictio, sort)

        bar.next()
    bar.finish()

    return li


def main():
    bookmark_file = 'musik.html'
    outputfile = 'data.csv'
    links = parse_bookmarks(bookmark_file)

    max_items = len(links)
    database = build_database(links, max_items)
    write_csv_output(outputfile, database)

    # link = links[0]
    # print(link)
    # wait()
    # webpage = get_webpage(link)
    # print(webpage)
    # page_list = get_page_dictio(webpage)

    # page = '227.html'
    # with open(page, 'r') as file:
    #     content = file.read()
    # page_list = get_page_dictio(content)
    # outputfile = 'out.csv'
    # write_csv_output(outputfile, page_list)
    # print(page_list)

if __name__ == '__main__':
    # test_sort()
    main()
