'''
Siyun He
CS 5800, Summer 2024
Final Project: read_data.py

This program reads data from an excel file by taking user input filepath and filename. It also let user choose a unique column to be the index of the dataframe.
The program will check whether the file exists and whether the file is in the correct format. Also, it will check whether the column is unique, has correct type and exists in the dataframe.
'''
import pandas as pd
import sys


def read_in_data() -> pd.DataFrame:
    '''
    Function read_in_data
    This function reads the data from an excel file by taking user input filepath and filename.
    Returns the dataframe of the data.
    '''
    try:
        filepath = input("Please enter the data file path and name: ")
    except IndexError:
        print("Please enter correct data file path and name")
        return
    
    try:
        data = pd.read_excel(filepath)
        return data
    except FileNotFoundError as error:
        print("File not found:", type(error), error)
    except TypeError as error:
        print("Invalid type:", type(error), error)
    except Exception as error:
        print("Error:", type(error), error)


def choose_index(data: pd.DataFrame) -> str:
    '''
    Function choose_index
    This function let user choose a unique column to be the index of the dataframe.
    Parameter:
    data -- the dataframe of the data
    Returns the name of the column that is set as index.
    '''
    all_columns = data.columns.tolist()
    print(f"The columns in the dataframe are: {all_columns} \nYou can choose one of the columns to be the index. The column must be unique, and the data type must be string or numeric.")
    try:
        column_name = input("Please enter the column name you want to set as index: ")
    except IndexError:
        print("Please enter correct column name")
        return
    
    try:
        if column_name not in data.columns:
            raise Exception("Column name does not exist in the dataframe")
        if not data[column_name].is_unique:
            raise Exception("Column is not unique")
        return column_name
    except TypeError as error:
        print("Invalid type:", type(error), error)
    except Exception as error:
        print("Error:", type(error), error)

