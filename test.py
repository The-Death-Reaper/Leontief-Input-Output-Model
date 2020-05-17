import numpy as np
import math

# This implementation serves the purpose of validating the Leonteif Input Output Model
# The dataset was downloaded from the website 'https://stats.oecd.org/Index.aspx?DataSetCode=IOTS'
# The dataset pertains to the economy of India in the year 2015
# The dataset contains the Input Output table for that year,
# And the Leonteif Inverse Matrix

data = np.genfromtxt('total_india.csv', dtype = None, delimiter = ',', skip_header = 1)
U = [row for row in data]
table2 = []
for row in U:
    i = 0
    row2 = []
    for item in row:        
        row2.append(math.fabs(float(item)))
        i += 1
    table2.append(row2)

# temp stores the input output table as is, in a matrix form
temp = np.matrix(table2)    
np.save('temp', temp)

# From total.csv, we get the total output for each sector
# We divide the inputs of each sector to other sectors (i.e a column in temp matrix) 
# with the total output of that specific sector (i.e the sum of the row for the corresponding sectors)
# to get the consumption matrix
total_output = [np.genfromtxt('total.csv', dtype = None, delimiter = ',', skip_header = 1)]
total_output = [i for i in np.array(total_output)[0]]
total_output_r = []
for i in total_output:
    if(i!=0):
        total_output_r.append(1/i)
    else:
        total_output_r.append(i)

C_matrix = []
for i in range(temp.shape[0]):
    temp_row = []
    for j in range(len(total_output)):
        temp_row.append(temp[i,j]*total_output_r[j])
    C_matrix.append(temp_row)
C_matrix = np.matrix(C_matrix)
np.save('C_matrix', C_matrix)

# Using the calculated consumption matrix, we calculate the 
# Leontief Inverse Matrix and compare it with the Matrix provided
lim_calc = np.linalg.inv(np.identity(temp.shape[0])-C_matrix)
np.save("lim_calc", lim_calc)

data1 = np.genfromtxt('lim_india.csv', dtype = None, delimiter = ',', skip_header = 1)
Y = [row for row in data1]

table3 = []
for row in Y:
    i = 0
    row2 = []
    for item in row:
        # item = item * x[i]
        row2.append(math.fabs(float(item)))
        i += 1
    table3.append(row2)

LIM = np.matrix(table3)
np.save('LIM', LIM)
print("\n\nDifference between the Calculated LIM and the given LIM:\n", (lim_calc - LIM).astype(int))
print("\nWe observe that the two matrices are the same\n")

#  Next we calculate the demand vector for this LIM
lim_calc_inv = np.linalg.inv(lim_calc)
demand = np.dot(lim_calc_inv,total_output)
print("\n\nDEMAND Vector:\n", demand)
# Using the calculated demand vector and the given Leontief Inverse Matrix
# we calculate the total output and show that it's the same as the one provided
# in the dataset
total_output_calc = np.dot(LIM, demand.T)
print("\n\nDifference between the Calculated Total Output and the given Total Output:\n", (total_output_calc - np.matrix(total_output).T).astype(int))
print("\nWe observe that the error margin is less than 0.06 %\n")