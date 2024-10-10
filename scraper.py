#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
import bs4 as bs


class Scraper(object):
    def __init__(self):
        self.name = "Scraper"
        self.URL = "https://www.hokej.cz/"
        self.FILTER = "/table?table-filter-season"
        self.URL_LIGA_1 = "maxa-liga"
        self.URL_LIGA_2 = "druha-liga"
        self.URL_LIGA_EX = "tipsport-extraliga"
        self.LIGA = None
        self.years = {}
        self._set_league(0)

    def _request(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
        else:
            return None

    def _set_league(self, liga):
        if liga == 0:
            self.LIGA = self.URL_LIGA_EX
        elif liga == 1:
            self.LIGA = self.URL_LIGA_1
        elif liga == 2:
            self.LIGA = self.URL_LIGA_2
        else:
            raise ValueError("Liga musi byt 0, 1 nebo 2")

    def get_league_available_years(self, liga):
        liga = int(liga)
        self._set_league(liga)
        URL = self.URL + self.LIGA + self.FILTER
        html = self._request(URL)

        soup = bs.BeautifulSoup(html, "lxml")
        supa = soup.find("select", attrs={"id": "frm-table-filter-form-season"})
        supo = supa.find_all("option")
        years = []
        for value in supo:
            years.append(int(value["value"]))
        self.years[liga] = years
        return years

    def _get_league_min_year(self, liga):
        return min(self._get_league_available_years(liga))

    def _get_league_max_year(self, liga):
        return max(self._get_league_available_years(liga))

    def get_league_table(self, liga, rok):
        liga = int(liga)
        if int(rok) not in self.years[liga]:
            self.get_league_available_years(liga)
        if int(rok) not in self.years[liga]:
            raise ValueError("Rok neni v seznamu roku")
        self._set_league(liga)
        URL = self.URL + self.LIGA + self.FILTER + "=" + str(rok)
        html = self._request(URL)
        soup = bs.BeautifulSoup(html, "lxml")
        table = soup.find("table", attrs={"class": "table-soupiska"})
        rows = table.find_all("tr")
        list_rows = []
        for row in rows:
            # TH
            row_td = row.find_all("th")
            str_cells = str(row_td)
            clean_text = bs.BeautifulSoup(str_cells, "lxml").get_text()
            list_rows.append(clean_text)
        for row in rows:
            # TD
            row_td = row.find_all("td")
            str_cells = str(row_td)
            clean_text = bs.BeautifulSoup(str_cells, "lxml").get_text()
            list_rows.append(clean_text)
        return list_rows

    def get_league_tables(self, liga, start, end):
        tables = []
        for rok in range(int(start), int(end) + 1):
            tables.append(self.get_league_table(liga, rok))
        return tables
