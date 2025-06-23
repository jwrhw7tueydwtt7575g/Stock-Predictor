# 📈 Stock Price Predictor with ARIMA (FastAPI + Docker)

A lightweight and interactive web application to forecast stock prices using the ARIMA model.  
It fetches historical data via **Yahoo Finance**, applies **time series forecasting**, and shows the results with an interactive **candlestick chart + future predictions**.

---

## 🚀 Features

- 📥 Input any stock ticker (e.g., `AAPL`, `TSLA`, `RELIANCE.NS`)
- 📊 Displays 6 months of **candlestick** price history
- 🔮 Predicts the next **30 days** using ARIMA
- 📉 Shows **RMSE** (prediction accuracy)
- 📦 Containerized using **Docker**
- 🧠 Built with FastAPI, Plotly, Jinja2, and yFinance

---

## 🖥️ Demo Screenshot

> *(Add your screenshot here later)*  

yaml
Copy
Edit

---

## 🧰 Tech Stack

- **Backend:** Python, FastAPI, ARIMA (statsmodels)
- **Frontend:** Jinja2 Templates + Plotly.js
- **Data Source:** Yahoo Finance (`yfinance`)
- **Packaging:** Docker
- **Others:** Scikit-learn, NumPy, Pandas

---

## 📂 Project Structure

Stock-Predictor/
├── main.py # FastAPI app
├── model_train.py # Forecasting logic (ARIMA)
├── requirements.txt # Python dependencies
├── Dockerfile # Containerization setup
├── templates/
│ └── index.html # HTML UI
├── static/
│ └── style.css # Optional CSS styling

yaml
Copy
Edit

---

## ⚙️ How to Run Locally

### 🔹 Option 1: Python (without Docker)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn main:app --reload
Open in browser: http://localhost:8000

🔹 Option 2: Using Docker
bash
Copy
Edit
# Build Docker image
docker build -t stock-forecast-app .

# Run the container
docker run -p 8000:8000 stock-forecast-app
Visit: http://localhost:8000

📈 Example Tickers
Try tickers like:

AAPL (Apple)

TSLA (Tesla)

INFY.NS (Infosys India)

RELIANCE.NS (Reliance Industries)

📃 License
MIT License © 2025 Vivek Chaudhari

vbnet
Copy
Edit

Let me know if you'd like to:
- Add a real screenshot to the `README`
- Auto-deploy this from GitHub to the web using Render or Railway
- Link your LinkedIn/GitHub in the footer of the app or README
