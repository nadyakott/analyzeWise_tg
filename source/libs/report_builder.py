import datapane as dp
import pandas as pd
import numpy as np
import logging

from libs.plt_module import SampleDistributionPlotter
from libs.statistics import StatisticalTests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ReportBuilder():

    def __init__(self, data=None):
        self.data = data

    def draw_graph(self, file_name: str):

        plot_page1 = SampleDistributionPlotter(self.data)
        test = StatisticalTests(self.data)

        t_statistic, t_p_value = test.independent_t_test()
        print(f"Independent T-Test: t-statistic = {t_statistic}, p-value = {t_p_value}")

        z_statistic, z_p_value = test.z_test(population_mean=20)
        print(f"One-Sample Z-Test: z-statistic = {z_statistic}, p-value = {z_p_value}")

        lower_diff, upper_diff = test.confidence_interval_difference()
        print(f"Difference in Confidence Intervals: Lower = {lower_diff}, Upper = {upper_diff}")

        # shapiro_p_values = test.shapiro_wilk_test()
        u_stat, p_value = test.perform_mannwhitneyu()

        logger.info('test GOOD')

        # Getting results
        results = [
            ('T-test',t_statistic, t_p_value),
            ('One-Sample Z-Test',z_statistic, z_p_value),
            ('Mann-Whitney U',u_stat, p_value),
        ]

        # Creating a summary table
        summary = pd.DataFrame(results, columns=['Test', 'Statistic', 'P-value'])

        summary['Interpretation'] = summary['P-value'].apply(test.interpret_pvalue)

        logger.info('summary GOOD')

        datapane_app = dp.App(
            dp.Page(
                dp.Text('# Stats and distribution'),
                dp.Text('### Raw data'),
                dp.DataTable(self.data),
                dp.Text('### Difference in Confidence Intervals'),
                dp.Group(
                    dp.BigNumber(heading="Lower", value=np.round(lower_diff,2)),
                    dp.BigNumber(heading="Upper", value=np.round(upper_diff,2)),
                    columns=2),
                dp.Text('### Histogram'),
                dp.Plot(plot_page1.plot_histograms()),
                # dp.Text(f'### Difference in Confidence Intervals: Lower = {lower_diff}, Upper = {upper_diff}'),
                dp.Text('### Stat tests results'),
                dp.DataTable(summary),
                title='Stats'
            )
            # dp.Page(
            #     dp.Text('Statistical tests'),
            #     dp.Table(summary),
            #     title='Page2',
            # )
        )

        logger.info('dp GOOD')

        datapane_app.save(file_name)

        logger.info('dp saved')


        return file_name, datapane_app.save(file_name)

    pass