from sqlalchemy.orm import Session

from app import models


def select_provider(currency: str, db: Session) -> str:
    provider = db.query(models.PaymentProvider).filter(
        models.PaymentProvider.currency == currency.upper(),
        models.PaymentProvider.is_active == True
    ).first()

    if provider:
        return provider.name

    return "MockPay"