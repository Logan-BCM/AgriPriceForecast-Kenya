import matplotlib.pyplot as plt
import seaborn as sns



def plot_price_trend(products_df, commodity, location=None):
    """Plot historical price trends for a specific commodity."""
    subset = products_df[products_df['Commodity'] == commodity]
    if location:
        subset = subset[subset['Location'] == location]
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='Date', y='Price', data=subset, hue='Location')
    plt.title(f'Price Trend for {commodity}')
    plt.xlabel('Date')
    plt.ylabel('Price (KSh)')
    plt.xticks(rotation=45)
    plt.legend(title='Location')
    plt.grid(True)
    plt.show()

def plot_geographical_distribution(products_df, date):
    """Plot a geographical heatmap of commodity prices for a given date."""
    subset = products_df[products_df['Date'] == date]
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Longitude', y='Latitude', hue='Price', size='Price', data=subset, palette='viridis', legend=True)
    plt.title(f'Commodity Prices on {date}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.show()

def plot_sentiment_analysis(products_df):
    """Plot sentiment analysis results as a bar chart."""
    sentiment_counts = products_df['Sentiment'].value_counts()
    
    plt.figure(figsize=(8, 5))
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette='coolwarm')
    plt.title('Sentiment Analysis of Market Discussions')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.grid(axis='y')
    plt.show()

def plot_histogram(products_df, column):
    """Plot a histogram for a given column."""
    plt.figure(figsize=(8, 5))
    sns.histplot(products_df[column], bins=20, kde=True, color='blue')
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

def plot_bar_chart(products_df, category_col, value_col):
    """Plot a bar chart for categorical data."""
    plt.figure(figsize=(10, 6))
    sns.barplot(x=category_col, y=value_col, data=products_df, palette='viridis')
    plt.title(f'Bar Chart of {value_col} by {category_col}')
    plt.xlabel(category_col)
    plt.ylabel(value_col)
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.show()

def plot_scatter(products_df, x_col, y_col, hue=None):
    """Plot a scatter plot for two numerical variables."""
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=x_col, y=y_col, data=products_df, hue=hue, palette='coolwarm')
    plt.title(f'Scatter Plot of {x_col} vs {y_col}')
    plt.xlabel('')
    plt.ylabel(y_col)
    plt.grid(True)
    plt.show()

def plot_boxplot(products_df, y_col):
    """Plot a boxplot to visualize distributions."""
    plt.figure(figsize=(8, 6))
    sns.boxplot(y=y_col, data=products_df, palette='pastel')
    plt.title(f'Boxplot of {y_col}')
    plt.xlabel('')
    plt.ylabel(y_col)
    plt.grid(True)
    plt.show()

    
def plot_pairplot(products_df, columns):
    """Plot a pairplot to visualize relationships between numerical variables."""
    sns.pairplot(products_df[columns], diag_kind='kde', plot_kws={'alpha': 0.7})
    plt.show()

# Example usage (assuming products_df is your DataFrame)
# plot_price_trend(products_df, 'Maize', 'Nairobi')
# plot_geographical_distribution(products_df, '2025-01-01')
# plot_sentiment_analysis(sentiment_products_df)
# plot_histogram(products_df, 'Price')
# plot_bar_chart(products_df, 'Location', 'Price')
# plot_scatter(products_df, 'Price', 'Quantity')
# plot_boxplot(products_df, 'Location', 'Price')
# plot_pairplot(products_df, ['Price', 'Quantity', 'Latitude', 'Longitude'])
