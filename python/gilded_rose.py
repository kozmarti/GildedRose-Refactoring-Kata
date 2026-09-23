# -*- coding: utf-8 -*-

AGED_BRIE = "Aged Brie"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS = "Sulfuras, Hand of Ragnaros"

MIN_QUALITY = 0
MAX_QUALITY = 50

BACKSTAGE_DOUBLE_INCREASE_DAYS = 10
BACKSTAGE_TRIPLE_INCREASE_DAYS = 5


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name != AGED_BRIE and item.name != BACKSTAGE_PASSES:
                if item.quality > MIN_QUALITY:
                    if item.name != SULFURAS:
                        item.quality = item.quality - 1
            else:
                if item.quality < MAX_QUALITY:
                    item.quality = item.quality + 1
                    if item.name == BACKSTAGE_PASSES:
                        if item.sell_in <= BACKSTAGE_DOUBLE_INCREASE_DAYS:
                            if item.quality < MAX_QUALITY:
                                item.quality = item.quality + 1
                        if item.sell_in <= BACKSTAGE_TRIPLE_INCREASE_DAYS:
                            if item.quality < MAX_QUALITY:
                                item.quality = item.quality + 1
            if item.name != SULFURAS:
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name != AGED_BRIE:
                    if item.name != BACKSTAGE_PASSES:
                        if item.quality > MIN_QUALITY:
                            if item.name != SULFURAS:
                                item.quality = item.quality - 1
                    else:
                        item.quality = item.quality - item.quality
                else:
                    if item.quality < MAX_QUALITY:
                        item.quality = item.quality + 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
