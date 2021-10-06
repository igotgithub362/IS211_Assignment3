import argparse
import urllib2
import csv
import re


def download(url):
     data_content = urllib2.urlopen(url)
     return data_content


def process(content):

    counts = {'imagehit':0,
              'rowcount':0}

    browsers = {'Internet Explorer':0,
                'Firefox':0,
                'Google Chrome':0,
                'Safari':0}

    for line in csv.reader(content):
        counts['rowcount'] += 1
        if re.search(r"jpe?g|JPE?G|GIF|PNG|gif|png", line[0]):
            counts['imagehit'] += 1
        if re.search("MSIE", line[2]):
            browsers['Internet Explorer'] += 1
        elif re.search("Chrome", line[2]):
            browsers['Google Chrome'] += 1
        elif re.search("firefox", line[2], re.I):
            browsers['Firefox'] += 1
        elif re.search("Safari", line[2]) and not re.search("Chrome", line[2]):
            browsers['Safari'] += 1

    image_cal = (float(counts['imagehit'])/ counts['rowcount']) * 100
    top_browsed = [max(b for b in browsers.items())]
    resultname = top_browsed[0][0]
    resultnum = top_browsed[0][1]

    report = ("There's a total of {} page hits today.\n"
              "Images account for {} % percent of all requests.\n"
              "{} is browser top used with {} hits.").format(counts['rowcount'],
                                                             image_cal,
                                                             resultname,
                                                             resultnum)
    print report


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help="Enter URL Link to CSV File")
    args = parser.parse_args()
    

    if args.url:
        try:
            inf = download(args.url)
            process(inf)
        except urllib2.URLError as url_err:
            print 'URL is INVALID'
            raise url_err
    else:
        print 'Please enter a valid URL.'

if __name__ == '__main__':
    main()
