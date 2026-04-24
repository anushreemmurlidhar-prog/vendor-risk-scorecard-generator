export default function VendorTile({ vendor }) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
      <h3 className="text-lg font-semibold">{vendor.name}</h3>
      <p className="mt-2 text-slate-600">Risk score: {vendor.riskScore}</p>
    </div>
  );
}
