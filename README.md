# Discount Calculator

A small Python project demonstrating the **Strategy design pattern**:
different discount rules (percentage off, fixed amount off, premium-user
pricing) are modeled as interchangeable strategy objects, and a
`DiscountEngine` finds the best price by trying every applicable one.

## Why the Strategy pattern?

Instead of a big pile of `if/elif` statements to decide which discount to
apply, each discount rule is its own class implementing a shared
interface (`is_applicable` + `apply_discount`). This makes it easy to add
new discount types later without touching existing code — you just write
a new class and pass it into the list of strategies.

## Features

- `Product` — a simple item with a name and price
- `DiscountStrategy` — abstract base class all discounts implement
- `PercentageDiscount` — a flat % off (capped at 70% as a sanity check)
- `FixedAmountDiscount` — a flat $ amount off (only applies if it wouldn't
  discount the product by more than 90%)
- `PremiumUserDiscount` — 20% off exclusively for premium-tier users
- `DiscountEngine` — runs a product through all strategies and returns
  the lowest resulting price

## Project structure

```
discount-calculator/
├── discount.py               # Product, strategies, and DiscountEngine
├── example.py                  # Demo script
├── tests/
│   └── test_discount.py        # Test suite (pytest)
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Installation

```bash
git clone https://github.com/<your-username>/discount-calculator.git
cd discount-calculator
pip install -r requirements.txt   # only needed to run the tests
```

No external libraries are required to run the project itself — it only
uses Python's standard library.

## Usage

```python
from discount import (
    Product,
    PercentageDiscount,
    FixedAmountDiscount,
    PremiumUserDiscount,
    DiscountEngine,
)

product = Product('Wireless Mouse', 50.0)
strategies = [
    PercentageDiscount(10),
    FixedAmountDiscount(5),
    PremiumUserDiscount(),
]
engine = DiscountEngine(strategies)

print(engine.calculate_best_price(product, 'Premium'))   # 40.0
print(engine.calculate_best_price(product, 'Standard'))  # 45.0
```

Or run the included demo:

```bash
python example.py
```

Output:

```
Best price for Wireless Mouse for Premium user: $40.00
Best price for Wireless Mouse for Standard user: $45.00
```

## Running the tests

```bash
pytest
```

12 tests cover each strategy's applicability and discount math
individually, plus the engine's behavior when combining strategies, when
none apply, and when the strategy list is empty.

## Known limitations / next steps

This is a learning project, so it's intentionally simple. Ideas for
extending it:

- Add validation so `PercentageDiscount` rejects negative percentages
  (right now only the upper bound of 70% is enforced).
- Add a `CouponCodeDiscount` strategy that looks up a discount from a
  code string.
- Let `DiscountEngine` return *which* strategy produced the best price,
  not just the number.
- Support stacking multiple discounts together instead of only picking
  the single best one.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE)
for details.
