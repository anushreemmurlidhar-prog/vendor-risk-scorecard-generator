import { useEffect, useState } from 'react';
import axios from './services/api';

function App() {
  const [message, setMessage] = useState('Loading backend health...');

  useEffect(() => {
    axios
      .get('/health')
      .then((response) => setMessage(response.data.status || 'Backend healthy'))
      .catch(() => setMessage('Unable to reach backend'));
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white shadow-sm">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-2xl font-semibold">Tool-93</h1>
            <p className="text-sm text-slate-500">Vendor Risk Scorecard Generator</p>
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-6 py-10">
        <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <h2 className="text-xl font-semibold">AI-powered risk scorecards</h2>
          <p className="mt-3 text-slate-600">
            Generate vendor risk scorecards, manage assessments, and review AI recommendations.
          </p>
          <div className="mt-6 rounded-2xl bg-slate-100 p-6">
            <p className="text-slate-700">Backend health status:</p>
            <p className="mt-2 text-lg font-medium text-slate-900">{message}</p>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
