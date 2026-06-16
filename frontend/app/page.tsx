"use client";

import { useState } from "react";

type Payment = {
  id: number;
  merchant_id: number;
  amount: string;
  currency: string;
  provider: string | null;
  status: string;
  customer_currency: string | null;
  merchant_currency: string | null;
  fx_rate: string | null;
  settlement_amount: string | null;
};

export default function Home() {
  const [apiKey, setApiKey] = useState("");
  const [payments, setPayments] = useState<Payment[]>([]);
  const [error, setError] = useState("");

  const totalPayments = payments.length;
  const totalVolume = payments.reduce((sum, p) => sum + Number(p.amount), 0);

  const settledVolume = payments
    .filter((p) => p.status === "settled")
    .reduce((sum, p) => sum + Number(p.settlement_amount || 0), 0);

  const monthlyRevenue = settledVolume;

  const providerStats = payments.reduce<
    Record<string, { count: number; volume: number; settled: number }>
  >((acc, payment) => {
    const provider = payment.provider || "Unknown";

    if (!acc[provider]) {
      acc[provider] = { count: 0, volume: 0, settled: 0 };
    }

    acc[provider].count += 1;
    acc[provider].volume += Number(payment.amount || 0);

    if (payment.status === "settled") {
      acc[provider].settled += Number(payment.settlement_amount || 0);
    }

    return acc;
  }, {});

  const providerRows = Object.entries(providerStats);

  const maxSettledVolume = Math.max(
    ...providerRows.map(([, stats]) => stats.settled),
    1
  );

  async function fetchPayments() {
    setError("");

    const response = await fetch("http://localhost:8000/payments", {
      headers: {
        "x-api-key": apiKey,
      },
    });

    if (!response.ok) {
      setError("Could not fetch payments. Check your API key.");
      return;
    }

    const data = await response.json();
    setPayments(data);
  }

  return (
    <main className="min-h-screen bg-gray-50 p-10 text-gray-900">
      <h1 className="text-3xl font-bold">Merchant Payment Dashboard</h1>

      <p className="mt-2 text-gray-600">
        Monitor cross-border payments, FX conversion and settlement status.
      </p>

      <div className="mt-8 flex gap-3">
        <input
          className="w-full rounded border bg-white p-3"
          placeholder="Paste merchant API key"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        />

        <button
          onClick={fetchPayments}
          className="rounded bg-black px-5 py-3 text-white"
        >
          Load Payments
        </button>
      </div>

      {error && <p className="mt-4 text-red-600">{error}</p>}

      <div className="mt-8 grid grid-cols-4 gap-4">
        <div className="rounded bg-white p-5 shadow">
          <p className="text-sm text-gray-500">Total Payments</p>
          <p className="mt-2 text-2xl font-bold">{totalPayments}</p>
        </div>

        <div className="rounded bg-white p-5 shadow">
          <p className="text-sm text-gray-500">Customer Volume</p>
          <p className="mt-2 text-2xl font-bold">{totalVolume.toFixed(2)}</p>
        </div>

        <div className="rounded bg-white p-5 shadow">
          <p className="text-sm text-gray-500">Settled Volume</p>
          <p className="mt-2 text-2xl font-bold">{settledVolume.toFixed(2)}</p>
        </div>

        <div className="rounded bg-white p-5 shadow">
          <p className="text-sm text-gray-500">Monthly Revenue</p>
          <p className="mt-2 text-2xl font-bold">{monthlyRevenue.toFixed(2)}</p>
        </div>
      </div>

      <div className="mt-8 overflow-hidden rounded bg-white shadow">
        <table className="w-full text-left text-sm">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-3">ID</th>
              <th className="p-3">Amount</th>
              <th className="p-3">Provider</th>
              <th className="p-3">FX</th>
              <th className="p-3">Settlement</th>
              <th className="p-3">Status</th>
            </tr>
          </thead>

          <tbody>
            {payments.map((p) => (
              <tr key={p.id} className="border-t">
                <td className="p-3">{p.id}</td>
                <td className="p-3">
                  {p.amount} {p.customer_currency}
                </td>
                <td className="p-3">{p.provider}</td>
                <td className="p-3">{p.fx_rate}</td>
                <td className="p-3">
                  {p.settlement_amount} {p.merchant_currency}
                </td>
                <td className="p-3">{p.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-8 overflow-hidden rounded bg-white shadow">
        <div className="border-b p-4">
          <h2 className="text-lg font-semibold">Provider Analytics</h2>
          <p className="text-sm text-gray-500">
            Payment volume and settled amount by provider.
          </p>
        </div>

        <table className="w-full text-left text-sm">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-3">Provider</th>
              <th className="p-3">Transactions</th>
              <th className="p-3">Customer Volume</th>
              <th className="p-3">Settled Volume</th>
            </tr>
          </thead>

          <tbody>
            {providerRows.map(([provider, stats]) => (
              <tr key={provider} className="border-t">
                <td className="p-3">{provider}</td>
                <td className="p-3">{stats.count}</td>
                <td className="p-3">{stats.volume.toFixed(2)}</td>
                <td className="p-3">{stats.settled.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-8 rounded bg-white p-6 shadow">
        <h2 className="text-lg font-semibold">Settlement Volume by Provider</h2>

        <p className="mt-1 text-sm text-gray-500">
          Visual breakdown of settled volume per payment provider.
        </p>

        <div className="mt-6 space-y-4">
          {providerRows.map(([provider, stats]) => {
            const widthPercentage = (stats.settled / maxSettledVolume) * 100;

            return (
              <div key={provider}>
                <div className="mb-1 flex justify-between text-sm">
                  <span>{provider}</span>
                  <span>{stats.settled.toFixed(2)}</span>
                </div>

                <div className="h-3 rounded bg-gray-200">
                  <div
                    className="h-3 rounded bg-black"
                    style={{ width: `${widthPercentage}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </main>
  );
}