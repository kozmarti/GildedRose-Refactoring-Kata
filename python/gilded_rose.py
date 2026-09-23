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
            self._update_item(item)

    def _update_item(self, item):
        if item.name == SULFURAS:
            return

        if item.name == AGED_BRIE:
            if item.quality < MAX_QUALITY:
                item.quality += 1
            item.sell_in -= 1
            if item.sell_in < 0 and item.quality < MAX_QUALITY:
                item.quality += 1
            return

        if item.name == BACKSTAGE_PASSES:
            if item.quality < MAX_QUALITY:
                item.quality += 1
            if item.sell_in <= BACKSTAGE_DOUBLE_INCREASE_DAYS and item.quality < MAX_QUALITY:
                item.quality += 1
            if item.sell_in <= BACKSTAGE_TRIPLE_INCREASE_DAYS and item.quality < MAX_QUALITY:
                item.quality += 1
            item.sell_in -= 1
            if item.sell_in < 0:
                item.quality = MIN_QUALITY
            return

        if item.quality > MIN_QUALITY:
            item.quality -= 1
        item.sell_in -= 1
        if item.sell_in < 0 and item.quality > MIN_QUALITY:
            item.quality -= 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
