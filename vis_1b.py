import pandas as pd
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
import os
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.models import FixedTicker, FuncTickFormatter


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
    
    # Total counts of dogs and cats
    total_dog = len(df[df['label'] == 'dog'])
    total_cat = len(df[df['label'] == 'cat'])

    # Classifier A Correctly and Incorrectly Predicted counts
    correct_dog_A = len(df[(df['label'] == 'dog') & (df['classifierA_predicted_label'] == 'dog')])
    correct_cat_A = len(df[(df['label'] == 'cat') & (df['classifierA_predicted_label'] == 'cat')])
    
    # Classifier B Correctly and Incorrectly Predicted counts
    correct_dog_B = len(df[(df['label'] == 'dog') & (df['classifierB_predicted_label'] == 'dog')])
    correct_cat_B = len(df[(df['label'] == 'cat') & (df['classifierB_predicted_label'] == 'cat')])

    
    # Find where both classifiers correctly predicted Dog and cat
    both_correct_dog = len(df[(df['label'] == 'dog') & 
                              (df['classifierA_predicted_label'] == 'dog') & 
                              (df['classifierB_predicted_label'] == 'dog')])

    # Find where both classifiers correctly predicted Cat
    both_correct_cat = len(df[(df['label'] == 'cat') & 
                              (df['classifierA_predicted_label'] == 'cat') & 
                              (df['classifierB_predicted_label'] == 'cat')])

    # Data for Plotting
    categories = ['Classifier A- \ncorrectly predicted Dog',
                  'Classifier B- \ncorrectly predicted Dog',
                  'Classifier A- \ncorrectly predicted Cat',
                  'Classifier B- \ncorrectly predicted Cat']
    
    # Calculate counts for plotting
    grey_counts = [correct_dog_A, correct_dog_B, correct_cat_A, correct_cat_B]
    black_counts = [both_correct_dog, both_correct_dog, both_correct_cat, both_correct_cat]
    
    x_dog = [0.8, 1.2]  # Grouping for dog predictions (Classifier A and B)
    x_cat = [2.8, 3.2]  # Grouping for cat predictions (Classifier A and B)
    x_positions = [0.8, 1.2, 2.8, 3.2] 
    # Create the figure
    output_notebook()
    p = figure(height=600, width=800, title="Assessing Classifiers' Performance for each class.",
               toolbar_location=None, tools="")
    
    # Plot grey bars for correctly predicted labels (by each classifier)
    p.vbar(x=x_dog, top=grey_counts[:2], width=0.3, color='grey')
    p.vbar(x=x_cat, top=grey_counts[2:], width=0.3, color='grey')
    
    # Plot black bars for both classifiers correctly predicted (stacked on top of grey bars)
    p.vbar(x=x_dog, top=black_counts[:2], width=0.3, color='black')
    p.vbar(x=x_cat, top=black_counts[2:], width=0.3, color='black')
    
    
    p.quad(left=[0.5], right=[1.5], bottom=[0], top=[total_dog + 10],  # Set bottom to 0
        fill_color='red', fill_alpha=0.1, line_color='red', line_width=2)

    p.quad(left=[2.5], right=[3.5], bottom=[0], top=[total_cat + 10],  # Set bottom to 0
        fill_color='blue', fill_alpha=0.1, line_color='blue', line_width=2)
    
    labels = ['Classifier A- \ncorrectly predicted Dog', 
          'Classifier B- \ncorrectly predicted Dog',
          'Classifier A- \ncorrectly predicted Cat', 
          'Classifier B- \ncorrectly predicted Cat']
    
    # Set custom tick locations and labels
    p.xaxis.ticker = FixedTicker(ticks=x_positions)
    p.xaxis.formatter = FuncTickFormatter(code="""
        var labels = {'0.8': 'Classifier A- \\ncorrectly \\npredicted Dog',
                      '1.2': 'Classifier B- \\ncorrectly \\npredicted Dog',
                      '2.8': 'Classifier A- \\ncorrectly \\npredicted Cat',
                      '3.2': 'Classifier B- \\ncorrectly \\npredicted Cat'};
        return labels[tick];
    """)
    # Final touches
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.yaxis.axis_label = "Count"

    # Show the plot
    show(p)
    