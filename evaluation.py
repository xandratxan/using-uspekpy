import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_histograms(n):
    df = pd.read_csv(f'output/out_{n}.csv', index_col=0)
    iterations = df.loc[0:n - 1]
    print(f'Minimum and maximum filter thickness (mm):')
    print(f'Al: ({iterations['Al (mm)'].min():.2f}, {iterations['Al (mm)'].max():.2f})')
    print(f'Cu: ({iterations['Cu (mm)'].min():.2f}, {iterations['Cu (mm)'].max():.2f})')

    fig, axs = plt.subplots(3, 4, figsize=(12.8, 9.6))
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
    plt.suptitle(f'Reference case with {n} iterations')
    plt.savefig(f'output/histogram_{n}.png')
    plt.close()
    return


def plot_execution_time(iterations, times, suffix):
    t_m = times / 60
    # Fit a straight line to the data
    coefficients = np.polyfit(iterations, t_m, 1)
    slope, intercept = coefficients
    # Calculate the fitted y values
    y_fit = slope * iterations + intercept
    # Equation of the fitted line
    equation_text = f't (min) = {slope:.2f}n + {intercept:.2f}'
    # Plot the original data, the fitted line and the fitted equation
    plt.scatter(iterations, t_m, label='Data')
    plt.plot(iterations, y_fit, label='Fit')
    plt.xlabel('Number of iterations')
    plt.ylabel('Execution time (min)')
    # plt.xscale('log')
    plt.legend()
    plt.text(0.05, 0.95, equation_text, transform=plt.gca().transAxes)
    # plt.show()
    plt.savefig(f'output/execution_time{suffix}.png')
    plt.close()
    return


def plot_values_and_uncertainties(iterations):
    means = []
    relative_uncertainties = []
    for n in iterations:
        df = pd.read_csv(f'output/out_{n}.csv', index_col=0)
        df = df.set_index('#')
        means.append(df.loc['Mean', :])
        relative_uncertainties.append(df.loc['Relative uncertainty', :])

    means = pd.DataFrame(dict(zip(iterations, means)))
    means = means.T
    fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(19.2, 14.4))
    means['kVp (kV)'].plot(ax=axs[0, 0], title='kVp (kV)', marker='o')
    means['th (deg)'].plot(ax=axs[0, 1], title='th (deg)', marker='o')
    means['Air (mm)'].plot(ax=axs[0, 2], title='Air (mm)', marker='o')
    means['Al (mm)'].plot(ax=axs[0, 3], title='Al (mm)', marker='o')
    means['Cu (mm)'].plot(ax=axs[1, 0], title='Cu (mm)', marker='o')
    means['HVL1 Al (mm)'].plot(ax=axs[1, 1], title='HVL1 Al (mm)', marker='o')
    means['HVL2 Al (mm)'].plot(ax=axs[1, 2], title='HVL2 Al (mm)', marker='o')
    means['HVL1 Cu (mm)'].plot(ax=axs[1, 3], title='HVL1 Cu (mm)', marker='o')
    means['HVL2 Cu (mm)'].plot(ax=axs[2, 0], title='HVL2 Cu (mm)', marker='o')
    means['Mean energy (keV)'].plot(ax=axs[2, 1], title='Mean energy (keV)', marker='o')
    means['Air kerma (uGy)'].plot(ax=axs[2, 2], title='Air kerma (uGy)', marker='o')
    means['Mean conv. coeff. (Sv/Gy)'].plot(ax=axs[2, 3], title='Mean conv. coeff. (Sv/Gy)', marker='o')
    plt.suptitle(f'Mean values of input and output variables in terms of the number of iterations')
    # plt.show()
    plt.savefig(f'output/mean_values.png')
    plt.close()

    relative_uncertainties = pd.DataFrame(dict(zip(iterations, relative_uncertainties)))
    relative_uncertainties = relative_uncertainties.T
    fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(19.2, 14.4))
    relative_uncertainties['kVp (kV)'].plot(ax=axs[0, 0], title='kVp (kV)', marker='o')
    relative_uncertainties['th (deg)'].plot(ax=axs[0, 1], title='th (deg)', marker='o')
    relative_uncertainties['Air (mm)'].plot(ax=axs[0, 2], title='Air (mm)', marker='o')
    relative_uncertainties['Al (mm)'].plot(ax=axs[0, 3], title='Al (mm)', marker='o')
    relative_uncertainties['Cu (mm)'].plot(ax=axs[1, 0], title='Cu (mm)', marker='o')
    relative_uncertainties['HVL1 Al (mm)'].plot(ax=axs[1, 1], title='HVL1 Al (mm)', marker='o')
    relative_uncertainties['HVL2 Al (mm)'].plot(ax=axs[1, 2], title='HVL2 Al (mm)', marker='o')
    relative_uncertainties['HVL1 Cu (mm)'].plot(ax=axs[1, 3], title='HVL1 Cu (mm)', marker='o')
    relative_uncertainties['HVL2 Cu (mm)'].plot(ax=axs[2, 0], title='HVL2 Cu (mm)', marker='o')
    relative_uncertainties['Mean energy (keV)'].plot(ax=axs[2, 1], title='Mean energy (keV)', marker='o')
    relative_uncertainties['Air kerma (uGy)'].plot(ax=axs[2, 2], title='Air kerma (uGy)', marker='o')
    relative_uncertainties['Mean conv. coeff. (Sv/Gy)'].plot(ax=axs[2, 3], title='Mean conv. coeff. (Sv/Gy)',
                                                             marker='o')
    plt.suptitle(f'Relative uncertainty of input and output variables in terms of the number of iterations')
    # plt.show()
    plt.savefig(f'output/relative_uncertainties.png')
    plt.close()
    return


if __name__ == "__main__":
    iterations = [10, 50, 100, 500, 1000, 5000]

    # Probability distribution of input and output variables
    for i in iterations:
        plot_histograms(n=i)

    # Execution time
    # iterations = np.array([10, 50, 100, 500, 1000])
    # times = np.array([7.773966312408447, 38.55954885482788, 81.8867039680481, 412.0777871608734, 953.7109704017639])
    # suffix = '_first_run'
    times = np.array([8.112820148468018, 38.74364185333252, 74.59362983703613, 371.9314422607422, 1380.4966669082642,
                      8006.918867588043])
    suffix = '_second_run'
    plot_execution_time(np.array(iterations), times, suffix)

    # Quantities mean values
    plot_values_and_uncertainties(iterations)
