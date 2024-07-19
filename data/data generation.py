import pandas as pd
import numpy as np
# import excel file
df = pd.read_excel('data.xlsx')
# create a new column with column name 'grade', and randomly assign a grade between 90 to 100 to each student
np.random.seed(8)
df['grade'] = np.random.randint(90, 101, df.shape[0])
# create a new column and assign a grade based on the following conditions: grade <= 93: "A-", grade <= 96: "A", grade <= 100: "A+", ensure the column name is 'grade_letter'
df['grade_letter'] = df['grade'].apply(lambda x: "A-" if x <= 93 else "A" if x <= 96 else "A+")
# save the dataframe to a new excel file
df.to_excel('data_with_grade.xlsx', index=False)