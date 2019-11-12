#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, time, re
from datetime import datetime
from bs4 import BeautifulSoup
import requests

currency_multiplier = {'million': 1000000, 'billion': 1000000000}
wiki_page = "https://en.wikipedia.org/wiki/"

pricey_objects = {
    'jet': "40 million"

}

class Public_Figure:
    def __init__(self, figure_name):
        self.name = figure_name
        self.net_worth = Public_Figure.find_net_worth(self.name)

    @classmethod
    def find_net_worth(cls, name):
        # Todo: clean name so that first letter of first and last name capitalized
        name = name.replace(" ", "_")
        wiki_page_with_name = wiki_page + name

        r = requests.get(wiki_page_with_name)
        soup = BeautifulSoup(r.text, "html.parser")
        result_set = soup.find_all('table', attrs={'class': 'infobox biography vcard'})
        pattern = r'\d[0-5].*illion'

        net_worth = ""
        for tr in result_set[0].find_all('tr'):
            if "Net" in str(tr):
                match = re.search(pattern, str(tr))
                try:
                    net_worth = match.group(0)
                    print(tr, net_worth)
                    break
                except AttributeError:
                    net_worth = None

        if net_worth:
            digit, str_multiplier = net_worth.split()
            int_worth = int(float(digit) * currency_multiplier[str_multiplier])
        else:
            print("No net worth found for {}".format(name))
            sys.exit(1)

        return int_worth

    def print_net_worth(self):
        print("name: {}, net worth: {}".format(self.name, self.net_worth))
        return

    def buy_something(self, object):
        price_of_object = pricey_objects[object]

        if isinstance(price_of_object, str):
            digit, multiplier = price_of_object.split()
            price_of_object = int(float(digit) * currency_multiplier[multiplier])

        self.net_worth -= price_of_object
        print("Successfully purchased: {}\n Money remaining: {}".format(object, self.net_worth))
        return self.net_worth


if __name__ == '__main__':
    a_celebity = Public_Figure("Beyonce")
    a_celebity.print_net_worth()
    a_celebity.buy_something("jet")
    a_celebity.print_net_worth()
    sys.exit(0)
