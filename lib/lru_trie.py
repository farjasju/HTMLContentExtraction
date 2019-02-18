# =============================================================================
# LRU Trie
# =============================================================================
#
# Temporary class based on Datapol's code. This will be moved in a full-fledged
# library in the future.
#
import csv
try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse

# Notes:
#   1) We will drop the scheme. It's not relevant for us right now.
#   2) Some urls are filtered for relevance (e.g. twitter.com)
#   3) www variations needs to be taken into account
#   4) We need to avoid the TLD


def url_to_lru(url):

    if '://' not in url:
        url = 'http://' + url

    if 'https://' in url:
        url = url.replace('https://', 'http://')

    parsed = urlparse(url)
    loc = ''
    port = ''

    if ':' in parsed.netloc:
        loc, port = parsed.netloc.split(':')
    else:
        loc = parsed.netloc

    stems = [
        # 's:' + parsed.scheme,
        't:' + port
    ]

    stems += ['h:' + x for x in reversed(loc.split('.')[:-1])]
    stems += ['p:' + x for x in parsed.path.split('/')]
    stems += ['q:' + parsed.query, 'f:' + parsed.fragment]

    stems = [stem for stem in stems if len(stem) > 2]

    return stems


def generate_www_variation(lru):
    if 'h:www' in lru:
        return [stem for stem in lru if stem != 'h:www']
    else:
        if len([stem for stem in lru if stem.startswith('h:')]) > 1:
            return None

        if lru[0].startswith('t:'):
            return lru[:2] + ['h:www'] + lru[2:]
        else:
            return lru[:1] + ['h:www'] + lru[1:]


class LRUTrie(object):

    def __init__(self):
        self.root = {}
        self.leaf = 1
        self.values = []

    def set(self, url, value):
        lru = url_to_lru(url)
        node = self.root

        for stem in lru:
            if stem not in node:
                node[stem] = {}

            node = node[stem]

        node[self.leaf] = value

        # Handling variation
        variation = generate_www_variation(lru)

        if variation:

            node = self.root

            for stem in variation:
                if stem not in node:
                    node[stem] = {}

                node = node[stem]

            node[self.leaf] = value

        self.values.append(value)

    def longest(self, url):
        lru = url_to_lru(url) + [None]
        node = self.root

        last_leaf = None

        for stem in lru:

            if self.leaf in node:
                last_leaf = node[self.leaf]

            if stem not in node:
                break

            node = node[stem]

        if last_leaf is None:
            return

        return last_leaf

    @staticmethod
    def from_csv(filename, detailed=False):
        trie = LRUTrie()

        with open(filename, 'r') as f:
            reader = csv.DictReader(f)

            for line in reader:
                trie.set(line['url'], line['name'] if not detailed else line)

        return trie
