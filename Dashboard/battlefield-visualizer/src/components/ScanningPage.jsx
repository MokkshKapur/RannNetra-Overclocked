import React, { useState } from 'react';

const ScanningPage = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setSelectedImage(file);
    setLoading(true);
    setError(null);

    // Create FormData to send the image
    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await fetch('http://localhost:5000/analyze', { // Update with your Python API endpoint
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError('Failed to analyze image: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="scanning-page">
      <div className="scanning-header">
        <h1>Battlefield Scan Analysis</h1>
        <p>Upload battlefield images for instant tactical analysis</p>
      </div>

      <div className="scanning-grid">
        {/* Image Upload Section */}
        <div className="scan-section upload-section">
          <h2>Upload Image</h2>
          <div className="upload-area">
            <input 
              type="file" 
              id="imageUpload" 
              className="file-input" 
              accept="image/*"
              onChange={handleImageUpload}
            />
            <label htmlFor="imageUpload" className="upload-label">
              <div className="upload-placeholder">
                {selectedImage ? (
                  <img 
                    src={URL.createObjectURL(selectedImage)} 
                    alt="Selected" 
                    className="preview-image"
                  />
                ) : (
                  <>
                    <span>Drop your image here or click to browse</span>
                    <small>Supports JPG, PNG files</small>
                  </>
                )}
              </div>
            </label>
          </div>
        </div>

        {/* Result Preview Section */}
        <div className="scan-section result-section">
          <h2>Scan Results</h2>
          <div className="result-placeholder">
            {loading ? (
              <div className="loading-spinner">Analyzing...</div>
            ) : error ? (
              <div className="error-message">{error}</div>
            ) : results ? (
              <div className="results-display">
                {/* Display your results here based on API response */}
                <pre>{JSON.stringify(results, null, 2)}</pre>
              </div>
            ) : (
              <span>Upload an image to see analysis results</span>
            )}
          </div>
        </div>

        {/* Detection Details Section */}
        <div className="scan-section details-section">
          <h2>Detection Details</h2>
          <div className="details-placeholder">
            {results ? (
              <>
                <div className="detail-item">
                  <span className="detail-label">Objects Detected:</span>
                  <span className="detail-value">{results.objectsCount || '--'}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Confidence Score:</span>
                  <span className="detail-value">{results.confidence || '--'}%</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Analysis Time:</span>
                  <span className="detail-value">{results.analysisTime || '--'} ms</span>
                </div>
              </>
            ) : (
              <span>Analysis details will appear here</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ScanningPage; 