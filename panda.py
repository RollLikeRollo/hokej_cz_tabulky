#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd


class Tables(object):

    def __init__(self, tables):
        self.tables = [Table(t) for t in tables]

    def get_tables(self):
        return self.tables


class Table(object):

    def __init__(self, data):

        for i in range(len(data)):
            data[i] = data[i].replace("[", "")
            data[i] = data[i].replace("]", "")
            data[i] = data[i].split(",")
            data[i] = [x.strip() for x in data[i]]

        data_clean = []
        for i in range(len(data)):
            data[i] = [x for x in data[i] if x]
            if len(data[i]) > 0:
                data_clean.append(data[i])

        self.df = pd.DataFrame(data_clean[1:], columns=data_clean[0])

    def print_table(self):
        return self.df.to_string()

    def apply_system(self, system: int):
        system = int(system)
        if system == 0:
            return
        elif system == 1:
            self.df["Body"] = self.df["Skóre"].apply(
                lambda x: int(x.split(":")[0]) - int(x.split(":")[1])
            )
            self.df = self.df.sort_values(by=["Body"], ascending=False)
            self.df["# Nove"] = range(1, len(self.df) + 1)
            self.df["# Original"] = self.df["#"]

    def print_simple(self):
        print(self.df[["# Original", "# Nove", "Tým", "Body", "Skóre"]])
