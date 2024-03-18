######################################################################
# Python code to run an input file by changing some parameters of it #
# Author: Abhinav Jha                                                #
# Email : jha.abhinav0207@gmail.com                                  #
######################################################################

##################################################################################################
# To run the code                                                                                #
# python3 run_mutiple_tests.py -e executable -i input_file -val1 value_1 -val2 value_2           #
# NOTE: If you want to run the code with multiple values of variable 1 (value _1) use            #
# python3 run_mutiple_tests.py -e executable -i input_file -val1 value_11 value_12 -val2 value_2 #
# Read below to understand what all the above things mean                                        #
##################################################################################################
import os
import argparse
import datetime
import shutil

# Insert new_value in variable_name in the file file_name
# For example: File name is input.txt and you want to assign the variable
#              'print_console' to 'false'.
# INPUT:
# file_name     : Name of input file
# variable_name : The option that needs to be assigned
# new_value     : The value that is assigned
def update_option_in_input_file(file_name, variable_name, new_value):
    import fileinput
    #inplace checks of such an option exists or not
    with fileinput.input(file_name, inplace=True) as f:
        for line in f:
            if(line.startswith(variable_name)):
                line = "{}: {}".format(variable_name, new_value)
            print(line.rstrip())

# Send all the options that needs to be updated
# INPUT:
# value_1 : Value that needs to be assigned to variable_name_1
# value_2 : Value that needs to be assigned to variable_name_2
def update_input_file(value_1, value_2):
    update_option_in_input_file(input_file, "variable_name_1", value_1)
    update_option_in_input_file(input_file, "variable_name_2", value_2)


# Run the program
# INPUT:
# exe        : Executable
# input_file : Input file
# outfile    : Output file
def run_program(exe, input_file, outfile):
    print("\nRunning {}. Input file: {}. Outfile: {}".format(exe, input_file, outfile))
    # Save the console output
    sytem_call = "./{} {} > {} 2>&1".format(exe, input_file, outfile + "console.out")
    start = datetime.datetime.now()
    os.system(sytem_call)
    print(sytem_call)
    end = datetime.datetime.now()
    # Time taken to run the program
    return (end-start).total_seconds()

# Check if the executable exists or not
# INPUT:
# exe : Name of the executable
def check_executable(exe):
    # If executable exists
    if not os.path.isfile(exe):
        print("Could not find the executable")
        exit(1)
    # If executable can be accessed
    if not os.access(exe, os.X_OK):
        print("Given executable is not executable")
        exit(1)


# Make a seperate directory for all the outputs
# INPUT:
# dir : Name of directory
def make_directory(dir):
    # Check if directories exist and if not create it
    if not os.path.exists(dir):
        os.makedirs(dir)
    else:
        print("A directory {} already exists!".format(dir))
        exit(0)

# Main Function
if __name__ == '__main__':
    # Name of and path to the executable from command line options
    parser = argparse.ArgumentParser(
        description='Run a program with a varying number of MPI processes.')
    parser.add_argument('-e', '--executable',
                        help='the Executable to be run', required=True)
    parser.add_argument('-i', '--input_file',
                        help='an input file for the program',
                        required=True)
    parser.add_argument('-val1', '--value_1',
                        help='Value_1', nargs='+',
                        required=True)
    parser.add_argument('-val2', '--value_2',
                        help='Value_2', nargs='+',
                        type=int, required=True)

    args = parser.parse_args()
    print("Running the Executable {} with the Input file {}, with Value_1 {},"
          " Valuw_2 {}."
          .format(args.executable, args.input_file, args.value_1, args.value_2))

    check_executable(args.executable)

    # The date used for unique naming
    date = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    # Name of a directory where all output of this script goes
    computation_dir = "computation_{}".format(date)
    # Create this directory
    make_directory(computation_dir)
    # Copy the input file, so it is not changed at all, we work with the copy
    input_file = "{}/base_input_file.dat".format(computation_dir)
    exe = "{}/executable".format(computation_dir)
    shutil.copy(args.input_file, input_file)
    shutil.copy(args.executable, exe)

    results = []
    # Loop over all the values for variable 1
    for value_1 in args.value_1:
        for value_2 in args.value_2:
           # Change the input file according to the given values
           update_input_file(value_1, value_2)
           output_file = "{}/Code_with_value1_{}_value2_{}.out".format(computation_dir, value_1, value_2)
           update_option_in_input_file(input_file, "outfile", output_file)
           # Run the program and store the computational times together with an
           # appropriate name in 'results'
           computational_time = run_program(exe, input_file, output_file)
           results.append([value_1, value_2])

    print("Done with the computations.")
    print(results)
    # Print the summary also to a file
    with open('{}/summary.txt'.format(computation_dir), 'w') as text_file:
        import sys
        print("# Summary from call '{}'".format(' '.join(sys.argv)),
              file=text_file)
        print("data = {}".format(results), file=text_file)

    print(">>>>>> Exiting the run script.")
