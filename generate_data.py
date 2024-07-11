# Script to compute integral quantities for a reference case using USpekPy with different numbers of iterations and save
# the results to CSV files for later use. It also measures the execution time of each case.
# Reference case: radiation quality N-60, operational quantity H*(10), mass energy transfer coefficients from PENELOPE,
# mono energetic air kerma-to-dose-equivalent conversion coefficients from ISO, uncertainties 5% for all quantities.

import pandas as pd
from uspekpy import USpek
from time import time
import numpy as np

# Define the beam parameters for the reference case with uncertainties (fraction of one)
my_beam = {
    'kVp': (60, 0.05),  # Peak kilovoltage with 5% uncertainty
    'th': (20, 0.05),  # Tube current-time product with 5% uncertainty
    'Al': (4, 0.05),  # Aluminum filter thickness with 5% uncertainty
    'Cu': (0.6, 0.05),  # Copper filter thickness with 5% uncertainty
    'Sn': (0, 0),  # Tin filter thickness with no uncertainty
    'Pb': (0, 0),  # Lead filter thickness with no uncertainty
    'Be': (0, 0),  # Beryllium filter thickness with no uncertainty
    'Air': (1000, 0.05)  # Air path length with 5% uncertainty
}

# File paths for input data
my_mu_csv = 'assets/input_files/mu_tr_rho.csv'  # Mass energy transfer coefficients
my_hk_csv = 'assets/input_files/h_k_h_amb_10.csv'  # Conversion coefficients
my_mu_std = 0.05  # Uncertainty for mass energy transfer coefficients (fraction of one)

# Initialize the USpek instance with the specified parameters and input files
s = USpek(beam_parameters=my_beam, mass_transfer_coefficients=my_mu_csv,
          mass_transfer_coefficients_uncertainty=my_mu_std, conversion_coefficients=my_hk_csv)

# Define the list of iteration counts to be used in simulations
iterations = [10, 20, 30, 40, 50, 60, 70, 80, 90,
              100, 200, 300, 400, 500, 600, 700, 800, 900,
              1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
              10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000,
              100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000,
              1000000]

# Initialize lists to store iteration counts and execution times
iters = []
times = []

# Loop through each iteration count, run the simulation, and record the execution time
for n in iterations:
    print(f'Running reference case with {n} iterations')
    try:
        # Record the start time of the simulation
        start_time = time()

        # Run the simulation with the specified number of iterations
        df = s.simulate(simulations_number=n)

        # Save the simulation results to a CSV file
        df.to_csv(f'output/out_{n}.csv', index=True)

        # Record the end time of the simulation
        end_time = time()

        # Calculate the execution time
        execution_time = end_time - start_time

        # Append the execution time to the list
        times.append(execution_time)
        print(f'Execution time: {execution_time} s for {n} iterations')
    except Exception as e:
        # If an error occurs, append NaN to the times list and print the error message
        times.append(np.nan)
        print(f"An error occurred while running reference case with {n} iterations:\n{e}")

    # Append the current iteration count to the list
    iters.append(n)

    # Create a DataFrame with iteration counts and execution times
    df = pd.DataFrame({'Iterations': iters, 'Execution time (s)': times})

    # Save the execution times to a CSV file
    df.to_csv('output/execution_times.csv', index=True)