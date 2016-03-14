import sys
import codecs
import networkx

if __name__ == '__main__':

    with codecs.open(sys.argv[1], 'r', 'utf-8') as f:
        lines = f.readlines()
        lines = map(lambda l: l.strip(), lines)

        records = map(lambda l: l.split(" "), lines)
        records = map(lambda r: (int(r[0]), " ".join(r[1:])), records)

        G = networkx.Graph()

        for r1 in records:
            for r2 in records:
                if r1[0] == r2[0]:
                    G.add_edge(r1[1], r2[1])

        networkx.write_graphml(G, sys.argv[2])
