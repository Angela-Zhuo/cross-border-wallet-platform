import secrets

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app import models, schemas
from fastapi import FastAPI, Depends, Header, HTTPException
from app.services.routing import select_provider
from app.services.fx import get_fx_rate
from app.services.payment_status import can_transition
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Cross-Border Wallet Integration Platform",
    description="Mock fintech payment gateway for cross-border wallet integrations.",
    version="0.1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "cross-border-wallet"
    }


@app.post("/merchants", response_model=schemas.MerchantResponse)
def create_merchant(
    merchant: schemas.MerchantCreate,
    db: Session = Depends(get_db)
):
    api_key = "cbw_" + secrets.token_urlsafe(32)

    new_merchant = models.Merchant(
        name=merchant.name,
        country=merchant.country,
        settlement_currency=merchant.settlement_currency.upper(),
        api_key=api_key
    )

    db.add(new_merchant)
    db.commit()
    db.refresh(new_merchant)

    return new_merchant

@app.get("/merchants", response_model=list[schemas.MerchantResponse])
def get_merchants(db: Session = Depends(get_db)):
    merchants = db.query(models.Merchant).all()
    return merchants

@app.post("/payments", response_model=schemas.PaymentResponse)
def create_payment(
    payment: schemas.PaymentCreate,
    x_api_key: str = Header(...),
    idempotency_key: str | None = Header(default=None),
    db: Session = Depends(get_db)
):
    merchant = db.query(models.Merchant).filter(
        models.Merchant.api_key == x_api_key
    ).first()

    if not merchant:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if idempotency_key:
        existing_payment = db.query(models.Payment).filter(
            models.Payment.merchant_id == merchant.id,
            models.Payment.idempotency_key == idempotency_key
        ).first()

        if existing_payment:
            return existing_payment

    provider = select_provider(payment.currency, db)

    fx_rate = get_fx_rate(payment.currency, merchant.settlement_currency)
    settlement_amount = payment.amount * fx_rate

    new_payment = models.Payment(
        merchant_id=merchant.id,
        amount=payment.amount,
        currency=payment.currency.upper(),
        provider=provider,
        status="created",
        idempotency_key=idempotency_key,
        customer_currency=payment.currency.upper(),
        merchant_currency=merchant.settlement_currency,
        fx_rate=fx_rate,
        settlement_amount=settlement_amount
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return new_payment

@app.get("/payments", response_model=list[schemas.PaymentResponse])
def get_payments(
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
):
    merchant = db.query(models.Merchant).filter(
        models.Merchant.api_key == x_api_key
    ).first()

    if not merchant:
        raise HTTPException(status_code=401, detail="Invalid API key")

    payments = db.query(models.Payment).filter(
        models.Payment.merchant_id == merchant.id
    ).all()

    return payments

@app.post("/webhooks/mockpay")
def mockpay_webhook(
    webhook: schemas.WebhookPaymentUpdate,
    db: Session = Depends(get_db)
):
    payment = db.query(models.Payment).filter(
        models.Payment.id == webhook.payment_id
    ).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if not can_transition(payment.status, webhook.status):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from {payment.status} to {webhook.status}"
        )

    payment.status = webhook.status
    payment.provider_transaction_id = webhook.provider_transaction_id

    db.commit()
    db.refresh(payment)

    return {
        "message": "Webhook processed successfully",
        "payment_id": payment.id,
        "status": payment.status
    }

@app.post("/providers", response_model=schemas.PaymentProviderResponse)
def create_provider(
    provider: schemas.PaymentProviderCreate,
    db: Session = Depends(get_db)
):
    new_provider = models.PaymentProvider(
        name=provider.name,
        currency=provider.currency.upper(),
        is_active=provider.is_active
    )

    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)

    return new_provider


@app.get("/providers", response_model=list[schemas.PaymentProviderResponse])
def get_providers(db: Session = Depends(get_db)):
    return db.query(models.PaymentProvider).all()