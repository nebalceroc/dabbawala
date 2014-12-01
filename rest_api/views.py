from django.shortcuts import render
from delivery.models import Product, Request, RequestProduct
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
import datetime
import re
import urllib

# Create your views here.
def query(request):
    if request.method == 'GET':
        query_type = request.GET.get('query')
        if query_type == 'allproducts':
            product_list = Product.objects.all()
            response = '\n'.join(["%s,%s,%s" % (prod.code, prod.name, prod.price) for prod in product_list])
            return HttpResponse(response)
        elif query_type == 'submit':
            form_user = request.GET.get('user')
            form_address = request.GET.get('address')
            form_products = [str(p) for p in request.GET.getlist('product')]

            if not form_address:
                return HttpResponse('0:La direccion no puede ser vacia')
            if not form_products:
                return HttpResponse('0:La lista de productos no puede ser vacia')

            u = User.objects.get(username='prokids')
            d = urllib.unquote(form_address)
            r = Request(state='C', user=u, dir=d, pur_date=datetime.datetime.now(), total=0)
            r.save()

            total = 0
            for prod in form_products:
                am = int(re.search(r'\d+', prod).group(0))
                na = re.split(str(am), prod)[1]
                print am, na

                p = Product.objects.filter(code=na)
                if not p:
                    return HttpResponse('0:El producto %s no existe' % na)
                else:
                    p = p[0]

                total += p.price * am
                rp = RequestProduct(request=r, product=p, amount=am)
                print rp.amount
                rp.save()
            r.total = total
            r.save()
            return HttpResponse('1:Pedido realizado, total %s USD, enviado a %s' % (total, d))


    # fuck templates, fuck the police #yolo
    return HttpResponse('''
        <h1>Dabbawala REST API</h1>

        <strong>GET /rest_api/comm</strong>
        <dl>
            <dt><tt>query=allproducts</tt></dt>
            <dd>Retorna la lista completa de productos disponibles.</dd>
        </dl>

        <strong>GET /rest_api/comm</strong>
        <dl>
            <dt><tt>query=submit</tt><dt>
            <dd>Realiza un pedido.</dd>

            <dt><tt>address=</tt><em>&lt;direccion del usuario&gt;</em></dt>
            <dt><tt>product=</tt><em>&lt;cantidad&gt;&lt;id del producto&gt;</em></dt>
            <dd>Establece los valores necesarios para realizar un pedido. </dd>
        </dl>
        ''')

