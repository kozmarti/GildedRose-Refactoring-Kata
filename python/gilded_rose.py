# -*- coding: utf-8 -*-

AGED_BRIE = "Aged Brie"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS = "Sulfuras, Hand of Ragnaros"

MIN_QUALITY = 0
MAX_QUALITY = 50

BACKSTAGE_DOUBLE_INCREASE_DAYS = 10
BACKSTAGE_TRIPLE_INCREASE_DAYS = 5


class ItemUpdater:
    """Updates the sell_in and quality of one item at the end of a day."""

    def __init__(self, item):
        self.item = item

    def update(self):
        self.update_quality()
        self.item.sell_in -= 1
        if self.item.sell_in < 0:
            self.update_quality_after_sell_by()

    def update_quality(self):
        raise NotImplementedError

    def update_quality_after_sell_by(self):
        raise NotImplementedError

    def increase_quality(self, amount):
        if self.item.quality < MAX_QUALITY:
            self.item.quality = min(self.item.quality + amount, MAX_QUALITY)

    def decrease_quality(self, amount):
        if self.item.quality > MIN_QUALITY:
            self.item.quality = max(self.item.quality - amount, MIN_QUALITY)


class NormalItem(ItemUpdater):
    def update_quality(self):
        self.decrease_quality(1)

    def update_quality_after_sell_by(self):
        self.decrease_quality(1)


class AgedBrie(ItemUpdater):
    def update_quality(self):
        self.increase_quality(1)

    def update_quality_after_sell_by(self):
        self.increase_quality(1)


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
            AgedBrie(item).update()
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

        NormalItem(item).update()


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
