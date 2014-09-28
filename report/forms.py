from django import forms
from django.forms.extras.widgets import SelectDateWidget
from delivery.models import Product, Request
import datetime
import re

from django.forms.widgets import Widget, Select
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe


__all__ = ('MonthYearWidget',)

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')

class MonthYearWidget(Widget):
    """
    A Widget that splits date input into two <select> boxes for month and year,
    with 'day' defaulting to the first of the month.
    
    Based on SelectDateWidget, in 
    
    django/trunk/django/forms/extras/widgets.py
    
    
    """
    none_value = (0, '---')
    month_field = '%s_month'
    year_field = '%s_year'

    def __init__(self, attrs=None, years=None, required=True):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}
        self.required = required
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year+10)

    def render(self, name, value, attrs=None):
        try:
            year_val, month_val = value.year, value.month
        except AttributeError:
            year_val = month_val = None
            if isinstance(value, basestring):
                match = RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val = [int(v) for v in match.groups()]

        output = []

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        month_choices = MONTHS.items()
        if not (self.required and value):
            month_choices.append(self.none_value)
        month_choices.sort()
        local_attrs = self.build_attrs(id=self.month_field % id_)
        s = Select(choices=month_choices)
        select_html = s.render(self.month_field % name, month_val, local_attrs)
        output.append(select_html)

        year_choices = [(i, i) for i in self.years]
        if not (self.required and value):
            year_choices.insert(0, self.none_value)
        local_attrs['id'] = self.year_field % id_
        s = Select(choices=year_choices)
        select_html = s.render(self.year_field % name, year_val, local_attrs)
        output.append(select_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_month' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        if y == m == "0":
            return None
        if y and m:
            return '%s-%s-%s' % (y, m, 1)
        return data.get(name, None)

class StatForm(forms.Form):
	STAT_CHOICES = (('TV','Total de Ventas'),('P','Por producto'))
	kind = forms.CharField(max_length=2,initial='P',help_text='Tipo de reporte',widget=forms.Select(attrs={"onchange":'Hide()'},choices=STAT_CHOICES))
	product = forms.ModelChoiceField(help_text='Producto a consultar', queryset=Product.objects.all(),initial=0)
	start_date = forms.DateField(help_text='Desde el 1 de esta fecha', widget=MonthYearWidget())
	end_date = forms.DateField(help_text='Hasta un dia anterior al 1 de esta fecha', widget=MonthYearWidget())

	def clean(self):
		cleaned_data = self.cleaned_data
		start_date = cleaned_data.get('start_date')
		end_date = cleaned_data.get('end_date')

		if end_date <= start_date:
			msg = u"End date should be greater than start date."
			self._errors["end_date"] = self.error_class([msg])

		return self.cleaned_data