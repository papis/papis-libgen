from pylibgen import Library
import click
import logging
import papis.document
import re
import bs4
import papis.downloaders.base
import urllib.request


@click.command('libgen')
@click.pass_context
@click.help_option('--help', '-h')
@click.option('--author', '-a', default=None)
@click.option('--title', '-t', default=None)
@click.option('--isbn', '-i', default=None)
def explorer(ctx, author, title, isbn):
    """
    Look for documents on library genesis

    Examples of its usage are

    papis explore libgen -a 'Albert einstein' export --yaml einstein.yaml

    """
    logger = logging.getLogger('explore:libgen')
    logger.info('Looking up...')
    lg = Library()
    ids = []

    if author:
        ids += lg.search(ascii(author), 'author')
    if isbn:
        ids += lg.search(ascii(isbn), 'isbn')
    if title:
        ids += lg.search(ascii(title), 'title')

    try:
        data = lg.lookup(ids)
    except:
        data = []

    docs = [papis.document.from_data(data=d.__dict__) for d in data]
    ctx.obj['documents'] += docs
    logger.info('{} documents found'.format(len(docs)))


class Downloader(papis.downloaders.Downloader):

    def __init__(self, url):
        papis.downloaders.Downloader.__init__(self, url, name="libgen")
        self.logger = logging.getLogger('downloader:libgen')
        self._doc_url = None

    @classmethod
    def match(cls, url):
        # http://libgen.io/ads.php?md5=CBA569C45B32CA3DF52E736CD8EF6340
        if re.match(r".*libgen.*md5=.*", url):
            return Downloader(url)
        else:
            return False

    def get_md5(self):
        m = re.match(r'.*md5=([A-Z0-9]+).*', self.uri)
        if m:
            md5 = m.group(1)
            self.logger.debug("got md5 %s", md5)
            return md5

    def _get_raw_data(self):
        url = 'https://libgen.rocks/ads.php?md5=%s' % self.get_md5()
        self.logger.debug("got url %s", url)
        raw_data = (self.session.get(url)
                    .content
                    .decode('utf-8'))
        return raw_data

    def get_document_url(self):
        if self._doc_url:
            return self._doc_url
        raw_data = self._get_raw_data()
        soup = bs4.BeautifulSoup(raw_data, "html.parser")
        a_list = soup.find_all("a")
        for a in a_list:
            for s in a.stripped_strings:
                if re.match("GET", s):
                    self._doc_url = "https://libgen.rocks/{}".format(a["href"])
                    self.logger.info("got doc url %s", self._doc_url)
                    return a._doc_url

    def download_bibtex(self) -> None:
        raw_data = self._get_raw_data()
        soup = bs4.BeautifulSoup(raw_data, "html.parser")
        textareas = soup.find_all("textarea")
        if not textareas:
            return
        self.bibtex_data = textareas[0].text
