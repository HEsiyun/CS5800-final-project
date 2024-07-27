'''
Siyun He
CS 5800, Summer 2024
Final Project: data generation.py

This program read in a CS5800 student name data. Randomly generates grade between 90 and 100, and assign letter grade according to the numeric grade. Then save it to an excel file.
'''
import pandas as pd
import numpy as np
import uuid


# import excel file
df = pd.read_excel('data.xlsx')
# convert the student_name column to string type
df['student_name'] = df['student_name'].astype(str)
# create a new column with column name 'grade', and randomly assign a grade between 90 to 100 to each student
np.random.seed(8)
df['grade'] = np.random.randint(90, 101, df.shape[0])
# create a new column and assign a grade based on the following conditions: grade <= 93: "A-", grade <= 96: "A", grade <= 100: "A+", ensure the column name is 'grade_letter'
df['grade_letter'] = df['grade'].apply(lambda x: "A-" if x <= 93 else "A" if x <= 96 else "A+")
# generate a unique student ID for each student, and add it to the dataframe as the first column
df.insert(0, 'student_ID', range(1, len(df) + 1))
# save the dataframe to a new excel file
df.to_excel('data_with_grade.xlsx', index=False)