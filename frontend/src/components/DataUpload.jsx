import React, { useRef } from 'react'
import './DataUpload.css'

function DataUpload({ onUpload, onGenerateFromCache, loading }) {
  const fileInputRef = useRef(null)

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      onUpload(file)
    }
  }

  const handleClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="data-upload">
      <div className="upload-card">
        <h2>Upload Transaction Data</h2>
        <p className="upload-description">
          Upload a CSV file with your transaction data to generate decision insights.
        </p>
        
        <div className="upload-actions">
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
          <button 
            onClick={handleClick}
            disabled={loading}
            className="upload-button primary"
          >
            {loading ? 'Processing...' : 'Upload CSV File'}
          </button>
          
          <button
            onClick={onGenerateFromCache}
            disabled={loading}
            className="upload-button secondary"
          >
            {loading ? 'Generating...' : 'Generate from Cached Data'}
          </button>
        </div>

        <div className="csv-format-info">
          <h3>Expected CSV Format:</h3>
          <pre>
{`transaction_id,product_id,product_name,quantity,unit_price,transaction_date,customer_id
TXN001,PROD001,Widget A,5,10.50,2024-01-15T10:30:00,CUST001
TXN002,PROD002,Widget B,2,25.00,2024-01-15T11:00:00,CUST002`}
          </pre>
        </div>
      </div>
    </div>
  )
}

export default DataUpload
