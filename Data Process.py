import pandas as pd
from tqdm import tqdm

# Use tqdm to display progress bar
tqdm.pandas()

# Read data with specified encoding (try 'latin1' or 'ISO-8859-1' if 'utf-8' fails)
print("Step 1: Reading data...")
file_path = 'TweetsUsersLocationsUTUIH2_CSV_2013_22.csv'  # Replace with your file path
data = pd.read_csv(file_path, encoding='ISO-8859-1')  # You can try 'latin1' or 'ISO-8859-1' if UTF-8 does not work
print(f"Step 1: Completed - Data contains {data.shape[0]} rows and {data.shape[1]} columns.\n")


# Convert 'tweet_creation' to datetime format and sort by this column
print("Step 2: Sorting data by 'tweet_creation'...")
data['tweet_creation'] = pd.to_datetime(data['tweet_creation'])
data = data.sort_values(by='tweet_creation')
print("Step 2: Completed - Data sorted by 'tweet_creation'.\n")

# Extract date and time information
print("Step 3: Extracting date and time features...")
data['tweet_year'] = data['tweet_creation'].dt.year
data['tweet_month'] = data['tweet_creation'].dt.month
data['tweet_days'] = data['tweet_creation'].dt.day
data['tweet_hour'] = data['tweet_creation'].dt.hour
data['tweet_day'] = data['tweet_creation'].dt.dayofweek
data['is_weekend'] = data['tweet_day'].apply(lambda x: 1 if x == 5 or x == 6 else 0)
print("Step 3: Completed - Date and time features extracted.\n")

# Keep interaction-related columns and calculate weighted average engagement
print("Step 4: Calculating engagement scores...")
# Calculate weighted engagement using new weights
weights = {'retweet_count': 3, 'reply_count': 4, 'like_count': 3, 'quote_count': 0, 'impression_count': 0}

# Calculate engagement and normalize
data['engagement'] = (
    data['retweet_count'] * weights['retweet_count'] +
    data['reply_count'] * weights['reply_count'] +
    data['like_count'] * weights['like_count'] +
    data['quote_count'] * weights['quote_count'] +
    data['impression_count'] * weights['impression_count']
) / sum(weights.values())
print("Step 4: Completed - Engagement scores calculated.\n")

# Select necessary columns
print("Step 5: Selecting necessary columns...")
data = data[['tweet_year', 'tweet_month', 'tweet_days', 'tweet_hour', 'tweet_day', 'is_weekend',
             'retweet_count', 'reply_count', 'like_count', 'quote_count', 'impression_count', 'engagement']]
print("Step 5: Completed - Columns selected.\n")

# Aggregate data by date
print("Step 6: Aggregating data by date...")
aggregated_data = data.groupby(['tweet_year', 'tweet_month', 'tweet_days'], as_index=False).agg({
    'tweet_hour': 'mean',  # Take mean value
    'tweet_day': 'first',  # Take first (as tweet_day is the same for the same day)
    'is_weekend': 'first',  # Take first (as is_weekend is the same for the same day)
    'retweet_count': 'sum',
    'reply_count': 'sum',
    'like_count': 'sum',
    'quote_count': 'sum',
    'impression_count': 'sum',
    'engagement': 'sum'  # Calculate total engagement for the day
})
print(f"Step 6: Completed - Aggregated data contains {aggregated_data.shape[0]} rows.\n")

# Save to a new CSV file
output_file_path = 'data_processed_filtered1.csv'
aggregated_data.to_csv(output_file_path, index=False)
print(f"Step 7: Completed - Data saved to {output_file_path}\n")

print("Data processing complete.")
