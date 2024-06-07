import datetime
import pandas as pd
from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import DateRangeForm
from .utils.scraper import Scraper
from .utils.SyncDB import SyncDB
from .utils.CurrencyPlot import CurrencyPlot
from .models import Currency, Country, ExchangeRate, BaseDate

from django.views.generic import FormView


class IndexView(FormView):
    template_name = 'main/index.html'
    form_class = DateRangeForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.sync_data()
        context['countries'] = Country.objects.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        selected_country_names = self.request.POST.getlist('countries')
        begin_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        SyncDB.set_base_date(datetime.datetime(2020, 1, 1))

        selected_countries = Country.objects.filter(name__in=selected_country_names)
        currency_codes = list(selected_countries.values_list('currency__code', flat=True))

        relative_changes, selected_currencies = self.sync_currency_rates_and_relative_changes(begin_date, end_date,
                                                                                              currency_codes)
        self.render_plot(relative_changes, selected_currencies, selected_country_names, currency_codes, context)

        return render(self.request, self.template_name, context)

    def sync_data(self):
        country_currencies = Scraper.parse_country_currencies()
        unique_currency_codes = list(set([currency_code[1] for currency_code in country_currencies]))
        SyncDB.sync_currencies(unique_currency_codes)
        SyncDB.sync_countries(country_currencies)

    def sync_currency_rates_and_relative_changes(self, begin_date, end_date, currency_codes):
        currency_rates = Scraper.parse_currency_rates(begin_date, end_date, currency_codes)
        SyncDB.sync_exchange_rates(currency_rates)

        base_date = BaseDate.objects.first().date
        if not ExchangeRate.objects.filter(date=base_date).exists():
            currency_rates = Scraper.parse_currency_rates(base_date, base_date + datetime.timedelta(days=1),
                                                          currency_codes)
            SyncDB.sync_exchange_rates(currency_rates)

        selected_currencies = list(Currency.objects.filter(code__in=currency_codes))
        relative_changes = SyncDB.calculate_relative_changes(begin_date, end_date, selected_currencies)
        SyncDB.sync_relative_changes(relative_changes)

        return relative_changes, selected_currencies

    def render_plot(self, relative_changes, selected_currencies, selected_country_names, currency_codes, context):
        df_relative_changes = pd.DataFrame(relative_changes, columns=['currency', 'date', 'relative_change'])
        currency_map = {currency.id: currency.code for currency in selected_currencies}
        df_relative_changes['currency_code'] = df_relative_changes['currency'].map(currency_map)

        if not df_relative_changes.empty:
            plotter = CurrencyPlot(df_relative_changes, selected_country_names, currency_codes)
            context['plot_url'] = plotter.get_plot_url()

