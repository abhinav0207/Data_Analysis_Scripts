################################################################
# Python code to plot results, can be plotted in LaTeX and EPS #
# Author: Abhinav Jha                                          #
# Email : jha.abhinav0207@gmail.com                            #
################################################################
import numpy as np
import matplotlib
import math
import matplotlib.pyplot as plt
from array import *

# Different name in the output file that seperates them
# For example we have eight output files corresponding to different processors
# and variables:
# Name of output_file : output_i_processor_j_var_k.out
# where i,j,k = 1,2

# In this example we want to plot the results for k=1
var_name = 1

# Directory where the output files are saved
dir = "../output_files/"

# Empty list to store the values
# Store for processor, j=1
# Range goes from 1 to end_value where end_value is the end of value i
filename_pro1 = []
for i in range(1,3):
    filename_next = dir+"output_"+str(i)+"_processor_1_"+str(var_name)+".out"
    filename_pro1.append(filename_next);

# Store for processor, j=2
filename_pro2 = []
for i in range(1,3):
    filename_next = dir+"output_"+str(i)+"_processor_2_"+str(var_name)+".out"
    filename_pro2.append(filename_next);

#Figure name and title
fig_name = "Plot_Results"
title_name = r"var_name_"+str(ren)

# Legend Name
legend=["Processor 1", "Processor 2"]

# Parameters Set for Plot
fontsize = 12
linewidth = 2
markersize = 8
x_label = 'x-label';
y_label = 'y-label'
# Size of plot
plt.figure(figsize=(5,4))

# List for storing values on x axis
xarray =[]
# List for storing values on y axis
yarray_pro1 = []
yarray_pro2 = []

# Loop over all the files for processor 1
for f_id in range(0,len(filename_pro1)):
    with open(filename_pro1[f_id]) as f:
        for line in f:
            # Replace the 'x_value   :' with the x values that you want to plot
            if 'x_value   :' in line:
                words = line.split()
                # words[-1] refer to the value in the end of the line. If the values
                # you desire is in the middle, replace -1 with that index
                xarray.append(float(words[-1]))
            # Replace the 'y_value :' with the y values that you want to plot
            if 'y_value :' in line:
                words = line.split()
                yarray_pro1.append(float(words[-1]))

# Loop over all the files for processor 2
# In this example we have the same x_array for both the plots
for f_id in range(0,len(filename_pro2)):
    with open(filename_pro2[f_id]) as f:
        for line in f:
            # Replace the 'y_value :' with the y values that you want to plot
            if 'y_value :' in line:
                words = line.split()
                yarray_pro2.append(float(words[-1]))

# Print Size of array to check if they are equal lengths
print(len(xarray))
print(len(yarray_pro1))
print(len(yarray_pro2))

# Setting the minimum and maximum bounds for plotting
miny = min(yarray_pro1)
miny = min(miny, min(yarray_pro2))

maxy = max(yarray_pro1)
maxy = max(maxy, max(yarray_pro2))seq))

# Plotting of Different Graphs
# Choose differnt colors, linestyle, markers, and markersize
plt.loglog(xarray, yarray_pro1, color='blue', linestyle='-.', marker='o', label = legend[0],
         linewidth=linewidth, markersize=markersize)
plt.loglog(xarray, yarray_pro2, color='red', linestyle='-.', marker='o', label = legend[1],
         linewidth=linewidth, markersize=markersize)

plt.axis([min(x_array), max(x_array), miny*0.01, maxy*1.1])

plt.xlabel(x_label,fontsize=fontsize)
plt.ylabel(y_label,fontsize=fontsize)
plt.title(title_name,fontsize=fontsize)
plt.legend(loc='lower right',fontsize=fontsize-1)
plt.tight_layout()

# Save the figure
plt.savefig(fig_name+'.eps',format='eps')
plt.show()

# Creation of LaTeX figures
f = open("LaTeX_Fig/"+str(fig_name)+".txt","w+")
f.write('\\addplot[color=black,  mark=square*, line width = 0.5mm, dashdotted,, mark options = {scale= 1.5, solid}] \n')
f.write('coordinates{')
for i in range(0, len(x_array)):
	f.write(' '.join(('(',str(x_array[i]),',',str(yarray_pro1[i]),')')))
f.write('};\n')
f.write('\\addlegendentry{Processor 1} \n')

f.write('\\addplot[color=red,  mark=oplus*, line width = 0.5mm, dashdotted,, mark options = {scale= 1.5, solid}] \n')
f.write('coordinates{')
for i in range(0, len(x_array)):
	f.write(' '.join(('(',str(x_array[i]),',',str(yarray_pro2[i]),')')))
f.write('};\n')
f.write('\\addlegendentry{Processor 2} \n')
f.close()
