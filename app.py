import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.neighbors import BallTree
import glob
import os

# Find all CSV files in the '0' directory and its subdirectories
csv_files = glob.glob('0/**/*.csv', recursive=True)

print("CSV files found:", csv_files)

# Initialize an empty list to store DataFrames
dfs = []

for file in csv_files:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file).dropna()
    
    # Append the DataFrame to the list
    dfs.append(df)
    
    print(f"Processed file: {file}, Shape: {df.shape}")

# Combine all DataFrames into a single DataFrame
roundaboutData = pd.concat(dfs, ignore_index=True)

# Convert 'sampledate' column to datetime
roundaboutData['time'] = pd.to_datetime(roundaboutData['sampledate'])

# Sort the DataFrame by 'traceid' and 'time'
roundaboutData = roundaboutData.sort_values(['traceid', 'time'])

# Calculate changes in heading, latitude, and longitude
roundaboutData['heading_change'] = roundaboutData.groupby('traceid')['heading'].diff().abs()
roundaboutData['latitude_change'] = roundaboutData.groupby('traceid')['latitude'].diff().abs()
roundaboutData['longitude_change'] = roundaboutData.groupby('traceid')['longitude'].diff().abs()

# Calculate time difference in seconds
roundaboutData['time_diff'] = roundaboutData.groupby('traceid')['time'].diff().dt.total_seconds()

# Define thresholds for significant changes (adjust these as needed)
heading_change_threshold = 2  # degrees
lat_long_change_threshold = 0.00001  # approximately 1 meter
time_threshold = 10  # seconds

# Create a function to detect potential roundabout behavior
def is_potential_roundabout(row):
    return (
        (row['heading_change'] > heading_change_threshold) and
        (row['latitude_change'] > lat_long_change_threshold or row['longitude_change'] > lat_long_change_threshold) and
        (row['time_diff'] <= time_threshold)
    )

# Apply the function to create a new column 'is_roundabout'
roundaboutData['is_roundabout'] = roundaboutData.apply(is_potential_roundabout, axis=1)

# Select features to use
features_to_use = ['heading', 'latitude', 'longitude', 'speed', 'heading_change', 'latitude_change', 'longitude_change', 'time_diff']
X = roundaboutData[features_to_use]
y = roundaboutData['is_roundabout']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and fit random forest classifier
rfModel = RandomForestClassifier(n_estimators=100, random_state=42)
rfModel.fit(X_train, y_train)

# Make predictions on the entire dataset
all_predictions = rfModel.predict(X)

# Add predictions to the original DataFrame
roundaboutData['predicted_roundabout'] = all_predictions

# Filter and output coordinates predicted to be in a roundabout
roundabout_coordinates = roundaboutData[roundaboutData['predicted_roundabout'] == True][['latitude', 'longitude']]

print("Coordinates predicted to be within roundabouts:")
print(roundabout_coordinates)


print(f"\nNumber of coordinates predicted to be in roundabouts: {len(roundabout_coordinates)}")

# Calculate and print the accuracy score
accuracy = accuracy_score(y, all_predictions)
print(f"\nModel Accuracy: {accuracy:.2f}")

# Print the classification report
print("\nClassification Report:")
print(classification_report(y, all_predictions))

# Print feature importances
feature_importance = pd.DataFrame({'feature': features_to_use, 'importance': rfModel.feature_importances_})
feature_importance = feature_importance.sort_values('importance', ascending=False)
print("\nFeature Importances:")
print(feature_importance)

# Load actual roundabout coordinates
actual_roundabouts = pd.read_csv('./csvdata/hamburg_rounsabouts.csv')

# Function to check if a predicted coordinate is close to an actual roundabout
def is_close_to_actual(lat, lon, actual_coords, threshold=0.001):  # threshold is roughly 100 meters
    return any((abs(lat - actual_lat) < threshold and abs(lon - actual_lon) < threshold) 
               for _, actual_lat, actual_lon in actual_coords[['latitude', 'longitude']].itertuples())

# Check each predicted roundabout against actual roundabouts
true_positives = roundabout_coordinates[roundabout_coordinates.apply(lambda row: is_close_to_actual(row['latitude'], row['longitude'], actual_roundabouts), axis=1)]
false_positives = roundabout_coordinates[~roundabout_coordinates.apply(lambda row: is_close_to_actual(row['latitude'], row['longitude'], actual_roundabouts), axis=1)]

print(f"\nTrue Positives (correctly identified roundabouts): {len(true_positives)}")
print(f"False Positives (incorrectly identified as roundabouts): {len(false_positives)}")

# Calculate precision
precision = len(true_positives) / len(roundabout_coordinates) if len(roundabout_coordinates) > 0 else 0
print(f"\nPrecision: {precision:.2f}")

# Check for missed roundabouts (false negatives)
missed_roundabouts = actual_roundabouts[~actual_roundabouts.apply(lambda row: is_close_to_actual(row['latitude'], row['longitude'], roundabout_coordinates), axis=1)]
print(f"\nMissed Roundabouts (false negatives): {len(missed_roundabouts)}")

# Calculate recall
recall = len(true_positives) / len(actual_roundabouts)
print(f"Recall: {recall:.2f}")

# Calculate F1 score
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
print(f"F1 Score: {f1_score:.2f}")