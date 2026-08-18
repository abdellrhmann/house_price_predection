import React from 'react';
import '../styles/result.css';

interface ResultPageProps {
  predictedPrice: number | null;
  onReset: () => void;
}

const formatPrice = (price: number): string => {
  if (price >= 10000000) {
    return `₹${(price / 10000000).toFixed(2)} Cr`;
  } else if (price >= 100000) {
    return `₹${(price / 100000).toFixed(2)} Lac`;
  }
  return `₹${price.toFixed(0)}`;
};

export const ResultPage: React.FC<ResultPageProps> = ({ predictedPrice, onReset }) => {
  if (predictedPrice === null) {
    return null;
  }

  return (
    <div className="result-page">
      <div className="result-card">
        <h2>Prediction Result</h2>
        <div className="result-value">
          <p className="label">Estimated Price</p>
          <p className="price">{formatPrice(predictedPrice)}</p>
        </div>
        <p className="description">
          Based on the provided property details, our model predicts this price range for your property.
        </p>
        <button onClick={onReset} className="btn-predict-again">
          Predict Another Property
        </button>
      </div>
    </div>
  );
};
