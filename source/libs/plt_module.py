import plotly.express as px
import pandas as pd

class SampleDistributionPlotter:
    def __init__(self, data):
        self.data = data
        self.labels = data.columns

    def plot_histograms(self):
        fig = px.histogram(self.data, x=self.labels, title='Sample Distributions',
                           color_discrete_sequence=['blue', 'red'],
                           barmode="overlay",
                           labels={col: col for col in self.labels})

        fig.update_traces(showlegend=True)

        # Add axis labels
        fig.update_xaxes(title_text='Values')
        fig.update_yaxes(title_text='Frequency')

        # # Show the plot
        # fig.show()

        return fig

# Example usage:
if __name__ == "__main__":
    import numpy as np

    # Generate two sample distributions (you can replace these with your own data)
    sample1 = np.random.normal(10, 1, 1000)
    sample2 = np.random.normal(5, 1, 1000)

    df = pd.DataFrame({'col1':sample1
                     , 'col2':sample2})

    df.to_csv('template.csv')

    # Create an instance of the SampleDistributionPlotter class
    plotter = SampleDistributionPlotter(df)

    # Plot the histograms using Plotly Express
    plotter.plot_histograms()
