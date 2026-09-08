"""
Basic tests for discount.py.

Run with:
    pytest
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from discount import (  # noqa: E402
    Product,
    PercentageDiscount,
    FixedAmountDiscount,
    PremiumUserDiscount,
    DiscountEngine,
)


# --- Product ---

def test_product_str_format():
    product = Product('Mouse', 50.0)
    assert str(product) == 'Mouse - $50.0'


# --- PercentageDiscount ---

def test_percentage_discount_applies_correctly():
    product = Product('Mouse', 50.0)
    discount = PercentageDiscount(10)
    assert discount.is_applicable(product, 'standard') is True
    assert discount.apply_discount(product) == 45.0


def test_percentage_discount_over_70_is_not_applicable():
    product = Product('Mouse', 50.0)
    discount = PercentageDiscount(75)
    assert discount.is_applicable(product, 'standard') is False


# --- FixedAmountDiscount ---

def test_fixed_amount_discount_applies_correctly():
    product = Product('Mouse', 50.0)
    discount = FixedAmountDiscount(5)
    assert discount.is_applicable(product, 'standard') is True
    assert discount.apply_discount(product) == 45.0


def test_fixed_amount_discount_too_large_is_not_applicable():
    # amount (48) would eat more than 90% of the $50 price, so it's rejected.
    product = Product('Mouse', 50.0)
    discount = FixedAmountDiscount(48)
    assert discount.is_applicable(product, 'standard') is False


# --- PremiumUserDiscount ---

def test_premium_discount_applies_to_premium_users():
    product = Product('Mouse', 50.0)
    discount = PremiumUserDiscount()
    assert discount.is_applicable(product, 'Premium') is True
    assert discount.apply_discount(product) == 40.0


def test_premium_discount_does_not_apply_to_standard_users():
    product = Product('Mouse', 50.0)
    discount = PremiumUserDiscount()
    assert discount.is_applicable(product, 'standard') is False


def test_premium_discount_is_case_insensitive():
    product = Product('Mouse', 50.0)
    discount = PremiumUserDiscount()
    assert discount.is_applicable(product, 'PREMIUM') is True


# --- DiscountEngine ---

def test_engine_picks_the_lowest_price_among_applicable_discounts():
    product = Product('Mouse', 50.0)
    strategies = [
        PercentageDiscount(10),   # -> 45.0
        FixedAmountDiscount(5),   # -> 45.0
        PremiumUserDiscount(),    # -> 40.0 (applicable, premium user)
    ]
    engine = DiscountEngine(strategies)
    assert engine.calculate_best_price(product, 'Premium') == 40.0


def test_engine_falls_back_to_original_price_when_no_discount_applies():
    product = Product('Mouse', 50.0)
    strategies = [PremiumUserDiscount()]
    engine = DiscountEngine(strategies)
    # Standard user: PremiumUserDiscount isn't applicable, so no discount.
    assert engine.calculate_best_price(product, 'standard') == 50.0


def test_engine_with_no_strategies_returns_original_price():
    product = Product('Mouse', 50.0)
    engine = DiscountEngine([])
    assert engine.calculate_best_price(product, 'standard') == 50.0


def test_engine_ignores_non_applicable_strategies():
    product = Product('Mouse', 50.0)
    strategies = [
        PercentageDiscount(80),   # not applicable (over 70%)
        FixedAmountDiscount(48),  # not applicable (too large)
    ]
    engine = DiscountEngine(strategies)
    assert engine.calculate_best_price(product, 'standard') == 50.0
