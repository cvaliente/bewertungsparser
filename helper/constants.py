from collections import OrderedDict

# URL of a thread (%d will be thread_id)
BASE_URL = "http://forum.splittermond.de/index.php?topic=%d.0"

# Number of parallel threads (should be equal to number of CPU cores)
CONCURRENCY = 4

SPIEL_HILFEN = 'Spielhilfen'
ZUBEHOR = 'Zubehör'
KAUF_ABENTEUER = 'Kaufabenteuer'
FREIE_ABENTEUER = 'Kostenlos verfügbare Abenteuer'
ANTHOLOGIE = "Anthologien"

produkt_typen = [SPIEL_HILFEN, ZUBEHOR, KAUF_ABENTEUER, FREIE_ABENTEUER]

BAYES_LIMIT_ABENTEUER = 30
BAYES_LIMIT_SPIELHILFEN = 50

produkt_bayes_limit = {
    SPIEL_HILFEN: BAYES_LIMIT_SPIELHILFEN,
    ZUBEHOR: BAYES_LIMIT_ABENTEUER,
    KAUF_ABENTEUER: BAYES_LIMIT_ABENTEUER,
    FREIE_ABENTEUER: BAYES_LIMIT_ABENTEUER,
}

# Collection of Thread IDs in several categories
produkt_threads = OrderedDict([
    (SPIEL_HILFEN,
     [1418, 1676, 2653, 3340, 3341, 3510, 4023, 4241, 4389, 4681, 4682, 4868, 5089, 5170, 5414, 5667, 5668, 5785]),
    (ZUBEHOR, [2361, 3158, 3344, 3345, 5115, 5550]),
    (KAUF_ABENTEUER,
     [2003, 2097, 2360, 2651, 2652, 2752, 3006, 3342, 3343, 4098, 4244, 4245, 4252, 4302, 4690, 4744, 4745, 5171, 5172,
      5373, 5538, 5549, 5696, 5786, 5787, 5822]),
    (FREIE_ABENTEUER, [2097, 2098, 2099, 2100, 2101, 2652, 2651, 4253])
])

# maintain anthologies separately
Anthologien = OrderedDict([
    ('Unter Wölfen', [
        3523, 3524, 3525]),
    ('Zwischen den Welten', [
        5009, 5010, 5011]),
    ('An den Küsten der Kristallsee', [
        3817, 3826, 3827, 3828]),
    ('Alter Friede, neuer Streit', [
        5173, 5174, 5175]),
    ('Verwunschene Mauern', [
        5535, 5536, 5537])
])

# Add anthologies to collection to avoid duplicates
for Anthologie in Anthologien:
    for thread_id in Anthologien[Anthologie]:
        if thread_id not in produkt_threads[KAUF_ABENTEUER]:
            produkt_threads[KAUF_ABENTEUER].append(thread_id)

if __name__ == '__main__':
    print(sorted(produkt_threads[FREIE_ABENTEUER]))
