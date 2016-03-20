import nltk
import codecs
import collections
from pprint import pprint

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('words')
nltk.download('maxent_ne_chunker')


BASE = '/home/dominik/Studia/integracja/geomedia/Geomedia_extract_AGENDA/Geomedia_extract_AGENDA/'

FILES = [
    BASE + 'en_AUS_austra_int/rss_unique.csv'
]


def extract_entity_names(text):
    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    def entity_names(t):
        names = []

        if hasattr(t, 'label') and t.label:
            if t.label() == 'NE':
                names.append(' '.join([child[0] for child in t]))
            else:
                for child in t:
                    names.extend(entity_names(child))

        return names

    names = []
    for tree in chunked_sentences:
        # Print results per sentence
        # print extract_entity_names(tree)

        names.extend(entity_names(tree))

    return set(names)



def extract_feeds(path):
    records = []
    with codecs.open(path, 'r', 'utf-8') as f:
        lines = f.readlines()[1:]
        for l in lines:
            l = l.strip()
            tokens = l.split('"')
            tokens = filter(lambda s: s.strip(), tokens)
            text = tokens[3].replace('"', "")
            if len(tokens) > 4:
                text += ". " + tokens[4].replace('"', "")
            records.append((int(tokens[0]), text))
    return records


if __name__ == '__main__':

    keywords = []

    for f in FILES:
        for id, text in extract_feeds(f):
            keywords.append((id, extract_entity_names(text)))

    words = []
    for id, tokens in keywords:
        for token in tokens:
            words.append(token)
    words = list(set(words))

    counter=collections.Counter(words)
    words = counter.most_common(100)
    words = map(lambda t: t[0], words)

    with codecs.open('keywords.dict', 'w', 'utf-8') as f:
        for token in words:
            f.write("%s\n" % token)
