import { useState } from 'react';
import { PredictionForm } from './components/PredictionForm';
import { ResultPage } from './pages/ResultPage';
import './App.css';

function App() {
  const [predictedPrice, setPredictedPrice] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handlePredict = (price: number) => {
    setPredictedPrice(price);
  };

  const handleReset = () => {
    setPredictedPrice(null);
    setError('');
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🏠 House Price Prediction</h1>
        <p className="subtitle">Predict property prices using ML</p>
      </header>

      <main className="main-content">
        {!predictedPrice ? (
          <>
            {error && <div className="error-banner">{error}</div>}
            <PredictionForm
              onPredict={handlePredict}
              onLoading={setLoading}
              onError={setError}
            />
            {loading && <div className="loading">Predicting...</div>}
          </>
        ) : (
          <ResultPage predictedPrice={predictedPrice} onReset={handleReset} />
        )}
      </main>

      <footer className="footer">
        <p>ML Model • House Price Prediction • 2025</p>
      </footer>
    </div>
  );
}

export default App;
