#!/usr/bin/python
# coding=utf-8

from helper.bbcodewriter import generate_table, font_bold
from helper.excelwriter import generate_xlsx
from helper.fetcher import ProduktErgebnisse
from helper.constants import produkt_typen
from helper.options import output

if __name__ == '__main__':

    if output == 'bbcode':
        print('Hier die Sammlung aller Produktbewertungsthreads, inklusive Durchschnittsbewertung und Ranking.')
        print('Das script ist verfügbar unter https://github.com/zaboron/Splittermond/blob/master/parsebewertungen.py')

        for produkt_typ in produkt_typen:
            print('\r\n' + font_bold(produkt_typ))
            print(generate_table(ProduktErgebnisse.get_produkt_ergebnisse(produkt_typ)))

        print('\r\n' + font_bold("Anthologien"))
        print(generate_table(ProduktErgebnisse.get_anthologie_ergebnisse()))

    if output == 'xlsx':
        generate_xlsx(ProduktErgebnisse.get_all())
