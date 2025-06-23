from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import plotly.graph_objs as go
import yfinance as yf
from model_train import (
    get_data, get_differencing_order, scaling,
    inverse_scaling, get_forecast, evaluate_model
)

app = FastAPI()

# Mount static and template directories
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, ticker: str = Form(...)):
    try:
        # Download close price
        close_price = get_data(ticker)
        d_order = get_differencing_order(close_price)
        scaled_data, scaler = scaling(close_price)

        rmse = evaluate_model(scaled_data, d_order)
        forecast_df = get_forecast(scaled_data, d_order)
        forecast_df['Close'] = inverse_scaling(scaler, forecast_df['Close']).flatten()

        # Get full OHLC historical data for candlestick
        ohlc_data = yf.download(ticker, period="6mo")

        fig = go.Figure()

        # Historical candlestick
        fig.add_trace(go.Candlestick(
            x=ohlc_data.index,
            open=ohlc_data['Open'],
            high=ohlc_data['High'],
            low=ohlc_data['Low'],
            close=ohlc_data['Close'],
            name='Historical'
        ))

        # Forecast line chart
        fig.add_trace(go.Scatter(
            x=forecast_df.index,
            y=forecast_df['Close'],
            mode='lines+markers',
            name='Forecast (Close)',
            line=dict(color='blue', width=2)
        ))

        fig.update_layout(
            title=f"Candlestick + 30-Day Forecast for {ticker}",
            xaxis_title="Date",
            yaxis_title="Price",
            xaxis_rangeslider_visible=False,
            template="plotly_white"
        )

        plot_html = fig.to_html(full_html=False)

        return templates.TemplateResponse("index.html", {
            "request": request,
            "ticker": ticker.upper(),
            "rmse": rmse,
            "plot_html": plot_html
        })

    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Error: {str(e)}. Please try a valid stock ticker like 'AAPL' or 'TSLA'."
        })
