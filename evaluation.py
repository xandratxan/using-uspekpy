# Import necessary libraries
import os
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Define paths for data set and figures
data_set_path = 'assets/data_set/'
figures_path = 'assets/figures/'


def plot_histograms(n):
    # Read the CSV file for the given number of iterations
    df = pd.read_csv(data_set_path + f'out_{n}.csv', index_col=0)
    iterations = df.loc[0:n - 1]

    # Print min and max filter thickness for Al and Cu
    print(f'{n} iterations: min and max filter thickness (mm):')
    print(f'Al: ({iterations["Al (mm)"].min():.2f}, {iterations["Al (mm)"].max():.2f})')
    print(f'Cu: ({iterations["Cu (mm)"].min():.2f}, {iterations["Cu (mm)"].max():.2f})')

    # Create subplots for histograms
    fig, axs = plt.subplots(3, 4, figsize=(12.8, 9.6))

    # Plot histograms for various parameters
    axs[0, 0].hist(iterations['kVp (kV)'])
    axs[0, 1].hist(iterations['th (deg)'])
    axs[0, 2].hist(iterations['Air (mm)'])
    axs[0, 3].hist(iterations['Al (mm)'])
    axs[1, 0].hist(iterations['Cu (mm)'])
    axs[1, 1].hist(iterations['HVL1 Al (mm)'])
    axs[1, 2].hist(iterations['HVL2 Al (mm)'])
    axs[1, 3].hist(iterations['HVL1 Cu (mm)'])
    axs[2, 0].hist(iterations['HVL2 Cu (mm)'])
    axs[2, 1].hist(iterations['Mean energy (keV)'])
    axs[2, 2].hist(iterations['Air kerma (uGy)'])
    axs[2, 3].hist(iterations['Mean conv. coeff. (Sv/Gy)'])

    # Set labels for each subplot
    axs[0, 0].set_xlabel('kVp (kV)')
    axs[0, 1].set_xlabel('th (deg)')
    axs[0, 2].set_xlabel('Air (mm)')
    axs[0, 3].set_xlabel('Al (mm)')
    axs[1, 0].set_xlabel('Cu (mm)')
    axs[1, 1].set_xlabel('HVL1 Al (mm)')
    axs[1, 2].set_xlabel('HVL2 Al (mm)')
    axs[1, 3].set_xlabel('HVL1 Cu (mm)')
    axs[2, 0].set_xlabel('HVL2 Cu (mm)')
    axs[2, 1].set_xlabel('Mean energy (keV)')
    axs[2, 2].set_xlabel('Air kerma (uGy)')
    axs[2, 3].set_xlabel('Mean conv. coeff. (Sv/Gy)')

    # Set the title for the entire figure
    plt.suptitle(f'Reference case with {n} iterations')

    # Save the figure to a file and close it
    plt.savefig(figures_path + f'histogram_{n}.png')
    plt.close()
    return


def plot_execution_time(iterations, times, suffix, log=False):
    # Convert times to minutes
    t_m = times / 60

    # Fit a straight line to the data
    coefficients = np.polyfit(iterations, t_m, 1)
    slope, intercept = coefficients
    y_fit = slope * iterations + intercept  # Calculate the fitted y values

    # Equation of the fitted line
    equation_text = f't (min) = {slope:.2f}n + {intercept:.2f}'

    # Plot the original data and the fitted line
    plt.scatter(iterations, t_m, label='Data')
    plt.plot(iterations, y_fit, label='Fit')
    plt.xlabel('Number of iterations')
    plt.ylabel('Execution time (min)')
    plt.legend()
    plt.text(0.05, 0.95, equation_text, transform=plt.gca().transAxes)

    # Apply log scale if specified
    if log:
        plt.xscale('log')
        plt.savefig(figures_path + f'execution_time_log.png')
    else:
        plt.savefig(figures_path + f'execution_time.png')

    # Close the plot
    plt.close()
    return


def plot_values_and_uncertainties(iterations, log=False):
    means = []
    relative_uncertainties = []

    # Read mean values and uncertainties for each iteration
    for n in iterations:
        df = pd.read_csv(data_set_path + f'out_{n}.csv', index_col=0)
        df = df.set_index('#')
        means.append(df.loc['Mean', :])
        relative_uncertainties.append(df.loc['Relative uncertainty', :])

    # Convert lists to DataFrames
    means = pd.DataFrame(dict(zip(iterations, means))).T
    fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(19.2, 14.4))

    # Plot mean values for various parameters
    means['kVp (kV)'].plot(ax=axs[0, 0], title='kVp (kV)', marker='o', logx=log)
    means['th (deg)'].plot(ax=axs[0, 1], title='th (deg)', marker='o', logx=log)
    means['Air (mm)'].plot(ax=axs[0, 2], title='Air (mm)', marker='o', logx=log)
    means['Al (mm)'].plot(ax=axs[0, 3], title='Al (mm)', marker='o', logx=log)
    means['Cu (mm)'].plot(ax=axs[1, 0], title='Cu (mm)', marker='o', logx=log)
    means['HVL1 Al (mm)'].plot(ax=axs[1, 1], title='HVL1 Al (mm)', marker='o', logx=log)
    means['HVL2 Al (mm)'].plot(ax=axs[1, 2], title='HVL2 Al (mm)', marker='o', logx=log)
    means['HVL1 Cu (mm)'].plot(ax=axs[1, 3], title='HVL1 Cu (mm)', marker='o', logx=log)
    means['HVL2 Cu (mm)'].plot(ax=axs[2, 0], title='HVL2 Cu (mm)', marker='o', logx=log)
    means['Mean energy (keV)'].plot(ax=axs[2, 1], title='Mean energy (keV)', marker='o', logx=log)
    means['Air kerma (uGy)'].plot(ax=axs[2, 2], title='Air kerma (uGy)', marker='o', logx=log)
    means['Mean conv. coeff. (Sv/Gy)'].plot(ax=axs[2, 3], title='Mean conv. coeff. (Sv/Gy)', marker='o', logx=log)

    # Save the plot with log scale if specified
    if log:
        plt.savefig(figures_path + f'mean_values_log.png')
    else:
        plt.savefig(figures_path + f'mean_values.png')
    plt.close()

    # Convert lists to DataFrames for relative uncertainties
    relative_uncertainties = pd.DataFrame(dict(zip(iterations, relative_uncertainties))).T
    fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(19.2, 14.4))

    # Plot relative uncertainties for various parameters
    relative_uncertainties['kVp (kV)'].plot(ax=axs[0, 0], title='kVp (kV)', marker='o', logx=log)
    relative_uncertainties['th (deg)'].plot(ax=axs[0, 1], title='th (deg)', marker='o', logx=log)
    relative_uncertainties['Air (mm)'].plot(ax=axs[0, 2], title='Air (mm)', marker='o', logx=log)
    relative_uncertainties['Al (mm)'].plot(ax=axs[0, 3], title='Al (mm)', marker='o', logx=log)
    relative_uncertainties['Cu (mm)'].plot(ax=axs[1, 0], title='Cu (mm)', marker='o', logx=log)
    relative_uncertainties['HVL1 Al (mm)'].plot(ax=axs[1, 1], title='HVL1 Al (mm)', marker='o', logx=log)
    relative_uncertainties['HVL2 Al (mm)'].plot(ax=axs[1, 2], title='HVL2 Al (mm)', marker='o', logx=log)
    relative_uncertainties['HVL1 Cu (mm)'].plot(ax=axs[1, 3], title='HVL1 Cu (mm)', marker='o', logx=log)
    relative_uncertainties['HVL2 Cu (mm)'].plot(ax=axs[2, 0], title='HVL2 Cu (mm)', marker='o', logx=log)
    relative_uncertainties['Mean energy (keV)'].plot(ax=axs[2, 1], title='Mean energy (keV)', marker='o', logx=log)
    relative_uncertainties['Air kerma (uGy)'].plot(ax=axs[2, 2], title='Air kerma (uGy)', marker='o', logx=log)
    relative_uncertainties['Mean conv. coeff. (Sv/Gy)'].plot(ax=axs[2, 3], title='Mean conv. coeff. (Sv/Gy)',
                                                             marker='o', logx=log)

    # Save the plot with log scale if specified
    if log:
        plt.xscale('log')
        plt.savefig(figures_path + f'relative_uncertainties_log.png')
    else:
        plt.savefig(figures_path + f'relative_uncertainties.png')
    plt.close()
    return


def extract_numbers_from_filenames(directory):
    # List all files in the given directory
    files = os.listdir(directory)

    # Define the regular expression pattern to match 'out_<number>.csv'
    pattern = re.compile(r'^out_(\d+)\.csv$')

    # List to store the extracted numbers
    numbers = []

    # Iterate over the files and apply the regex pattern
    for file in files:
        match = pattern.match(file)
        if match:
            # Extract the number and add it to the list
            numbers.append(int(match.group(1)))

    # Sort the numbers in ascending order
    numbers.sort()

    return numbers


def main():
    # Retrieve iteration numbers from output files
    print('Retrieve iterations from output files.')
    iterations = extract_numbers_from_filenames(data_set_path)
    print(f'Retrieved {len(iterations)} cases with iteration numbers: {iterations}.')
    print()

    # Plot histograms for input and output variables
    print('Plot probability distribution of input and output variables.')
    for i in iterations:
        plot_histograms(n=i)
    print()

    # Plot execution time against the number of iterations
    print('Plot execution time of one case in terms of the iteration number.')
    df = pd.read_csv('assets/data_set/execution_times.csv', index_col=0)
    plot_execution_time(df['Iterations'], df['Execution time (s)'], '_third_run')
    plot_execution_time(df['Iterations'], df['Execution time (s)'], '_third_run', log=True)
    print()

    # Plot mean values and uncertainties of input and output variables
    print('Plot mean values and uncertainties of input and output variables in terms of the iteration number.')
    plot_values_and_uncertainties(iterations)
    plot_values_and_uncertainties(iterations, log=True)


# Run the main function if the script is executed
if __name__ == "__main__":
    main()
