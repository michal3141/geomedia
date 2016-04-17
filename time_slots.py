import sys
import codecs
import networkx
from nltk.tokenize import TweetTokenizer
import re
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import relativedelta


timeformat = "%Y-%m-%d %H:%M:%S"


def read_dict(path):
    with codecs.open(path, 'r', 'utf-8') as f:
        lines = f.readlines()
        lines = map(lambda l: l.strip(), lines)
        return lines

def read_feeds(path):
    import re
    tokenizer = TweetTokenizer()
    with codecs.open(path, 'r', 'utf-8') as f:
        lines = f.readlines()[1:]
        lines = map(lambda l: l.strip(), lines)

        sentences = []
        for line in lines:
            quotes = re.findall(r'\"(.+?)\"',line)
            sentence = "%s. %s" % (quotes[-2], quotes[-1])
            sentence = re.sub('[?.!/;:,]', ' ', sentence).lower()
            date = datetime.strptime(quotes[1], timeformat)
            sentences.append((sentence, date))
        return sentences



# Beginning: 2014-01-01 00:43:21
# End: 2015-06-30 23:41:04

def determine_start_end(feeds):
    import re
    _max = datetime.strptime("1900-01-01 16:30:00", timeformat)
    _min = datetime.strptime("2100-01-01 16:30:00", timeformat)
    for path in feeds:
        with codecs.open(path, 'r', 'utf-8') as f:
            lines = f.readlines()[1:]
            lines = map(lambda l: l.strip(), lines)

            sentences = []
            for line in lines:
                quotes = re.findall(r'\"(.+?)\"',line)
                date = datetime.strptime(quotes[1], timeformat)
                _min = min(_min, date)
                _max = max(_max, date)

    print 'Beginning: '+_min.strftime(timeformat)
    print 'End: '+_max.strftime(timeformat)


def find_slot_number(slots, date):
    for i in range(10):
        if date > slots[i]:
            continue
        else:
            return i-1


if __name__ == '__main__':

        DICT = 'keywords3.dict'

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

        determine_start_end(FEEDS)

        sentences = []
        for feed in FEEDS:
            sentences.extend(read_feeds(feed))

        print 'Extracted feeds.'

        keywords = read_dict(DICT)
        keywords = map(lambda s: s.lower(), keywords)

        filtered = []
        for i in range(len(sentences)):
            words = []

            for w in keywords:
                s,d = sentences[i]
                if ' '+w+' ' in s:
                    words.append((w, d))
            filtered.append(words)
            if i % 10000 == 0:
                print '%d sentences filtered' % i

        print 'Filtered keywords.'

        ordered = []
        for i in range(9):
            ordered.append([])
        timeslots = []
        start_date = datetime.strptime("2014-01-01 00:43:21", timeformat)
        for i in range(10):
            timeslots.append(start_date + relativedelta(months=2*i))

        for f in filtered:
            if f:
                w, d = f[0]
                i = find_slot_number(timeslots, d)
                ordered[i].append(f)

        Gs = []
        for i in range(9):
            Gs.append(networkx.Graph())

        print 'Created timeslots'

        for i in range(9):
            o = ordered[i]
            for f in o:
                for w1, d1 in f:
                    for w2, d2 in f:
                        if w1 != w2:
                            if Gs[i].has_edge(w1, w2):
                                weight = Gs[i][w1][w2]['weight']
                                Gs[i][w1][w2]['weight'] = weight+1
                            else:
                                Gs[i].add_edge(w1, w2, {'weight' : 1})

        print 'Built graph.'

        for i in range(9):
            networkx.write_graphml(Gs[i], "cities_ts%d.graphml" % i)
