import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from qiskit_optimization import QuadraticProgram

class MeanVarianceModel:
    def __init__(self, file_path, stock_names):
        self.file_path = file_path
        self.stock_names = stock_names
        self.adj_close_data = None
        self.daily_returns = None
        self.mean_returns = None
        self.covariance_matrix = None

    def load_and_clean_data(self):
        data = pd.read_csv(self.file_path)

        # Remove non-data rows
        data_cleaned = data.drop([0, 1])

        # Convert the first column to datetime and set as index
        data_cleaned['Date'] = pd.to_datetime(data_cleaned.iloc[:, 0])
        data_cleaned.set_index('Date', inplace=True)

        # Select only the columns for Adjusted Close Prices
        adj_close_columns = [col for col in data_cleaned.columns if 'Adj Close' in col]
        self.adj_close_data = data_cleaned[adj_close_columns]

        # Rename columns for clarity
        # self.adj_close_data.columns = ['AAPL', 'AMZN', 'GOOG', 'MSFT', 'TSLA']
        # Rename columns based on provided stock names
        if len(self.stock_names) == len(self.adj_close_data.columns):
            self.adj_close_data.columns = self.stock_names
        else:
            print("Warning: The number of stock names provided does not match the number of columns in the data.")

        # Convert the data to numeric type
        self.adj_close_data = self.adj_close_data.apply(pd.to_numeric)

    def calculate_daily_returns(self):
        self.daily_returns = self.adj_close_data.pct_change().dropna()

    def calculate_mean_and_covariance(self):
        self.mean_returns = self.daily_returns.mean()
        self.covariance_matrix = self.daily_returns.cov()

    def get_mean_returns(self):
        return self.mean_returns.values

    def get_covariance_matrix(self):
        return self.covariance_matrix.values
    
    def plot_adj_close_prices(self):
        if self.adj_close_data is None:
            print("Data not loaded. Please load data using load_and_clean_data method.")
            return

        plt.figure(figsize=(15, 8))

        for column in self.adj_close_data.columns:
            plt.plot(self.adj_close_data.index, self.adj_close_data[column], label=column)

        plt.title('Adjusted Close Prices of AAPL, AMZN, GOOG, MSFT, TSLA')
        plt.xlabel('Date')
        plt.ylabel('Adjusted Close Price')
        plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability
        plt.legend()
        plt.show()
        
        
    def plot_covariance(self):
        plt.figure(figsize=(10, 8))
        sns.heatmap(self.covariance_matrix, annot=True, fmt='.8f', cmap='viridis')
        plt.title('Covariance Matrix Heatmap')
        plt.show()
        
        
    def validate_sizes(self):
        if len(self.mean_returns) != len(self.covariance_matrix):
            print("Sizes do not match: Mean Returns Length:", len(self.mean_returns), 
                  "Covariance Matrix Dimensions:", self.covariance_matrix.shape)
            return False
        if not self.covariance_matrix.shape[0] == self.covariance_matrix.shape[1]:
            print("Covariance matrix is not square:", self.covariance_matrix.shape)
            return False
        return True
        




