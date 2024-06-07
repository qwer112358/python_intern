import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64


class CurrencyPlot:
    def __init__(self, df, country_names, currency_codes):
        self.df = df
        self.country_names = country_names
        self.currency_codes = currency_codes
        self.plot_url = None

    def preprocess_data(self):
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df = self.df.drop_duplicates()

    def plot_relative_change(self, ax):
        color = 'tab:red'
        ax.set_xlabel('Дата')
        ax.set_ylabel('Относительное изменение (%)', color=color)

        [ax.plot(self.df[self.df['currency_code'] == currency_code]['date'],
                 self.df[self.df['currency_code'] == currency_code]['relative_change'],
                 label=f'{currency_code} Change')
         for currency_code in self.currency_codes]

        ax.tick_params(axis='y', labelcolor=color)
        ax.legend(loc='upper right')
        ax.grid(True)

    def create_plot(self):
        fig, ax = plt.subplots(figsize=(13, 7))
        self.plot_relative_change(ax)

        plt.title('Относительное изменение валюты')

        fig.tight_layout()
        return fig

    def save_plot_to_buffer(self, fig):
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        self.plot_url = self._encode_image_to_base64(buf)
        plt.close(fig)

    @staticmethod
    def _encode_image_to_base64(buf):
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        return f'data:image/png;base64,{image_base64}'

    def get_plot_url(self):
        self.preprocess_data()
        fig = self.create_plot()
        self.save_plot_to_buffer(fig)
        return self.plot_url
