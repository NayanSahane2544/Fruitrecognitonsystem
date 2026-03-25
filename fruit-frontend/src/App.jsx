import React, { useState, useRef } from 'react';
import axios from 'axios';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';
import { Download, History, ChevronRight, UploadCloud, Trash2 } from 'lucide-react';
import './App.css';

const COLORS = ['#f1c40f', '#e74c3c', '#3498db']; // Carbs, Protein, Fat

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [scanHistory, setScanHistory] = useState([]); 
  
  const reportRef = useRef(null); 

  // Handle User selecting an image
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreview(URL.createObjectURL(file));
      setResult(null); // Clear previous results on new selection
    }
  };

  // Send the image to the Flask Backend
  const handleUpload = async () => {
    if (!selectedImage) return;
    setLoading(true);
    
    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await axios.post('http://127.0.0.1:5000/predict', formData);
      const data = response.data;
      setResult(data);
      
      // Update Sidebar History (keeps the 5 most recent scans)
      setScanHistory(prev => [
        { id: Date.now(), fruit: data.fruit, conf: data.confidence, img: preview },
        ...prev
      ].slice(0, 5));

    } catch (error) {
      console.error(error);
      alert("Analysis failed. Please ensure your Python Flask server is running on port 5000.");
    } finally {
      setLoading(false);
    }
  };

  // Capture the results section and save as PDF
  const downloadPDF = () => {
    const input = reportRef.current;
    html2canvas(input, { scale: 2, useCORS: true }).then((canvas) => {
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`${result.fruit}_AI_Analysis_Report.pdf`);
    });
  };

  return (
    <div className="app-layout">
      
      {/* LEFT PANEL: Sidebar History */}
      <div className="history-sidebar">
        
        {/* Header with Clear Button */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#2c3e50', margin: 0 }}>
            <History size={20} /> Recent Scans
          </h3>
          
          {/* Only show the Clear button if there is history to clear */}
          {scanHistory.length > 0 && (
            <button 
              onClick={() => setScanHistory([])}
              style={{ 
                background: 'none', border: 'none', color: '#e74c3c', cursor: 'pointer', 
                display: 'flex', alignItems: 'center', gap: '5px', fontSize: '12px', fontWeight: 'bold' 
              }}
            >
              <Trash2 size={14} /> Clear
            </button>
          )}
        </div>
        
        {scanHistory.length === 0 ? (
          <p style={{ color: '#95a5a6', fontSize: '14px', textAlign: 'center', marginTop: '20px' }}>
            No recent scans yet.
          </p>
        ) : null}

        {scanHistory.map(item => (
          <div key={item.id} className="history-item">
            <img src={item.img} alt="thumb" className="history-thumb" />
            <div style={{ flex: 1 }}>
              <strong style={{ fontSize: '15px', color: '#333' }}>{item.fruit}</strong>
              <div style={{ fontSize: '12px', color: '#27ae60', fontWeight: 'bold' }}>
                {item.conf.toFixed(1)}% Match
              </div>
            </div>
            <ChevronRight size={18} color="#bdc3c7" />
          </div>
        ))}
      </div>

      {/* RIGHT PANEL: Main Dashboard */}
      <div className="dashboard-container">
        
        <header className="dashboard-header">
          <span style={{ fontSize: '2rem' }}>🍎</span>
          <h1>AI Agri-Tech Recognition System</h1>
        </header>

        <div className="dashboard-content">
          
          {/* UPLOAD CONTROLS */}
          <div className="upload-section">
            <div className="upload-box">
              <input type="file" className="file-input" onChange={handleImageChange} accept="image/png, image/jpeg" />
              <UploadCloud size={48} color="#bdc3c7" style={{ margin: '0 auto 10px auto' }} />
              <h3 style={{ color: '#2c3e50' }}>Drag & Drop Image</h3>
              <p style={{ color: '#7f8c8d', fontSize: '14px', marginTop: '5px' }}>or click to browse files</p>
            </div>
            
            {preview && (
              <img src={preview} alt="Preview" style={{ width: '130px', height: '130px', objectFit: 'cover', borderRadius: '15px', border: '1px solid #ecf0f1' }} />
            )}
            
            <button className="upload-btn" onClick={handleUpload} disabled={!selectedImage || loading}>
              {loading ? "Scanning pixels..." : "Analyze Fruit"}
            </button>
          </div>

          {/* LOADING STATE (Skeleton UI) */}
          {loading && (
            <div style={{ padding: '20px' }}>
               <div className="skeleton skeleton-title"></div>
               <div className="skeleton skeleton-text"></div>
               <div className="charts-container">
                 <div className="skeleton skeleton-chart"></div>
                 <div className="skeleton skeleton-chart"></div>
               </div>
            </div>
          )}

          {/* RESULTS STATE */}
          {result && !loading && (
            <div ref={reportRef} style={{ background: 'white', padding: '10px 20px', borderRadius: '10px' }}>
              
              <div className="report-header">
                <div>
                  <h2 style={{ fontSize: '2.5rem', color: '#2c3e50', margin: 0 }}>
                    {result.fruit} 
                    <span style={{ fontSize: '1.2rem', fontStyle: 'italic', color: '#7f8c8d', marginLeft: '10px' }}>
                      ({result.scientific_name})
                    </span>
                  </h2>
                  <div className="confidence-badge">
                    {result.confidence.toFixed(1)}% AI Confidence
                  </div>
                </div>
                
                <button onClick={downloadPDF} className="export-btn">
                  <Download size={18} /> Export Report
                </button>
              </div>

              <p style={{ color: '#555', marginTop: '15px', fontSize: '1.05rem', lineHeight: '1.6' }}>
                {result.description}
              </p>

              {/* STATS ROW (Calories) */}
              <div className="stats-row">
                <div className="stat-pill">
                  🔥 <strong>Calories:</strong> {result.calories}
                </div>
              </div>

              {/* DATA CHARTS */}
              <div className="charts-container">
                
                {/* Chart 1: Macros */}
                <div className="chart-card">
                  <h4>🧬 Nutritional Profile</h4>
                  <ResponsiveContainer width="100%" height={220}>
                    <PieChart>
                      <Pie data={result.macros} cx="50%" cy="50%" innerRadius={60} outerRadius={90} paddingAngle={5} dataKey="value">
                        {result.macros.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                  <div style={{ display: 'flex', justifyContent: 'center', gap: '15px', fontSize: '13px', fontWeight: '500' }}>
                    <span style={{ color: COLORS[0] }}>● Carbs</span>
                    <span style={{ color: COLORS[1] }}>● Protein</span>
                    <span style={{ color: COLORS[2] }}>● Fat</span>
                  </div>
                </div>

                {/* Chart 2: Cultivation */}
                <div className="chart-card">
                  <h4>🇮🇳 Cultivation by State</h4>
                  <ResponsiveContainer width="100%" height={250}>
                    <BarChart data={result.cultivation} layout="vertical" margin={{ top: 5, right: 30, left: 10, bottom: 5 }}>
                      <XAxis type="number" hide />
                      <YAxis dataKey="state" type="category" width={90} fontSize={13} fontWeight="500" tickLine={false} axisLine={false} />
                      <Tooltip cursor={{fill: '#f8f9fa'}} />
                      <Bar dataKey="percent" fill="#2ecc71" radius={[0, 10, 10, 0]} barSize={24} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* CULINARY USES (Local Images) */}
              <div className="chart-card" style={{ marginTop: '20px' }}>
                <h4>🍽️ Popular Culinary Uses</h4>
                <div className="dishes-grid">
                  {result.dish_images.map((dish, i) => (
                    <div key={i} className="dish-card">
                      {/* Notice crossOrigin is removed as it's hosted locally now */}
                      <img src={dish.url} alt={dish.name} />
                      <p style={{ textAlign: 'center', marginTop: '10px', fontSize: '14px', fontWeight: '600', color: '#2c3e50' }}>
                        {dish.name}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;