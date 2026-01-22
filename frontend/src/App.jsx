import React, { useState } from 'react'
import './App.css'
import DataUpload from './components/DataUpload'
import DecisionInsights from './components/DecisionInsights'
import Summary from './components/Summary'

function App() {
  const [decisions, setDecisions] = useState(null)
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleDataUpload = async (file) => {
    setLoading(true)
    setError(null)
    
    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('http://localhost:8000/api/v1/decisions/generate', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to generate decisions')
      }

      const data = await response.json()
      setDecisions(data)
      
      // Fetch summary
      const summaryResponse = await fetch('http://localhost:8000/api/v1/decisions/summary')
      if (summaryResponse.ok) {
        const summaryData = await summaryResponse.json()
        setSummary(summaryData)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateFromCache = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/decisions/generate', {
        method: 'POST',
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to generate decisions')
      }

      const data = await response.json()
      setDecisions(data)
      
      // Fetch summary
      const summaryResponse = await fetch('http://localhost:8000/api/v1/decisions/summary')
      if (summaryResponse.ok) {
        const summaryData = await summaryResponse.json()
        setSummary(summaryData)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Decision Intelligence Platform</h1>
        <p className="subtitle">Transform data into actionable decisions</p>
      </header>

      <main className="app-main">
        <div className="container">
          <DataUpload 
            onUpload={handleDataUpload} 
            onGenerateFromCache={handleGenerateFromCache}
            loading={loading}
          />
          
          {error && (
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          )}

          {summary && <Summary data={summary} />}

          {decisions && (
            <DecisionInsights 
              insights={decisions.insights}
              timestamp={decisions.timestamp}
              criticalCount={decisions.critical_actions}
            />
          )}
        </div>
      </main>
    </div>
  )
}

export default App
