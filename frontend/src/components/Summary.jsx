import React from 'react'
import './Summary.css'

function Summary({ data }) {
  return (
    <div className="summary">
      <div className="summary-card">
        <h2>Decision Summary</h2>
        <div className="summary-grid">
          <div className="summary-item">
            <div className="summary-label">Total Products</div>
            <div className="summary-value">{data.total_products}</div>
          </div>
          
          <div className="summary-item critical">
            <div className="summary-label">Critical Risks</div>
            <div className="summary-value">{data.inventory_risks.critical}</div>
          </div>
          
          <div className="summary-item high">
            <div className="summary-label">High Risks</div>
            <div className="summary-value">{data.inventory_risks.high}</div>
          </div>
          
          <div className="summary-item">
            <div className="summary-label">Slow-Moving Products</div>
            <div className="summary-value">{data.slow_moving_products}</div>
          </div>
          
          <div className="summary-item">
            <div className="summary-label">Reorder Recommendations</div>
            <div className="summary-value">{data.reorder_recommendations}</div>
          </div>
          
          <div className="summary-item">
            <div className="summary-label">Total Inventory Risks</div>
            <div className="summary-value">{data.inventory_risks.total}</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Summary
