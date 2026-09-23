# Gilded Rose – Python

For exercise instructions see [top level README](../README.md) and the [requirements](../GildedRoseRequirements.md).

## Context
Gilded Rose refactoring kata in Python: refactor `update_quality` and add support for Conjured items, without modifying the `Item` class or the `items` property.

## Approach
1. **Safety net first:** golden master (30-day output), characterization tests per rule and boundary (100% branch coverage), CI on every push.
2. **Small refactoring steps**, tests green at every commit:
   - extract constants,
   - group the rules by item type (early returns instead of nested ifs),
   - move each group into its own class with a common `update()` method, chosen by a factory.
3. **Conjured in TDD:** tests first, then implementation. The golden master diff shows that only the Conjured Mana Cake lines changed.

## Design
- **One class per item type** (`NormalItem`, `AgedBrie`, `BackstagePass`, `Sulfuras`, `Conjured`): each item's rules live in one place instead of scattered nested ifs.
- **`ItemUpdater` base class (Template Method):** fixes the daily order (quality, then `sell_in`, then the after-sell-by rule); subclasses only define their own rules. The 0–50 limits are enforced in one place.
- **Factory `updater_for(item)`:** the only place that looks at item names; `update_quality` is a simple loop.
- **Composition:** updaters wrap `Item` instead of changing it, so the goblin's code stays untouched.
- **Open for extension:** a new item type = one new class + one line in the factory (that's how Conjured was added).

## Assumptions
- Conjured: −2 per day, −4 after the sell-by date, never negative.
- Any name starting with "Conjured" is a Conjured item (e.g. "Conjured Aged Brie").
- Aged Brie +2 after the sell-by date is not in the spec but kept from the legacy behavior.

## How to run
Requires [uv](https://docs.astral.sh/uv/).

```
uv sync --group test
uv run pytest
```

Coverage:

```
uv run coverage run -m pytest
uv run coverage report
```

Print the inventory for e.g. 10 days:

```
uv run python texttest_fixture.py 10
```

If the golden master test fails, it writes a `.received.txt` file next to the approved one in `tests/approved_files/`. Rename it to `.approved.txt` only if the change is intended.
