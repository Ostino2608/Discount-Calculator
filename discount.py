"""
Discount Calculator

Uses the Strategy design pattern to model different, interchangeable
discount rules (percentage off, fixed amount off, premium-user pricing)
and picks whichever applicable discount gives the customer the best
(lowest) price.
"""

from abc import ABC, abstractmethod


class Product:
    """A simple product with a name and a price."""

    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f'{self.name} - ${self.price}'


class DiscountStrategy(ABC):
    """Base class every discount strategy must implement."""

    @abstractmethod
    def is_applicable(self, product: Product, user_tier: str) -> bool:
        """Return True if this discount can be applied to the product/user."""
        pass

    @abstractmethod
    def apply_discount(self, product: Product) -> float:
        """Return the discounted price for the product."""
        pass


class PercentageDiscount(DiscountStrategy):
    """Applies a flat percentage off, up to 70% (a sanity cap)."""

    def __init__(self, percent: int) -> None:
        self.percent = percent

    def is_applicable(self, product: Product, user_tier: str) -> bool:
        return self.percent <= 70

    def apply_discount(self, product: Product) -> float:
        return product.price * (1 - self.percent / 100)


class FixedAmountDiscount(DiscountStrategy):
    """
    Subtracts a fixed dollar amount, but only if doing so wouldn't
    discount the product by more than 90% of its price.
    """

    def __init__(self, amount: int) -> None:
        self.amount = amount

    def is_applicable(self, product: Product, user_tier: str) -> bool:
        return product.price * 0.9 > self.amount

    def apply_discount(self, product: Product) -> float:
        return product.price - self.amount


class PremiumUserDiscount(DiscountStrategy):
    """Gives premium-tier users a flat 20% off, regardless of product."""

    def is_applicable(self, product: Product, user_tier: str) -> bool:
        return user_tier.lower() == 'premium'

    def apply_discount(self, product: Product) -> float:
        return product.price * 0.8


class DiscountEngine:
    """Runs a product through a list of discount strategies and picks the best price."""

    def __init__(self, strategies: list[DiscountStrategy]) -> None:
        self.strategies = strategies

    def calculate_best_price(self, product: Product, user_tier: str) -> float:
        """
        Return the lowest price available for `product`, considering the
        original price plus every applicable discount strategy.
        """
        prices = [product.price]
        for strategy in self.strategies:
            if strategy.is_applicable(product, user_tier):
                discounted = strategy.apply_discount(product)
                prices.append(discounted)
        return min(prices)
