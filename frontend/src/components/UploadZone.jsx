import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import './UploadZone.css'

export default function UploadZone({ onUpload }) {
  const [isDragActive, setIsDragActive] = useState(false)

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      onUpload(acceptedFiles[0])
    }
  }, [onUpload])

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: { 'text/csv': ['.csv'] },
    maxFiles: 1,
    onDragEnter: () => setIsDragActive(true),
    onDragLeave: () => setIsDragActive(false),
  })

  return (
    <div className="upload-page animate-fade-up">
      {/* Hero text */}
      <div className="upload-hero">
        <div className="upload-hero-eyebrow">AI-Powered Review Analytics</div>
        <h1 className="upload-hero-title">
          Turn Customer Reviews Into
          <span className="upload-hero-gradient"> Business Intelligence</span>
        </h1>
        <p className="upload-hero-sub">
          Upload your reviews CSV and RIAS will automatically classify sentiment,
          identify key issues, and generate prioritised recommendations in seconds.
        </p>
      </div>

      {/* Drop zone */}
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'dropzone--active' : ''}`}
      >
        <input {...getInputProps()} id="csv-upload" />
        <div className="dropzone-icon">📂</div>
        <div className="dropzone-title">
          {isDragActive ? 'Drop it here…' : 'Drop your CSV file here'}
        </div>
        <div className="dropzone-sub">
          or <span className="dropzone-link">click to browse</span> — must contain a <code>review</code> column
        </div>
      </div>

      {/* Divider */}
      <div className="upload-or">
        <span className="upload-or-line" />
        <span className="upload-or-text">or</span>
        <span className="upload-or-line" />
      </div>

      {/* Sample button */}
      <button className="btn-sample" onClick={() => onUpload('sample')}>
        <span>⚡</span> Run on sample data (64 reviews)
      </button>

      {/* Feature pills */}
      <div className="feature-pills">
        {['Sentiment Analysis', 'Category Classification', 'Trend Detection', 'Smart Recommendations', 'CSV Export'].map(f => (
          <span key={f} className="feature-pill">{f}</span>
        ))}
      </div>
    </div>
  )
}
