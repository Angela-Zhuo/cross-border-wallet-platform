Cross-Border Wallet Platform

A payment orchestration platform that simulates how modern fintech companies process international payments across multiple payment providers.

The platform allows merchants to integrate once and route transactions through different payment providers while handling FX conversion, settlement, payment lifecycle management, and merchant analytics.

Features

Merchant Onboarding

* Merchant registration
* API key generation
* Merchant settlement currency configuration

Payment Processing

* Payment creation
* API key authentication
* Idempotent payment requests
* Transaction storage

Payment Routing

Dynamic provider selection based on transaction currency.

Example routing:

* CNY → Alipay
* EUR → SEPA
* USD → Stripe
* GBP → Wise

FX Conversion

Cross-border transactions are converted using an FX service.

Example:

Customer pays:

100 CNY

Merchant receives:

12 EUR

Payment Lifecycle

Supported payment states:

* created
* authorized
* captured
* settled
* failed
* refunded

State transitions are validated through the payment workflow engine.

Webhooks

Provider webhooks simulate external payment network notifications and update transaction status.

Merchant Dashboard

Frontend dashboard built with Next.js featuring:

* Total payments
* Customer volume
* Settled volume
* Revenue metrics
* Provider analytics
* Settlement volume visualization

System Architecture

Merchant
↓
Payment Gateway API
↓
Authentication Layer
↓
Routing Engine
↓
Provider Connectors
↓
Webhook Processor
↓
PostgreSQL

Supporting Services:

* FX Service
* Payment Lifecycle Engine
* Analytics Dashboard

Tech Stack

Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Docker

Frontend

* Next.js
* TypeScript
* Tailwind CSS

Infrastructure

* Docker Compose

Running the Project

Start Services

docker compose up --build

Backend:

http://localhost:8000

Swagger Documentation:

http://localhost:8000/docs

Start Frontend

cd frontend
npm install
npm run dev

Frontend:

http://localhost:3000

Example Payment Flow

1. Merchant registers and receives an API key.
2. Merchant submits a payment request.
3. Routing engine selects the appropriate provider.
4. FX service calculates settlement amount.
5. Transaction is stored.
6. Provider sends webhook notifications.
7. Payment lifecycle transitions through authorization, capture and settlement.
8. Merchant monitors transactions through the analytics dashboard.

Future Improvements

* Real payment provider integrations
* JWT authentication
* Merchant roles and permissions
* Fraud detection engine
* Real-time analytics
* Kubernetes deployment
* CI/CD pipeline
* Payment reconciliation engine

Author

Built as a portfolio project focused on payment systems, fintech infrastructure, solution architecture, and cross-border transaction processing.



This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
