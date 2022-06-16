#ENSF Final Project
#Authors: Aaryan Sharma and Brandon Phan

# Import appropriate libraries for the tasks of the project.
from enum import unique
from operator import index
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate aggregate stats for entire dataset (Describe method)

def describe_function(df_final):
    """
    The total aggregate stats for the entire DataFrame we have created.
    :param: df_final; the concatinated dataframe
    #:return: none
    """
    agg_stats = df_final.describe()
    print('Aggregate stats for the entire dataset\n', agg_stats)
    

# Function created for the purpose of masking operation, groupby and aggregation computation for a subset of data
def mask_group(totalprints_slice):
    """
    Using the parameter that is based on the user input, a masking operation is performed to store all the values that are over 10,000.
    Groupby is then used to group together the mean of the total print titles held by the service type.

    :param: totalprints_slice; a slice that includes the total print titles and service types related to the inputted year and library area
    :return: none
    """
    
    #Masking operation for if the slice of total number of print copies is over 10,000
    value_over = totalprints_slice[totalprints_slice['Total Print Titles Held'] > 10000]
    #print(value_over)
    group_by = value_over.groupby('Service Type').mean()
    print('\nPrinting the mean of all the total print tiles that are over 10,000 for the inputted year and library area grouped by the service type\n',group_by)
   


def main():
    """
    Reads three Excel files for years 2017, 2018, 2019 with regards to Public Library Statistics in Ontario and converts the content them into three respective DataFrames. 
    Concatenates all the DataFrames into a singular formatted DataFrame with indices set and sorted.
    Checks if DataFrame contains NaN values, if they are present, those values are filled in with zeroes.
    Prompts user to input a year (2017, 2018, 2019) for which they would like to access information in. An area (E.g. Toronto) in which the library
    is based in is prompted afterwards.
    Describe function is used to aggregate a dataset.
    Total titles per cardholder and Total print titles are calculated.
    Calling describe_function and mask_group()
    Export the final dataset after it is indexed, sorted and two columns are added.
    Plot a graph highlighting No. Cardholders vs. Total english titles.

    :param: none
    :return: none
    
    """
    # Stage 1: Dataset Selection
    # Reads the Excel files for 2017, 2018, 2019 respectively
    df_2017 = pd.read_excel('ontario_public_library_statistics_2017.xlsx') 
    df_2018 = pd.read_excel('ontario_public_library_statistics_2018.xlsx') 
    df_2019 = pd.read_excel('ontario_public_library_statistics_2019.xlsx') 

    # Stage 2: DataFrame Creation
    # Using concatenate function to concatenate the 2017 and 2018 DataFrames
    concat_17_18 = pd.concat([df_2017,df_2018]) 

    # We take the result of the concatenated 2017 and 2018 DataFrames and concatenate it with the 2019 DataFrames
    concat_17_18_19 = pd.concat([concat_17_18,df_2019]) 

    print(concat_17_18_19)

    # set the indices, level 1 for 'Year', level 2 for 'Ontario Library Service Region', level 3 for 'Library Full Name', then sorts the index
    df_set_ind = concat_17_18_19.set_index(['Year','Ontario Library Service Region','Library Full Name']) 
    df_final = df_set_ind.sort_index() 


    # Checking if any data contains NaN values, if so an appropriate message is printed
   
    #null_check = df_final.isnull() 
    #print("Checking if there are null values for any element:\n",null_check)


    # Stage 3: User Entry
    # While True loop to prompt the user for input regarding years (2017, 2018, 2019), try and except to catch then raise a ValueError
    while (True):
        input_years = input("Enter a valid year (2017, 2018 or 2019): ")
        try:
                if int(input_years) in set(concat_17_18_19['Year']):
                    break
                else:
                    raise ValueError("You must enter a valid input: ")
        except ValueError as error:
                print(error)

    # While True loop to prompt the user for the area of the library it is in, try and except to catch then raise a ValueError
    while (True):
        input_lib_area = input("Enter the area the library is in: \n")
        try:
                if input_lib_area in set(concat_17_18_19['Ontario Library Service Region']):
                    break
                else:
                    raise ValueError("You must enter a valid input")
        except ValueError as error:
                print(error)

    # Stage 4: Analysis and Calculations
    

    # Function call for describe_function()
    describe_function(df_final)

    # Adding two columns to the combined dataset, Total Print Titles Held and the Total titles per cardholder

    #Total titles
    total_titles = np.add(df_final['Total Print Titles Held'],df_final['Total E-book and E-audio Titles'])
    df_final['Total combined titles'] = total_titles

    #Total titles per cardholder
    print_online_diff=abs(np.subtract(df_final['Total Print Titles Held'],df_final['Total E-book and E-audio Titles']))
    df_final['Difference between print and e-titles'] = print_online_diff

    print("\nThe dataset after 'Total combined titles' and 'Difference between print and e-titles' columns are added \n",df_final)
   
    #Creating a slice to be used in the masking operation and the aggregation computation for a subset of data
    idx = pd.IndexSlice
    slice_inputs = df_final.loc[idx[int(input_years),input_lib_area]]
    print('\nDepicting the data corresponding to the inputted year and library area\n',slice_inputs)
    

    #Creating a slice to be used that includes the total print titles held and serivce types based on the inputted year and library area
    totalprints_slice = df_final.loc[idx[int(input_years),input_lib_area],idx['Service Type','Total Print Titles Held']]

    # Function call for the mask_group()
    mask_group(totalprints_slice)
    
    # Creating and printing a pivot table to display No. Cardholder data 
    pivot_table = df_final.pivot_table(index=['City/Town'], columns = ['Year'], values = ['No. Cardholders'])
    print('\nThe total number of cardholders in each city/town in the respective years\n',pivot_table)

    # Stage 5: Export and Matplotlib
    df_final.to_excel('Final_dataset.xlsx')

    # No. Cardholders in 2017
    x_axis = df_final.loc[idx[2017,'Southern Ontario Library Service'],idx['No. Cardholders']]
    
    # Total print titles held in 2017
    y_axis = df_final.loc[idx[2017,'Southern Ontario Library Service'],idx['Total Print Titles Held']]
   

    # Sorting the number of cardholders to be in an ascending order
    x_axis_sorted,y_axis_sorted=zip(*sorted(zip(x_axis,y_axis)))

    # Plotting a graph showing Titles per cardholder and No. Cardholders
    plt.plot(x_axis_sorted, y_axis_sorted)
    plt.xlabel('No. Cardholders')
    plt.ylabel('Total Print Titles Held')
    plt.title('The total print titles held in comparison to number of cardholders in 2017')
    plt.show()

# Calls the main() function
if __name__ == '__main__':
    main()