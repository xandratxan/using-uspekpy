# Script to compute integral quantities for a reference case using USpekPy with different number of iterations and save
# the results to CSV files for later use. It also measures the execution time of each case.
# Reference case: radiation quality N-60, operational quantity H*(10), mass energy transfer coefficients from PENELOPE,
# monoenergetic air kerma-to-dose-equivalent conversion coefficients from ISO, uncertainties 5% for all quantities.
import pandas as pd
from uspekpy import USpek
from time import time
import numpy as np

my_beam = {
    'kVp': (60, 0.05),  # mm, fraction of one
    'th': (20, 0.05),  # mm, fraction of one
    'Al': (4, 0.05),  # mm, fraction of one
    'Cu': (0.6, 0.05),  # mm, fraction of one
    'Sn': (0, 0),  # mm, fraction of one
    'Pb': (0, 0),  # mm, fraction of one
    'Be': (0, 0),  # mm, fraction of one
    'Air': (1000, 0.05)  # mm, fraction of one
}
my_mu_csv = 'data/mu_tr_rho.csv'
my_hk_csv = 'data/h_k_h_amb_10.csv'
my_mu_std = 0.05  # fraction of one

s = USpek(beam_parameters=my_beam, mass_transfer_coefficients=my_mu_csv,
          mass_transfer_coefficients_uncertainty=my_mu_std, conversion_coefficients=my_hk_csv)

iterations = [10, 20, 30, 40, 50, 60, 70, 80, 90,
              100, 200, 300, 400, 500, 600, 700, 800, 900,
              1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
              10000, 50000, 100000, 500000, 1000000]
iters = []
times = []

for n in iterations:
    print(f'Running reference case with {n} iterations')
    try:
        start_time = time()
        df = s.simulate(simulations_number=n)
        df.to_csv(f'output/out_{n}.csv', index=True)
        end_time = time()
        execution_time = end_time - start_time

        times.append(execution_time)
        print(f'Execution time: {execution_time} s for {n} iterations')
    except Exception as e:
        times.append(np.nan)
        print(f"An error occurred while running reference case with {n} iterations:\\{e}")
    iters.append(n)
    df = pd.DataFrame({'Iterations': iters, 'Execution time (s)': times})
    df.to_csv('output/execution_times_third_run.csv', index=True)
