export interface PredictionRequest {
  location: string;
  carpet_area_sqft: number;
  floor_num: number;
  bathroom: number;
  balcony: number;
  furnishing: string;
  transaction: string;
  ownership: string;
  facing: string;
  car_parking: number;
}

export interface PredictionResponse {
  predicted_price: number;
  message: string;
}

export interface FormData extends PredictionRequest {}
