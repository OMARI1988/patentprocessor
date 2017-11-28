from urllib import urlopen, urlretrieve, quote
import requests
# from urllib.parse import urljoin
import os
from bs4 import BeautifulSoup
import glob
import sys, getopt

def main(argv):
    #
    try:
        print 'downloading all of',argv[0]
    except:
        print 'enter a year to download, e.g. test.py 2010'
        sys.exit(2)

    url = 'http://patents.reedtech.com/pgrbft.php'
    u = urlopen(url)

    try:
        html = u.read().decode('utf-8')
    finally:
        u.close()

    soup = BeautifulSoup(html, "html5lib")

    yearToDownload = argv[0]
    downloadDir ='/media/ftg/My Book Duo/patents/'+argv[0]+'/'
    os.chdir(downloadDir)

    files = glob.glob(downloadDir+'*.xml')
    for i,file in enumerate(files):
        files[i] = file.split(".")[0].split("/")[-1]

    for a in soup.find_all('a', href=True):
        if a['href'][27:31] == yearToDownload:
            if a['href'].replace('/','_').split(".")[0].split("_")[-1] in files:
                continue
            # print a['href'].replace('/','_').split(".")[0].split("_")[-1]
        # if(a['href'][27:31] == yearToDownload and not os.path.exists(a['href'].replace('/','_'))):
            file_name = a['href']
            with open(file_name.replace('/','_'), "wb") as f:
                print(a['href'])
                url = 'http://patents.reedtech.com/' + a['href']
                r = requests.get(url,stream=True)
                total_size = int(r.headers.get('content-length', 0))
                print('Downloading %s' % url )
                print('total_size Mb %s' % int(total_size/1000000))
                if total_size is None: # no content length header
                    f.write(r.content)
                else:
                    dl = 0
                    total_size = int(total_size)
                    for data in r.iter_content(chunk_size=4096):
                        dl += len(data)
                        f.write(data)
                        done = int(50 * dl / total_size)
                        sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                        sys.stdout.flush()

if __name__ == "__main__":
   main(sys.argv[1:])
