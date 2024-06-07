from django import forms
from datetime import date, timedelta


class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        label='с',
        widget=forms.SelectDateWidget(years=range(1992, date.today().year + 1))
    )
    end_date = forms.DateField(
        label='по',
        widget=forms.SelectDateWidget(years=range(1992, date.today().year + 1))
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            max_date_range = timedelta(days=2 * 365 + 1)
            if end_date < start_date:
                raise forms.ValidationError('Дата окончания не может быть раньше даты начала.')
            if end_date - start_date > max_date_range:
                raise forms.ValidationError('Диапазон дат не может превышать 2 года.')

        return cleaned_data
