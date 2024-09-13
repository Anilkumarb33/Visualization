import os
import pandas as pd
import matplotlib.pyplot as plt

# Specify the base directory
base_directory = os.path.expanduser('~')  # Home directory

# File name to search for
file_name = 'Synthetic_2_classifiers.csv'

# Search for the file in the base directory and its subdirectories
file_location = None
for root, dirs, files in os.walk(base_directory):
    if file_name in files:
        file_location = os.path.join(root, file_name)
        break

# Check if the file was found and proceed
if file_location:
    print(f"File found at: {file_location}")
    
    # Load the dataset
    df = pd.read_csv(file_location)

    # Define conditions for classification
    correct_both = (df['label'] == df['classifierA_predicted_label']) & (df['label'] == df['classifierB_predicted_label'])
    correct_one = ((df['label'] == df['classifierA_predicted_label']) & (df['label'] != df['classifierB_predicted_label'])) | \
                  ((df['label'] != df['classifierA_predicted_label']) & (df['label'] == df['classifierB_predicted_label']))
    incorrect_both = (df['label'] != df['classifierA_predicted_label']) & (df['label'] != df['classifierB_predicted_label'])

    # Assign colors based on classification
    df['color'] = ['black' if both else 'gray' if one else 'white' for both, one in zip(correct_both, correct_one)]

    # Plot the scatterplot
    plt.figure(figsize=(10, 6))
    plt.scatter(df['x'], df['y'], c=df['color'], edgecolor=df['label'].apply(lambda x: 'red' if x == 'dog' else 'blue'))
    plt.title("Projected Data Space", loc='left')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
else:
    print("File not found!")