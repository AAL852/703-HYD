import pandas as pd

# Step 1: Read in the data
data = pd.read_csv('TweetsUsersLocationsUTUIH2_CSV_2013_22.csv')

# Step 2: Convert 'tweet_creation' to datetime format
data['tweet_creation'] = pd.to_datetime(data['tweet_creation'])

# Step 3: Sort the data by 'tweet_creation'
data_sorted = data.sort_values(by='tweet_creation')

# Step 4: Evenly sample 10,000 data points from the sorted DataFrame
sampled_data = data_sorted.iloc[::len(data_sorted) // 10000]

# Step 5: Save the sampled data
sampled_data.to_csv('sampled_data.csv', index=False)