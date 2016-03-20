import sys
import codecs
import networkx
from nltk.tokenize import TweetTokenizer


def read_dict(path):
    with codecs.open(path, 'r', 'utf-8') as f:
        lines = f.readlines()
        lines = map(lambda l: l.strip(), lines)
        return lines

def read_feeds(path):
    import re
    tokenizer = TweetTokenizer()
    with codecs.open(path, 'r', 'utf-8') as f:
        lines = f.readlines()
        lines = map(lambda l: l.strip(), lines)

        sentences = []
        for line in lines:
            quotes = re.findall(r'\"(.+?)\"',line)
            sentence = "%s. %s" % (quotes[-2], quotes[-1])
            sentences.append(sentence)
        return sentences


if __name__ == '__main__':

        DICT = 'keywords.dict'

        NETWORK = 'net.graphml'

        FEEDS_BASE = '/home/dominik/Studia/integracja/geomedia/Geomedia_extract_AGENDA/Geomedia_extract_AGENDA/'
        FEEDS = [
            FEEDS_BASE + 'en_AUS_hersun_int/rss_unique.csv',
            FEEDS_BASE + 'en_CAN_starca_int/rss_unique.csv',
            FEEDS_BASE + 'en_CHN_chinad_int/rss_unique.csv',
            FEEDS_BASE + 'en_CHN_mopost_int/rss_unique.csv',
            FEEDS_BASE + 'en_GBR_dailyt_int/rss_unique.csv',
            FEEDS_BASE + 'en_GBR_guardi_int/rss_unique.csv',
            FEEDS_BASE + 'en_IND_hindti_int/rss_unique.csv',
            FEEDS_BASE + 'en_IND_tindia_int/rss_unique.csv',
            # FEEDS_BASE + 'en_JPN_jatime_int/rss_unique.csv',
            # FEEDS_BASE + 'en_MLT_tmalta_int/rss_unique.csv',
            # FEEDS_BASE + 'en_MYS_starmy_int/rss_unique.csv',
            # FEEDS_BASE + 'en_NGA_thiday_int/rss_unique.csv',
            # FEEDS_BASE + 'en_NZL_nzhera_int/rss_unique.csv',
            # FEEDS_BASE + 'en_PAK_newint_int/rss_unique.csv',
            # FEEDS_BASE + 'en_SGP_twoday_int/rss_unique.csv',
            # FEEDS_BASE + 'en_USA_nytime_int/rss_unique.csv',
            # FEEDS_BASE + 'en_USA_wapost_int/rss_unique.csv',
            # FEEDS_BASE + 'en_ZWE_chroni_int/rss_unique.csv',
        ]

        sentences = []
        for feed in FEEDS:
            sentences.extend(read_feeds(feed))

        print 'Extracted feeds.'

        keywords = read_dict(DICT)
        keywords = map(lambda s: s.lower(), keywords)


        filtered = []
        for i in range(len(sentences)):
            words = keywords[:]
            words = filter(lambda w: w in sentences[i].lower(), words)
            filtered.append(words)
            if i % 10000 == 0:
                print '%d sentences filtered' % i

        print 'Filtered keywords.'

        G = networkx.Graph()

        for f in filtered:
            for w1 in f:
                for w2 in f:
                    if w1 != w2 and not G.has_edge(w1, w2):
                        G.add_edge(w1, w2)

        print 'Built graph.'

        networkx.write_graphml(G, NETWORK)
