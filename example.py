"""
Demo script: run a product through a set of discount strategies and
print the best price for different user tiers.

Usage:
    python example.py
"""

from discount import (
    Product,
    PercentageDiscount,
    FixedAmountDiscount,
    PremiumUserDiscount,
    DiscountEngine,
)

if __name__ == '__main__':
    product = Product('Wireless Mouse', 50.0)
    strategies = [
        PercentageDiscount(10),
        FixedAmountDiscount(5),
        PremiumUserDiscount(),
    ]
    engine = DiscountEngine(strategies)

    for user_tier in ('Premium', 'Standard'):
        best_price = engine.calculate_best_price(product, user_tier)
        print(f'Best price for {product.name} for {user_tier} user: ${best_price:.2f}')
