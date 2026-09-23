import pytest

from gilded_rose import GildedRose, Item

NORMAL_ITEM = "+5 Dexterity Vest"
AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
CONJURED = "Conjured Mana Cake"


def after_one_day(name, sell_in, quality):
    """Return (sell_in, quality) of a single item after one update."""
    item = Item(name, sell_in, quality)
    GildedRose([item]).update_quality()
    return item.sell_in, item.quality


class TestNormalItem:
    def test_degrades_by_one_before_sell_by(self):
        assert after_one_day(NORMAL_ITEM, 5, 10) == (4, 9)

    def test_degrades_by_one_on_last_day_before_sell_by(self):
        assert after_one_day(NORMAL_ITEM, 1, 10) == (0, 9)

    def test_degrades_twice_as_fast_after_sell_by(self):
        assert after_one_day(NORMAL_ITEM, 0, 10) == (-1, 8)

    def test_keeps_degrading_twice_as_fast_long_after_sell_by(self):
        assert after_one_day(NORMAL_ITEM, -5, 10) == (-6, 8)

    def test_quality_is_never_negative(self):
        assert after_one_day(NORMAL_ITEM, 5, 0) == (4, 0)

    def test_quality_is_never_negative_after_sell_by(self):
        assert after_one_day(NORMAL_ITEM, 0, 1) == (-1, 0)


class TestAgedBrie:
    def test_increases_by_one_before_sell_by(self):
        assert after_one_day(AGED_BRIE, 5, 10) == (4, 11)

    def test_increases_by_one_on_last_day_before_sell_by(self):
        assert after_one_day(AGED_BRIE, 1, 10) == (0, 11)

    def test_increases_by_two_after_sell_by(self):
        assert after_one_day(AGED_BRIE, 0, 10) == (-1, 12)

    def test_keeps_increasing_by_two_long_after_sell_by(self):
        assert after_one_day(AGED_BRIE, -5, 10) == (-6, 12)

    def test_reaches_max_quality(self):
        assert after_one_day(AGED_BRIE, 5, 49) == (4, 50)

    def test_quality_is_never_above_50(self):
        assert after_one_day(AGED_BRIE, 5, 50) == (4, 50)

    def test_quality_is_never_above_50_after_sell_by(self):
        assert after_one_day(AGED_BRIE, 0, 49) == (-1, 50)


class TestSulfuras:
    def test_never_changes(self):
        assert after_one_day(SULFURAS, 5, 80) == (5, 80)

    def test_never_changes_after_sell_by(self):
        assert after_one_day(SULFURAS, -1, 80) == (-1, 80)


class TestBackstagePasses:
    @pytest.mark.parametrize(
        "sell_in, expected",
        [
            (11, (10, 21)),  # more than 10 days: +1
            (10, (9, 22)),   # 10 days or less: +2
            (6, (5, 22)),
            (5, (4, 23)),    # 5 days or less: +3
            (1, (0, 23)),
        ],
    )
    def test_increases_faster_as_concert_approaches(self, sell_in, expected):
        assert after_one_day(BACKSTAGE_PASSES, sell_in, 20) == expected

    def test_quality_drops_to_zero_after_concert(self):
        assert after_one_day(BACKSTAGE_PASSES, 0, 20) == (-1, 0)

    def test_quality_stays_zero_long_after_concert(self):
        assert after_one_day(BACKSTAGE_PASSES, -1, 0) == (-2, 0)

    @pytest.mark.parametrize(
        "sell_in, quality, expected",
        [
            (11, 50, (10, 50)),
            (10, 49, (9, 50)),
            (5, 48, (4, 50)),
        ],
    )
    def test_quality_is_never_above_50(self, sell_in, quality, expected):
        assert after_one_day(BACKSTAGE_PASSES, sell_in, quality) == expected


class TestConjuredItem:
    # Characterization: Conjured is not implemented yet, so it currently
    # behaves like a normal item. Will change with the Conjured feature.
    def test_currently_degrades_like_normal_item(self):
        assert after_one_day(CONJURED, 5, 10) == (4, 9)

    def test_currently_degrades_like_normal_item_after_sell_by(self):
        assert after_one_day(CONJURED, 0, 10) == (-1, 8)


def test_updates_every_item():
    items = [Item(NORMAL_ITEM, 5, 10), Item(AGED_BRIE, 5, 10)]

    GildedRose(items).update_quality()

    assert [(item.sell_in, item.quality) for item in items] == [(4, 9), (4, 11)]
