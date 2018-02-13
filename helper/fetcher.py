#!/usr/bin/python
# coding=utf-8

import urllib.request
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
from helper.constants import *
from helper.options import average


class ProduktParser:

    def __init__(self, produktthreads, anthologien):
        """set base properties: URLs, thread ids, format"""

        self.produkt_ergebnisse = []
        self.anthologie_ergebnisse = []
        self.Produktthreads = produktthreads
        self.anthologien = anthologien
        self.bewertungen = set(
            [item for sublist in self.Produktthreads.values() for item in sublist])
        self.pool = ThreadPool(CONCURRENCY)
        self.pool.map(self.get_produkt, self.bewertungen)
        self.get_anthologie()
        self.calculate_average()

    def calculate_average(self):
        if average == 'mean':
            for produkt in self.produkt_ergebnisse:
                produkt.calculate_mean()

        if average == 'bayes':
            for produkt_typ in produkt_typen:
                total_stimmen = 0
                total_stimmen_cum = 0
                for index, produkt in self.get_produkt_ergebnisse(produkt_typ):
                    total_stimmen += produkt.stimmen
                    total_stimmen_cum += produkt.stimmen_cum
                for index, produkt in self.get_produkt_ergebnisse(produkt_typ):
                    produkt.calculate_bayes(total_stimmen, total_stimmen_cum, produkt_bayes_limit[produkt_typ])

    def get_produkt(self, thread_id):
        """collect information for selected thread id"""
        url = BASE_URL % thread_id
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page.read(), "html.parser")
        produkt_name = soup.find('title').string.split('/')[0].strip()
        polls = soup.find('dl', {'class': 'options'})
        options = polls.findAll('dt', {'class': 'middletext'})
        votes = polls.findAll('span', {'class': 'percentage'})
        ergebnis = dict(zip([[int(s) for s in option.string.split() if s.isdigit()][
                                 0] for option in options], [int(vote.string.split(' ')[0]) for vote in votes]))
        einzelvotes = [
            item for sublist in [[k] * v for k, v in ergebnis.items()] for item in sublist]
        stimmen = len(einzelvotes)
        stimmen_cum = sum(einzelvotes)
        self.produkt_ergebnisse.append(
            ProduktErgebnis(produkt_name, thread_id, url, stimmen, stimmen_cum))

    def get_anthologie(self):
        total_anthologie_stimmen = 0
        total_anthologie_stimmen_cum = 0
        for anthologie in self.anthologien:
            anthologie_stimmen = 0
            anthologie_durchschnitt_agg = 0
            for spiel_hilfe in self.produkt_ergebnisse:
                if spiel_hilfe.thread_id in self.anthologien[anthologie]:
                    anthologie_stimmen += spiel_hilfe.stimmen
                    anthologie_durchschnitt_agg += spiel_hilfe.stimmen_cum
                    total_anthologie_stimmen += spiel_hilfe.stimmen
                    total_anthologie_stimmen_cum += spiel_hilfe.stimmen_cum
            self.anthologie_ergebnisse.append(
                ProduktErgebnis(anthologie, 0, 0, anthologie_stimmen, anthologie_durchschnitt_agg))

        for anthologie in self.anthologie_ergebnisse:
            if average == 'mean':
                anthologie.calculate_mean()
            if average == 'bayes':
                anthologie.calculate_bayes(total_anthologie_stimmen, total_anthologie_stimmen_cum,
                                           BAYES_LIMIT_SPIELHILFEN)

    def get_produkt_ergebnisse(self, produkt_typ):

        result = [produkt for produkt in self.produkt_ergebnisse
                                 if produkt.thread_id in self.Produktthreads[produkt_typ]]
        if average == 'bayes':
            total_stimmen = 0
            total_stimmen_cum = 0
            for produkt in result:
                total_stimmen += produkt.stimmen
                total_stimmen_cum += produkt.stimmen_cum
            for produkt in result:
                produkt.calculate_bayes(total_stimmen, total_stimmen_cum, produkt_bayes_limit[produkt_typ])

        return enumerate(sorted(result))

    def get_anthologie_ergebnisse(self):
        return enumerate(sorted(self.anthologie_ergebnisse))

    def get_all(self):
        return enumerate(sorted(self.produkt_ergebnisse))


class ProduktErgebnis:
    def __init__(self, name, thread_id, url, stimmen, stimmen_cum):
        self.name = str(name)
        self.thread_id = thread_id
        self.url = str(url)
        self.stimmen = stimmen
        self.stimmen_cum = stimmen_cum
        self.thread_id_str = str(thread_id)
        self.stimmen_str = str(stimmen)
        self.durchschnitt = "No votes yet"

    def calculate_mean(self):
        if self.stimmen > 0:
            self.durchschnitt = str(round(self.stimmen_cum / self.stimmen, 2))

    def calculate_bayes(self, total_stimmen, total_stimmen_cum, limit):
        if self.stimmen > 0:

            if total_stimmen > limit:
                total_stimmen_cum = total_stimmen_cum / total_stimmen * limit
                total_stimmen = limit

            bayes = (total_stimmen_cum + self.stimmen_cum) / (total_stimmen + self.stimmen)
            self.durchschnitt = str(round(bayes, 2))

    def __lt__(self, other):
        return self.durchschnitt < other.durchschnitt

    def __eq__(self, other):
        return self.durchschnitt == other.durchschnitt

    def __str__(self):
        return ",".join([self.name, self.thread_id_str, self.url, self.stimmen_str, self.durchschnitt])


ProduktErgebnisse = ProduktParser(produktthreads=produkt_threads, anthologien=Anthologien)
