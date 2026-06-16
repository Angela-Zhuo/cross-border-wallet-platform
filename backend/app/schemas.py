from pydantic import BaseModel

from decimal import Decimal
from pydantic import BaseModel


class MerchantCreate(BaseModel):
    name: str
    country: str
    settlement_currency: str


class MerchantResponse(BaseModel):
    id: int
    name: str
    country: str
    settlement_currency: str
    api_key: str
    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    amount: Decimal
    currency: str


class PaymentResponse(BaseModel):
    id: int
    merchant_id: int
    amount: Decimal
    currency: str
    provider: str | None
    status: str
    customer_currency: str | None
    merchant_currency: str | None
    fx_rate: Decimal | None
    settlement_amount: Decimal | None
    class Config:
        from_attributes = True

class WebhookPaymentUpdate(BaseModel):
    payment_id: int
    provider_transaction_id: str
    status: str

class PaymentProviderCreate(BaseModel):
    name: str
    currency: str
    is_active: bool = True


class PaymentProviderResponse(BaseModel):
    id: int
    name: str
    currency: str
    is_active: bool

    class Config:
        from_attributes = True