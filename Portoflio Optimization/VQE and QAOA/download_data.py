import yfinance as yf

def download_stock_data(ticker_symbol, start_date, end_date):
    # Download stock data
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
    # Save the data to a CSV file
    stock_data.to_csv(f"data/{ticker_symbol}_stock_data.csv")

def main():
    # Define the stock ticker symbol
    ticker_symbol = "AAPL"  # Replace with your desired stock ticker
    # Define the start and end dates
    start_date = "2020-01-01"
    end_date = "2024-01-01"
    # Download the stock data
    download_stock_data(ticker_symbol, start_date, end_date)

if __name__ == "__main__":
    main()
