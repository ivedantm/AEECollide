export default function TopSiteCard({ topSite }) {
  if (!topSite) return null;

  return (
    <div className="why-midland">
      <h3>🏆 Why {topSite.name} Wins</h3>
      <ul>
        <li>
          <strong>Gas Cost Advantage</strong>
          Anchored safely to the {topSite.gas_hub} Hub, enabling highly competitive localized generation costs relative to the broader {topSite.zone} wholesale markets.
        </li>
        <li>
          <strong>High-Yield Volatility</strong>
          Generates an annualized {topSite.positive_hours_pct}% positive-hour frequency, maximizing the physical delta spread over sustained periods.
        </li>
        <li>
          <strong>Strategic Insight</strong>
          {topSite.insight.replace('REAL DATA VERSION: ', '')}
        </li>
      </ul>
    </div>
  )
}
