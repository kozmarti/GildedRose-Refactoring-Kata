from __future__ import annotations

AGED_BRIE = "Aged Brie"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS = "Sulfuras, Hand of Ragnaros"
CONJURED_PREFIX = "Conjured"

MIN_QUALITY = 0
MAX_QUALITY = 50

BACKSTAGE_DOUBLE_INCREASE_DAYS = 10
BACKSTAGE_TRIPLE_INCREASE_DAYS = 5


class ItemUpdater:
    """Updates the sell_in and quality of one item at the end of a day."""

    def __init__(self, item: Item) -> None:
        self.item = item

    def update(self) -> None:
        self.update_quality()
        self.item.sell_in -= 1
        if self.item.sell_in < 0:
            self.update_quality_after_sell_by()

    def update_quality(self) -> None:
        raise NotImplementedError

    def update_quality_after_sell_by(self) -> None:
        raise NotImplementedError

    def increase_quality(self, amount: int) -> None:
        if self.item.quality < MAX_QUALITY:
            self.item.quality = min(self.item.quality + amount, MAX_QUALITY)

    def decrease_quality(self, amount: int) -> None:
        if self.item.quality > MIN_QUALITY:
            self.item.quality = max(self.item.quality - amount, MIN_QUALITY)


class NormalItem(ItemUpdater):
    def update_quality(self) -> None:
        self.decrease_quality(1)

    def update_quality_after_sell_by(self) -> None:
        self.decrease_quality(1)


class AgedBrie(ItemUpdater):
    def update_quality(self) -> None:
        self.increase_quality(1)

    def update_quality_after_sell_by(self) -> None:
        self.increase_quality(1)


class BackstagePass(ItemUpdater):
    def update_quality(self) -> None:
        if self.item.sell_in <= BACKSTAGE_TRIPLE_INCREASE_DAYS:
            self.increase_quality(3)
        elif self.item.sell_in <= BACKSTAGE_DOUBLE_INCREASE_DAYS:
            self.increase_quality(2)
        else:
            self.increase_quality(1)

    def update_quality_after_sell_by(self) -> None:
        self.item.quality = MIN_QUALITY


class Sulfuras(ItemUpdater):
    def update(self) -> None:
        pass


class Conjured(ItemUpdater):
    def update_quality(self) -> None:
        self.decrease_quality(2)

    def update_quality_after_sell_by(self) -> None:
        self.decrease_quality(2)


UPDATERS_BY_NAME: dict[str, type[ItemUpdater]] = {
    AGED_BRIE: AgedBrie,
    BACKSTAGE_PASSES: BackstagePass,
    SULFURAS: Sulfuras,
}


def updater_for(item: Item) -> ItemUpdater:
    if item.name.startswith(CONJURED_PREFIX):
        return Conjured(item)
    updater_class = UPDATERS_BY_NAME.get(item.name, NormalItem)
    return updater_class(item)


class GildedRose:

    def __init__(self, items: list[Item]) -> None:
        self.items = items

    def update_quality(self) -> None:
        for item in self.items:
            updater_for(item).update()


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
