import React, { useState } from 'react'
import './DecisionInsights.css'

function DecisionInsights({ insights, timestamp, criticalCount }) {
  const [filter, setFilter] = useState('all')

  const getPriorityClass = (priority) => {
    const classes = {
      critical: 'priority-critical',
      high: 'priority-high',
      medium: 'priority-medium',
      low: 'priority-low'
    }
    return classes[priority] || ''
  }

  const getDecisionTypeLabel = (type) => {
    const labels = {
      reorder: 'Reorder',
      discontinue: 'Discontinue',
      promote: 'Promote',
      review: 'Review'
    }
    return labels[type] || type
  }

  const filteredInsights = filter === 'all' 
    ? insights 
    : insights.filter(i => i.priority === filter)

  return (
    <div className="decision-insights">
      <div className="insights-header">
        <div>
          <h2>Decision Insights</h2>
          <p className="insights-count">
            {filteredInsights.length} of {insights.length} insights
            {criticalCount > 0 && (
              <span className="critical-badge">{criticalCount} critical</span>
            )}
          </p>
        </div>
        
        <div className="filter-buttons">
          <button
            className={filter === 'all' ? 'active' : ''}
            onClick={() => setFilter('all')}
          >
            All
          </button>
          <button
            className={filter === 'critical' ? 'active' : ''}
            onClick={() => setFilter('critical')}
          >
            Critical
          </button>
          <button
            className={filter === 'high' ? 'active' : ''}
            onClick={() => setFilter('high')}
          >
            High
          </button>
          <button
            className={filter === 'medium' ? 'active' : ''}
            onClick={() => setFilter('medium')}
          >
            Medium
          </button>
          <button
            className={filter === 'low' ? 'active' : ''}
            onClick={() => setFilter('low')}
          >
            Low
          </button>
        </div>
      </div>

      {filteredInsights.length === 0 ? (
        <div className="no-insights">
          No insights match the selected filter.
        </div>
      ) : (
        <div className="insights-list">
          {filteredInsights.map((insight, index) => (
            <div key={index} className={`insight-card ${getPriorityClass(insight.priority)}`}>
              <div className="insight-header">
                <div className="insight-title-section">
                  <h3>{insight.product_name}</h3>
                  <div className="insight-badges">
                    <span className={`badge priority-${insight.priority}`}>
                      {insight.priority.toUpperCase()}
                    </span>
                    <span className="badge decision-type">
                      {getDecisionTypeLabel(insight.decision_type)}
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="insight-body">
                <p className="insight-summary">{insight.summary}</p>
                
                <div className="insight-details">
                  <div className="detail-section">
                    <strong>Reasoning:</strong>
                    <p>{insight.reasoning}</p>
                  </div>
                  
                  <div className="detail-section">
                    <strong>Recommended Action:</strong>
                    <p className="action-text">{insight.recommended_action}</p>
                  </div>
                  
                  {insight.estimated_impact && (
                    <div className="detail-section">
                      <strong>Estimated Impact:</strong>
                      <p>{insight.estimated_impact}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default DecisionInsights
