from django.shortcuts import render, render_to_response
from delivery.models import Request
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from report.forms import StatForm
from django import forms
from datetime import datetime, timedelta, date
import calendar
import json

def add_months(sourcedate,months):
     month = sourcedate.month - 1 + months
     year = sourcedate.year + month / 12
     month = month % 12 + 1
     day = min(sourcedate.day,calendar.monthrange(year,month)[1])
     return date(year,month,day)

# Create your views here.
def stats(request):
	context = RequestContext(request)
	if request.method == 'POST':
		form = StatForm(data=request.POST)
		if form.is_valid():
			kind = form.cleaned_data['kind']
			start_date = form.cleaned_data['start_date']
			end_date = form.cleaned_data['end_date']
			product = form.cleaned_data['product']
			delta =  end_date - start_date
			if kind == 'TV':
				values = []
				months = []
				query = Request.objects.filter(pur_date__range=(start_date, end_date))
				total_sold = 0
				actual = start_date
				while actual < end_date:
					for sold in query.filter(pur_date__range=(actual, add_months(actual,1)-timedelta(days=1))):
						total_sold += sold.total
					values.append(total_sold)
					months.append(calendar.month_name[actual.month])
					actual = add_months(actual, 1)
					total_sold = 0
				lens = []
				months = json.dumps(months)
				for i in range(len(values)):
					lens.append(i)
				form = StatForm()
				return render_to_response('report.html',{'form':form, 'kind': kind, 'total': total_sold,
										 'vals': values, 'len': lens, 'months': months},
										  context)
				
			if kind == 'P':
				values = []
				months = []
				total_sold = 0
				query = Request.objects.filter(pur_date__range=(start_date, end_date),products=product)
				actual = start_date
				while actual < end_date:
					for sold in query.filter(pur_date__range=(actual, add_months(actual,1)-timedelta(days=1))):
						total_sold += 1
					values.append(total_sold)
					months.append(calendar.month_name[actual.month])
					actual = add_months(actual, 1)
					total_sold = 0
				months = json.dumps(months)
				lens = []
				for i in range(len(values)):
					lens.append(i)
				form = StatForm()
				return render_to_response('report.html',{'form':form, 'kind': kind, 'total': total_sold,
										 'vals': values, 'len': lens, 'months': months},
										  context)
		else:
			form = StatForm()
			return render_to_response('report.html',{'form':form}, context)
	else:
		form = StatForm()
	return render_to_response('report.html',{'form':form}, context)