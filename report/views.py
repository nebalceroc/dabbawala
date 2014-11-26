from django.shortcuts import render, render_to_response
from delivery.models import Request, RequestProduct
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
				values = ['Total de Ventas']
				months = ['Mes']
				query = Request.objects.filter(pur_date__range=(start_date, end_date), state='A')
				total_sold = 0
				actual = start_date
				while actual < end_date:
					for sold in query.filter(pur_date__range=(actual, add_months(actual,1)-timedelta(days=1))):
						total_sold += sold.total
					values.append(total_sold)
					months.append(calendar.month_name[actual.month])
					actual = add_months(actual, 1)
					total_sold = 0
				arr = [months, values]
				arr = zip(*arr)
				arr = json.dumps(arr)
				form = StatForm()
				return render_to_response('report.html',{'form':form, 'kind': kind, 'total': total_sold,
										  'arr': arr},
										  context)
				
			if kind == 'P':
				values = [product.name]
				months = ['Mes']
				total_sold = 0
				query = RequestProduct.objects.filter(request__pur_date__range=(start_date, end_date), product = product, request__state = 'A')
				actual = start_date
				while actual < end_date:
					for sold in query.filter(request__pur_date__range=(actual, add_months(actual,1)-timedelta(days=1))):
						total_sold += sold.amount
					values.append(total_sold)
					months.append(calendar.month_name[actual.month])
					actual = add_months(actual, 1)
					total_sold = 0
				arr = [months, values]
				arr = zip(*arr)
				arr = json.dumps(arr)
				form = StatForm()
				return render_to_response('report.html',{'form':form, 'kind': kind, 'total': total_sold,
										 'arr': arr},
										  context)
		else:
			label = form.errors
			form = StatForm()
			return render_to_response('report.html',{'form':form, 'lab': label}, context)
	else:
		form = StatForm()
	return render_to_response('report.html',{'form':form}, context)