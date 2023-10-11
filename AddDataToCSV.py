
# Date: 9/28/2023

import csv
import pandas as pd

# prompt to answer the number of subjects to be evaluated (number entered should match last subject's number)
numSubs = int(input("Please enter the number of subjects: ")) 
# array to hold values that may need to be skipped
skipping = [] 
# for skipping number entered by user
skipP = 0 

answer = str(input("Are any subjects excluded from the data set? (please enter 'yes' or 'no'): ")) 
# example: if there are 12 subjects, but subject 10 is not included in evaluation
while answer == "yes": 
    # enter the first (or only) subject being skipped, for first iteration
    skipP = int(input("Please enter the number the subject you are excluding (please only enter one at this time): ")) 
    skipping.append(skipP)
    # prompts to enter any more subjects that might be excluded
    answer = str(input("Are any other subjects excluded from the data set? (please enter 'yes' or 'no'): ")) 

output_file = 'output.csv'

# R for "Rest" and E for "Exercise"
breath_types = ['R', 'E'] 

# loop to go through all subject files
for i in range(1, (numSubs + 1)):  
    # skip any subjects as previously specified
    if i in skipping: 
        continue
    for T in breath_types:

        input_file = f"CleanedData/TS{i}{T}1NaNRemoved.csv"
        
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(input_file)
            
            # only take the first 10 rows of file/data
            df = df.iloc[0:10] 

            # 'Subject' column for "TS{i}"
            df['Subject'] = f'TS{i}'  # This will add 'Subject' as the last column
            
            # 'Breath' column for a count value for the row
            df['Breath'] = range(1, len(df) + 1)
            
            # 'Activity State' for the value of T 
            activity = 'Rest' if T == 'R' else 'Exercise'
            df['Activity State'] = activity 
            
            # Reorganize DataFrame to only have the needed columns, in correct order
            df = df[['Subject', 'Activity State', 'Breath', 'Volume Exhaled Timestamps', 'Volume Exhaled (L)', 'VCO2/BV Timestamps', 'Vol CO2 / Vol Breath']]
            
            # Write adjusted DataFrame to output CSV file
            mode = 'a' if i > 1 or T == 'E' else 'w'
            header = False if i > 1 or (i == 1 and T == 'E') else True
            df.to_csv(output_file, mode=mode, header=header, index=False)

        #exception cases
        except FileNotFoundError:
            print(f"{input_file} not found.")
        except pd.errors.EmptyDataError:
            print(f"{input_file} is empty.")
        except Exception as e:
            print(f"An error occurred: {e}")