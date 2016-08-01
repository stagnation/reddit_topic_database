#!/usr/bin/python3

from bs4 import BeautifulSoup as bs
import re
import argparse
import csv
import subprocess
import os
from wait import wait
from lib import quicksort
from progress.bar import Bar


def get_page_dictio(content, url):
    """
    generates a dictionary with important information from the
    contents of a (web)page.
    """
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
    ret['filename'] = name(url)
    ret['url'] = url

    # """ also save bandcamp pages as if they were links """
    # if not topic_link:
    #     if 'bandcamp' in url:
    #         ret['topic_link'] = ret['url']

    return ret


def ensure_list(input_):
    """
    ensures input_ is a list
    if not, wraps it in a list
    """
    if isinstance(input_, list):
        return input_
    else:
        return [input_]


def write_csv_output(outputfile, page_list, *args, **kwargs):
    """
    writes a list of page dictionaries to a csv file
    """

    # default_delim = ','
    # if 'delimiter' not in kwargs.keys():
    #     kwargs['delimiter'] = default_delim

    page_list = ensure_list(page_list)
    with open(outputfile, 'wt') as csvfile:
        csvwriter = csv.writer(csvfile, *args, delimiter=',',
                               quotechar='"',
                               quoting=csv.QUOTE_MINIMAL, **kwargs)
        for page_ in page_list:
            dict_csv_output(page_, csvwriter)


def dict_csv_output(page_dict, csvwriter):
    """
    writes csv line for a single page_dict
    """
    title = page_dict['title']
    votes = page_dict['votes']
    comments = page_dict['comments']
    topic_link = page_dict['topic_link']
    url = page_dict['url']

    # title = bytes(title, 'UTF-8')
    # votes = bytes(votes, 'UTF-8')
    # comments = bytes(comments, 'UTF-8')

    csvwriter.writerow([votes, comments, title, topic_link, url])


def get_description(soup):
    """
    finds the description attribute of a page, soup
    """
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
    """
    finds the topic link for a page, soup
    """
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


def get_votes(soup):
    """
    finds number of upvotes in a page, soup
    """
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
    """
    finds number of comments in a page, soup
    """
    if not description:
        return -1

    pat = '(\d+) comments'
    match = re.search(pat, description)
    if match:
        return match.group(1)
    else:
        return -1


def parse_bookmarks(bookmark_html):
    """
    parse bookmark file for links
    """

    print("reading from ", bookmark_html)
    with open(bookmark_html, 'r') as book:
        content = book.read()
    soup = bs(content, 'html.parser')
    retlinks = []
    links = soup.find_all('a')
    for link in links:
        try:
            retlinks.append(link['href'])
        except:
            print('href error in {}'.format(bookmark_html))
            print('> {}'.format(link))
    return retlinks


# def get_webpage(link):
#     r = requests.get(link)
#     content = r.text
#     return content


def get_webpage(link, requesttimer, outputfile=None):
    """
    downloads webpages
    keeps track with requesttimer to not send requests too quickly
    """

    if not outputfile:
        outputfile = 'index.html'
    if not isinstance(outputfile, str):
        outputfile = str(outputfile)

    if not os.path.isfile(outputfile):
        requesttimer.next()
        args = ['wget', link, '-O', outputfile, '-o', outputfile + '.log']
        _, stderr = subprocess.Popen(args).communicate()
        if stderr:
            print(stderr)

    try:
        with open(outputfile, 'r') as ofile:
            content = ofile.read()
    except:
        print("\nerror reading: ", outputfile)
        print(link)
        return None

    return content


def read_csv_to_database(csvfile, *args, **kwargs):
    """
    reads list of dictionaries from a csvfile
    """

    database = []

    with open(csvfile, "r") as filehandle:
        csvreader = csv.reader(filehandle, *args,
                               delimiter=',', quotechar='"',
                               quoting=csv.QUOTE_MINIMAL, **kwargs)

        for row in csvreader:
            page_dict = {}
            page_dict['votes'] = int(row[0])
            page_dict['comments'] = int(row[1])
            page_dict['title'] = row[2]
            page_dict['topic_link'] = row[3]
            page_dict['url'] = row[4]

            database.append(page_dict)

    return database


def remove_duplicates(database):
    tups = [tuple(sorted(d.items())) for d in database]
    no_dups = [dict(t) for t in set(tups)]

    return no_dups


def name(url):
    return url.replace('/',"").replace('.', "").replace(':',"")
    # return url.translate(str.maketrans("", "", "/.:#;"))


def build_database(links, database, max_items=None):
    if not max_items:
        max_items = len(links)

    sort = lambda di: di['votes']

    bar = Bar("processing", max=max_items)
    requesttimer = wait(2000)
    for idx, url in enumerate(links):
        if idx >= max_items:
            break

        # outname = str(idx) + '.html'
        # outname = 'dl/' + str(idx) + '.html'
        outname = 'dl/' + name(url)
        content = get_webpage(url, requesttimer, outname)
        dictio = get_page_dictio(content, url)

        if dictio:
            database.append(dictio)

        bar.next()
    bar.finish()

    return database


def main():
    parser = argparse.ArgumentParser(description="reddit scraper, \
                                     sort topic in upvote order")

    parser.add_argument('-x', '--extend',
                        help="extends existing database with new input",
                        )
    parser.add_argument('-o', '--output',
                        help="output file",
                        default="data2.csv",
                        )

    args, inputfiles = parser.parse_known_args()
    if not inputfiles:
        parser.print_usage()
        exit(1)

    if args.extend:
        database = read_csv_to_database(args.extend)
    else:
        database = []

    for inputfile in inputfiles:
        links = parse_bookmarks(inputfile)
        database = build_database(links, database)

    database = remove_duplicates(database)

    sort = lambda di: di['votes']
    database = quicksort(database, sort)

    write_csv_output(args.output, database)

if __name__ == '__main__':
    # test_sort()
    main()
