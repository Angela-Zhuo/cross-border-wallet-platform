from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean

from app.database import Base


class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    api_key = Column(String, unique=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    payments = relationship("Payment", back_populates="merchant")
    settlement_currency = Column(String, nullable=False, default="EUR")



class PaymentProvider(Base):
    __tablename__ = "payment_providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String, nullable=False)
    provider = Column(String, nullable=True)
    status = Column(String, default="created")

    provider_transaction_id = Column(String, nullable=True)
    idempotency_key = Column(String, unique=True, nullable=True)

    customer_currency = Column(String, nullable=True)
    merchant_currency = Column(String, nullable=True)
    fx_rate = Column(Numeric(10, 4), nullable=True)
    settlement_amount = Column(Numeric(10, 2), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    merchant = relationship("Merchant", back_populates="payments")