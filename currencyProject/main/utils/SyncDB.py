import pandas as pd
from datetime import datetime, date, timedelta
from ..models import Currency, ExchangeRate, Country, RelativeChange, BaseDate
from decimal import Decimal


class SyncDB:
    @staticmethod
    def sync_currencies(currency_codes):
        currency_codes_obj = [
            Currency(code=cur_code)
            for cur_code in currency_codes
            if cur_code
        ]
        with Currency.objects.bulk_update_or_create_context(
                match_field=['code'], update_fields=['code']
        ) as bulkit:
            for obj in currency_codes_obj:
                bulkit.queue(obj)

    @staticmethod
    def sync_countries(country_data):
        name, currency_code = 0, 1
        country_objs = [
            Country(
                name=data[name],
                currency=Currency.objects.get(code=data[currency_code])
            )
            for data in country_data
            if Currency.objects.filter(code=data[currency_code]).exists()  # Фильтрация несуществующих валют
        ]

        with Country.objects.bulk_update_or_create_context(
                match_field=['name'], update_fields=['currency']
        ) as bulkit:
            for obj in country_objs:
                bulkit.queue(obj)

    @staticmethod
    def sync_exchange_rates(exchange_rate_data: list[list[str, str, str]]):
        _currency_code = 0
        _date = 1
        _rate = 2
        exchange_rate_objs = [
            ExchangeRate(
                currency=Currency.objects.get(code=cur_data[_currency_code]),
                date=datetime.strptime(cur_data[_date], '%d.%m.%Y').date(),
                rate=Decimal(cur_data[_rate].replace(',', '.'))
            )
            for cur_data in exchange_rate_data
            if Currency.objects.filter(code=cur_data[_currency_code]).exists()
        ]

        with ExchangeRate.objects.bulk_update_or_create_context(
                match_field=['currency', 'date'], update_fields=['rate']
        ) as bulkit:
            for obj in exchange_rate_objs:
                bulkit.queue(obj)

    @staticmethod
    def set_base_date(base_date: datetime):
        if base_date:
            BaseDate.objects.update_or_create(
                date=base_date,
                defaults={
                    'date': base_date
                }
            )

    @staticmethod
    def calculate_relative_changes(begin_date: datetime.date, end_date: datetime.date,
                                   currencies: list[Currency]) -> pd.DataFrame:
        base_date = BaseDate.objects.first().date

        exchange_rates = ExchangeRate.objects.filter(
            currency__in=currencies,
            date__range=[begin_date, end_date]
        ).values('currency', 'date', 'rate')

        df_rates = pd.DataFrame(list(exchange_rates))
        df_rates['date'] = pd.to_datetime(df_rates['date'])

        base_rates = ExchangeRate.objects.filter(
            currency__in=currencies,
            date=base_date
        ).values('currency', 'rate')

        df_base_rates = pd.DataFrame(list(base_rates))
        df_base_rates.rename(columns={'rate': 'base_rate'}, inplace=True)

        df_merged = pd.merge(df_rates, df_base_rates, on='currency', how='left')

        df_merged['relative_change'] = (df_merged['rate'] - df_merged['base_rate']) / df_merged['base_rate'] * 100

        return df_merged[['currency', 'date', 'relative_change']]

    @staticmethod
    def sync_relative_changes(df_relative_changes):
        relative_change_objs = [
            RelativeChange(
                currency=Currency.objects.get(id=row['currency']),
                date=row['date'].date(),
                relative_change=row['relative_change']
            )
            for index, row in df_relative_changes.iterrows()
        ]

        with RelativeChange.objects.bulk_update_or_create_context(
                match_field=['currency', 'date'], update_fields=['relative_change']
        ) as bulkit:
            for obj in relative_change_objs:
                bulkit.queue(obj)
