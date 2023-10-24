import numpy as np
from scipy import stats
import pandas as pd

class StatisticalTests:
    def __init__(self, data):
        self.A = data.iloc[: ,0]
        self.B = data.iloc[: ,1]

    def independent_t_test(self, alpha=0.05):
        """
        Perform an independent t-test.

        Args:
            alpha (float): Significance level (default is 0.05).

        Returns:
            (t_statistic, p_value): Tuple containing the t-statistic and p-value.
        """
        t_statistic, p_value = stats.ttest_ind(self.A, self.B)
        return t_statistic, p_value

    def z_test(self, population_mean, alpha=0.05):
        """
        Perform a one-sample z-test.

        Args:
            population_mean (float): The population mean for comparison.
            alpha (float): Significance level (default is 0.05).

        Returns:
            (z_statistic, p_value): Tuple containing the z-statistic and p-value.
        """
        sample_mean = np.mean(self.A)
        sample_std = np.std(self.A, ddof=1)  # ddof=1 for unbiased sample standard deviation
        sample_size = len(self.A)

        z_statistic = (sample_mean - population_mean) / (sample_std / np.sqrt(sample_size))
        p_value = 2 * (1 - stats.norm.cdf(abs(z_statistic)))  # Two-tailed test

        return z_statistic, p_value

    def confidence_interval_difference(self, alpha=0.05):
        """
        Calculate the difference in confidence intervals for means of two samples.

        Args:
            alpha (float): Significance level (default is 0.05).

        Returns:
            (lower_diff, upper_diff): Tuple containing the lower and upper bounds of the difference
            in confidence intervals.
        """
        n1 = len(self.A)
        n2 = len(self.B)

        mean1 = np.mean(self.A)
        mean2 = np.mean(self.B)

        std1 = np.std(self.A, ddof=1)  # ddof=1 for unbiased sample standard deviation
        std2 = np.std(self.B, ddof=1)

        se = np.sqrt((std1 ** 2 / n1) + (std2 ** 2 / n2))
        margin_of_error = stats.norm.ppf(1 - alpha / 2) * se

        lower_diff = (mean1 - mean2) - margin_of_error
        upper_diff = (mean1 - mean2) + margin_of_error

        return lower_diff, upper_diff

    # def shapiro_wilk_test(self):
    #     """
    #     Perform the Shapiro-Wilk test for normality on the data.
    #
    #     Returns:
    #         (statistic, p_value): Tuple containing the test statistic and p-value.
    #     """
    #     _, p_value1 = stats.shapiro(self.A)
    #     if self.B:
    #         _, p_value2 = stats.shapiro(self.B)
    #         return p_value1, p_value2
    #     return p_value1

    # Function for the Mann-Whitney U test
    def perform_mannwhitneyu(self):
        u_stat, p_value = stats.mannwhitneyu(self.A, self.B)
        return u_stat, p_value

    def interpret_pvalue(self,p_value):
        if p_value < 0.01:
            return 'Highly Significant'
        elif p_value < 0.05:
            return 'Significant'
        else:
            return 'Not Significant'

# Example usage:
if __name__ == '__main__':
    # df = pd.DataFrame({'col1':[12, 15, 17, 18, 21, 22, 25, 30, 32, 35]
    #                  , 'col2':[10, 14, 19, 21, 23, 26, 28, 31, 36, 37]})

    sample1 = np.random.normal(10, 1, 1000)
    sample2 = np.random.normal(5, 1, 1000)

    df = pd.DataFrame({'col1':sample1
                     , 'col2':sample2})

    test = StatisticalTests(df)

    t_statistic, t_p_value = test.independent_t_test()
    print(f"Independent T-Test: t-statistic = {t_statistic}, p-value = {t_p_value}")

    z_statistic, z_p_value = test.z_test(population_mean=20)
    print(f"One-Sample Z-Test: z-statistic = {z_statistic}, p-value = {z_p_value}")

    lower_diff, upper_diff = test.confidence_interval_difference()
    print(f"Difference in Confidence Intervals: Lower = {lower_diff}, Upper = {upper_diff}")

    # shapiro_p_values = test.shapiro_wilk_test()
    # print(f"Shapiro-Wilk p-values for data1: {shapiro_p_values[0]}")