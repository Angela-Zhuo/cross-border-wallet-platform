from decimal import Decimal
FX_RATES = {
    ("CNY", "EUR"): Decimal("0.12"),
    ("USD", "EUR"): Decimal("0.88"),
    ("GBP", "EUR"): Decimal("1.17"),
    ("EUR", "EUR"): Decimal("1.00"),
}
def get_fx_rate(source_currency: str, target_currency: str) -> Decimal:

    source = source_currency.upper()

    target = target_currency.upper()

    return FX_RATES.get((source, target), Decimal("1.00"))