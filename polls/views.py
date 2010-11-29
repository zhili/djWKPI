# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from polls.models import Cell, KPI
from django.template import Context, loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

def index(request):
    t = loader.get_template('index.html')
    c = Context({
        # 'latest_poll_list': latest_poll_list,
    })
    return HttpResponse(t.render(c))

from django import forms
from datetime import datetime
from datetime import timedelta
# from django.contrib.admin.views.decorators import staff_member_required
import csv
class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file  = forms.FileField()

def handle_uploaded_file(f):
    try:
	    reader = csv.reader(f)
	    header = reader.next()
	    # print header
	    hdict = {}
	    for col in header:
	         hdict[col] = 0
	    # print hdict
	    last_cell_name = ''
	    for row in reader:
	        if not row:
	            # print 'push db'
	            # if Cell.objects.filter(cell_name=hdict['UCell Name']).exists():
	            #    ucell = Cell.objects.get(cell_name=hdict['UCell Name'])
	            # else:
	            #    ucell = Cell.objects.create(rnc_id=hdict['RNC Id'],cell_name=hdict['UCell Name'])
	            # item_date = datetime.strptime(hdict['Date'], '%m/%d/%Y %I:%M:%S %p') + timedelta(hours=int(hdict['Hour'])+1, minutes=int(hdict['Min']))
	            # kpi = KPI(date = item_date, K01=hdict['K01'], K02=hdict['K02'], K03=hdict['K03'], K04=hdict['K04'], K05=hdict['K05'],
	            #               K08_a = hdict['K08_a'], K08_b = hdict['K08_b'], K09_a = hdict['K09_a'], K09_b = hdict['K09_b'], K10_a=hdict['K10_a'], 
	            #               K10_b=hdict['K10_b'], K11_a=hdict['K11_a'], K11_b=hdict['K11_b'], K12_a=hdict['K12_a'], K12_b=hdict['K12_b'], K13_1a=hdict['K13_1a'], 
	            #               K13_1b=hdict['K13_1b'], K13_2a=hdict['K13_2a'], K13_2b=hdict['K13_2b'], K14_1a=hdict['K14_1a'], K14_1b=hdict['K14_1b'], K15=hdict['K15'], 
	            #               K16_a=hdict['K16_a'], K16_b=hdict['K16_b'], K19_a=hdict['K19_a'], K19_b=hdict['K19_b'], K20_a=hdict['K20_a'], K20_b=hdict['K20_b'], 
	            #               K21_a=hdict['K21_a'], K21_b=hdict['K21_b'], K22_ucell=hdict['K22_ucell'], K24=hdict['K24'], K25_a=hdict['K25_a'], K25_b=hdict['K25_b'],
	            #               K26_a=hdict['K26_a'], K26_b=hdict['K26_b'], K27=hdict['K27'], K29=hdict[''], K30_a=hdict['K30_a'], K30_b=hdict['K30_b'], 
	            #               K31_a=hdict['K31_a'], K31_b=hdict['K31_b'], K33_ucell=hdict['K33_ucell'], K34_ucell=hdict['K34_ucell'], K06=hdict['K06'], K28=hdict['K28'],
	            #               K07=hdict['K07'], K23=hdict['K23'], K17_a=hdict['K17_a'], K17_b=hdict['K17_b'], K18_a=hdict['K18_a'], K18_b=hdict['K18_b'], K32_a=hdict['K32_a'], K32_b=hdict['K32_b'])
	            # ucell.kpi_set.add(kpi)	            	
	            break
	        rid= row[0]
	        cn = row[1]
	        # get rid of '' to in error
	        row[5:] = [s if s!='' and s!='#EMPTY' else '0' for s in row[5:]]
	        if last_cell_name != cn:
	           # new cell
	           if last_cell_name != '':
	              # add to db except the first time
	              # print 'push db'
	              if Cell.objects.filter(cell_name=hdict['UCell Name']).exists():
	                 ucell = Cell.objects.get(cell_name=hdict['UCell Name'])
	              else:
	                 ucell = Cell.objects.create(rnc_id=hdict['RNC Id'],cell_name=hdict['UCell Name'])
	              item_date = datetime.strptime(hdict['Date'], '%m/%d/%Y %I:%M:%S %p') + timedelta(hours=int(hdict['Hour'])+1, minutes=int(hdict['Min']))
	              kpi = KPI(date = item_date, K01=hdict['K01'], K02=hdict['K02'], K03=hdict['K03'], K04=hdict['K04'], K05=hdict['K05'],
	                          K08_a = hdict['K08_a'], K08_b = hdict['K08_b'], K09_a = hdict['K09_a'], K09_b = hdict['K09_b'], K10_a=hdict['K10_a'], 
	                          K10_b=hdict['K10_b'], K11_a=hdict['K11_a'], K11_b=hdict['K11_b'], K12_a=hdict['K12_a'], K12_b=hdict['K12_b'], K13_1a=hdict['K13_1a'], 
	                          K13_1b=hdict['K13_1b'], K13_2a=hdict['K13_2a'], K13_2b=hdict['K13_2b'], K14_1a=hdict['K14_1a'], K14_1b=hdict['K14_1b'], K15=hdict['K15'], 
	                          K16_a=hdict['K16_a'], K16_b=hdict['K16_b'], K19_a=hdict['K19_a'], K19_b=hdict['K19_b'], K20_a=hdict['K20_a'], K20_b=hdict['K20_b'], 
	                          K21_a=hdict['K21_a'], K21_b=hdict['K21_b'], K22_ucell=hdict['K22_ucell'], K24=hdict['K24'], K25_a=hdict['K25_a'], K25_b=hdict['K25_b'],
	                          K26_a=hdict['K26_a'], K26_b=hdict['K26_b'], K27=hdict['K27'], K29=hdict['K29'], K30_a=hdict['K30_a'], K30_b=hdict['K30_b'], 
	                          K31_a=hdict['K31_a'], K31_b=hdict['K31_b'], K33_ucell=hdict['K33_ucell'], K34_ucell=hdict['K34_ucell'], K06=hdict['K06'], K28=hdict['K28'],
	                          K07=hdict['K07'], K23=hdict['K23'], K17_a=hdict['K17_a'], K17_b=hdict['K17_b'], K18_a=hdict['K18_a'], K18_b=hdict['K18_b'], K32_a=hdict['K32_a'], K32_b=hdict['K32_b'])
	              ucell.kpi_set.add(kpi)
	              # clear dict content
	           i = 0
	           for k in header:
	                if i > 4:
	                    hdict[k] = float(row[i])
	                else:
		                hdict[k] = row[i]             
	                i += 1
	           # print hdict
	           last_cell_name = cn
	           continue
            # sum the data with the same hour
	        i = 0 # the perf data start with index: 5
	        # print 'sum data'
	        # print hdict
	        for k in header:
	            if i > 4:
	                 hdict[k] += float(row[i])
	            i += 1

    except csv.Error, e:
        # render_to_response('UploadError.html', {'message':'You need to specify a csv file'})
	    return False
    # print 'push db'
    # print hdict
    if Cell.objects.filter(cell_name=hdict['UCell Name']).exists():
       ucell = Cell.objects.get(cell_name=hdict['UCell Name'])
    else:
       ucell = Cell.objects.create(rnc_id=hdict['RNC Id'],cell_name=hdict['UCell Name'])
    item_date = datetime.strptime(hdict['Date'], '%m/%d/%Y %I:%M:%S %p') + timedelta(hours=int(hdict['Hour'])+1, minutes=int(hdict['Min']))
    kpi = KPI(date = item_date, K01=hdict['K01'], K02=hdict['K02'], K03=hdict['K03'], K04=hdict['K04'], K05=hdict['K05'],
                  K08_a = hdict['K08_a'], K08_b = hdict['K08_b'], K09_a = hdict['K09_a'], K09_b = hdict['K09_b'], K10_a=hdict['K10_a'], 
                  K10_b=hdict['K10_b'], K11_a=hdict['K11_a'], K11_b=hdict['K11_b'], K12_a=hdict['K12_a'], K12_b=hdict['K12_b'], K13_1a=hdict['K13_1a'], 
                  K13_1b=hdict['K13_1b'], K13_2a=hdict['K13_2a'], K13_2b=hdict['K13_2b'], K14_1a=hdict['K14_1a'], K14_1b=hdict['K14_1b'], K15=hdict['K15'], 
                  K16_a=hdict['K16_a'], K16_b=hdict['K16_b'], K19_a=hdict['K19_a'], K19_b=hdict['K19_b'], K20_a=hdict['K20_a'], K20_b=hdict['K20_b'], 
                  K21_a=hdict['K21_a'], K21_b=hdict['K21_b'], K22_ucell=hdict['K22_ucell'], K24=hdict['K24'], K25_a=hdict['K25_a'], K25_b=hdict['K25_b'],
                  K26_a=hdict['K26_a'], K26_b=hdict['K26_b'], K27=hdict['K27'], K29=hdict['K29'], K30_a=hdict['K30_a'], K30_b=hdict['K30_b'], 
                  K31_a=hdict['K31_a'], K31_b=hdict['K31_b'], K33_ucell=hdict['K33_ucell'], K34_ucell=hdict['K34_ucell'], K06=hdict['K06'], K28=hdict['K28'],
                  K07=hdict['K07'], K23=hdict['K23'], K17_a=hdict['K17_a'], K17_b=hdict['K17_b'], K18_a=hdict['K18_a'], K18_b=hdict['K18_b'], K32_a=hdict['K32_a'], K32_b=hdict['K32_b'])
    ucell.kpi_set.add(kpi)
    return True

import StringIO
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
@csrf_exempt
def upload(request):

    if request.method == 'POST':
        # print request.is_ajax()
        # print request.META['HTTP_X_FILE_NAME']
        # with io.BufferedReader( io.BytesIO( request.raw_post_data) ) as stream:
        #      with io.BufferedWriter( io.FileIO( "/tmp/%s" % request.META['HTTP_X_FILE_NAME'], "wb" ) ) as destination:
        #           foo = stream.read( 1024 )
        #           while foo:
        #               destination.write( foo )
        #               foo = stream.read( 1024 )
        # print  request.POST
        # data =  request.FILES['qqfile']
        #        print data.name
        # form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        #          print 'valid'
        #          if (False == handle_uploaded_file(request.FILES['qqfile'])):
        # 	            # !!!not safe!!!
        # 	            return render_to_response('UploadError.html', {'message':'You need to specify a csv file'})
        # return HttpResponseRedirect('/admin/')
        pseudofile = StringIO.StringIO(request.raw_post_data)
        if (False == handle_uploaded_file(pseudofile)):
            HttpResponse(simplejson.dumps({"error":"error message to display"}))
        return HttpResponse(simplejson.dumps({"success": "true"}))
    return render_to_response(
        "admin/upload.html",
        RequestContext(request),
    )

# report = staff_member_required(upload)
from pyofc2  import * 
import time
from django.core.exceptions import ObjectDoesNotExist
def chart_by_id(request, cellname, chart_id):
    # print chart_id
    my_cell = Cell.objects.get(cell_name=cellname)
    today = date.today() + timedelta(days=1)
    begin = today - timedelta(days=10)
    t = title(text=my_cell.cell_name)
    chart = open_flash_chart()
    chart.title = t
    cell_kpi_set = my_cell.kpi_set.filter(date__range=(begin, today))
    if chart_id == '1':
        b = bar()
        y = y_axis()
        y.min, y.max, y.steps = 0, 100, 10
        chart.y_axis = y     
        x = x_axis()
        xlbls = x_axis_labels(steps=1, rotate='45', colour='#FF0000', size=16)
        lbls = []
        for item in cell_kpi_set:
	        lbls.append(item.date.strftime('%Y-%m-%d %H:%M:%S'))
    
        xlbls.labels = lbls 
        x.labels = xlbls
        chart.x_axis = x
    
        # l.halo_size = 10
        b.width = 4
        # l.dot_size = 4
        b.tip = '#key# <br> ?val#', 
        b.text = 'Drop Call Rate'

        b.values = [float(item.K19_a * 100.0 / item.K19_b) if item.K19_b > 0 else 0 for item in cell_kpi_set]
        chart.add_element(b)
    elif chart_id == '2':
        l = line_hollow()
        y = y_axis()
        y.min, y.max, y.steps = 0, 100, 10
        chart.y_axis = y     
        x = x_axis()
        xlbls = x_axis_labels(steps=1, rotate='45', colour='#FF0000', size=16)
        lbls = []

        for item in cell_kpi_set:
	        lbls.append(item.date.strftime('%Y-%m-%d %H:%M:%S'))
    
        xlbls.labels = lbls 
        x.labels = xlbls
        chart.x_axis = x
        l.colour = "#3133C0"
        l.width = 4
        # l.halo_size = 10
        l.dot_size = 4
        l.tip = '#key#  #val#'
        l.text = 'IRAT HO'
        l.values = [float(item.K18_a * 100.0 / item.K18_b) if item.K18_b > 0 else 0 for item in cell_kpi_set]
        chart.add_element(l)
    else:
	    None
    return HttpResponse(chart.render())

def chart_data(request, cellname):

    my_cell = Cell.objects.get(cell_name=cellname)
    today = date.today() + timedelta(days=1)
    begin = today - timedelta(days=10)

    cell_kpi_set = my_cell.kpi_set.filter(date__range=(begin, today))
    t = title(text=my_cell.cell_name)
    chart = open_flash_chart()
    chart.title = t
    chart.bg_colour = '#FFFFFF'
    y = y_axis()
    y.min, y.max, y.steps = 0, 100, 10
    y.grid_colour = '#EDF5F9'
    y.colour = '#FF6600'
    chart.y_axis = y     
    x = x_axis()
    x.grid_colour = '#EDF5F9'
    x.colour = '#FF6600'
    xlbls = x_axis_labels(steps=1, rotate='45', colour='#FF0000', size=16)
    lbls = []

    for item in cell_kpi_set:
        lbls.append(item.date.strftime('%Y-%m-%d %H:%M:%S'))
    xlbls.labels = lbls 
    x.labels = xlbls
    chart.x_axis = x

    l_K18 = line_hollow()
    l_K18.colour = "#3133C0"
    l_K18.width = 4
    l_K18.halo_size = 2
    # l_K18.dot_size = 4
    l_K18.tip = '#key#  #val#'
    l_K18.text = 'IRAT HO'
    l_K18.values = [float(item.K18_a * 100.0 / item.K18_b) if item.K18_b > 0 else 100.0 for item in cell_kpi_set]

    l_K19 = line_hollow()
    l_K19.colour = "#00FF00"
    l_K19.width = 4
    # l.halo_size = 10
    l_K19.dot_size = 4
    l_K19.tip = '#key#  #val#'
    l_K19.text = 'Drop Call'
    l_K19.values = [float(item.K19_a * 100.0 / item.K19_b) if item.K19_b > 0 else 0 for item in cell_kpi_set]

    l_K16 = line_hollow()
    l_K16.colour = "#A60289"
    l_K16.width = 4
    l_K16.halo_size = 2
    # l_K18.dot_size = 4
    l_K16.tip = '#key#  #val#'
    l_K16.text = 'Soft HO'
    l_K16.values = [float(item.K16_a * 100.0 / item.K16_b) if item.K16_b > 0 else 100.0 for item in cell_kpi_set]


    chart.add_element(l_K18)
    chart.add_element(l_K19)
    chart.add_element(l_K16)
    return HttpResponse(chart.render())

from datetime import date
from django.db.models import Sum
def worst_cells(request, ratetype):
    # print ratetype
    # today = date.today()
    # begin = today - timedelta(days=1) # worst cells in N days
    dateform = DateSelectForm()
    rnc_kpi = []
    kpi_list = []
    title = 'No Title'
    if ratetype == 'dcr':
	    # kpi_list = KPI.objects.filter(date__range=(begin, today), K19_b__gt=0, K19_a__gt=0).extra(select={'rate':'K19_a*1.0 / K19_b', 'all':'K19_b', 'part':'K19_a'}).order_by('-rate')[:20]
	    rnc_kpi_list = KPI.objects.values('ucell__rnc_id', 'date').annotate(K19_a_sum=Sum('K19_a'), K19_b_sum=Sum('K19_b')).order_by('-date')[:4]

	    for kp in rnc_kpi_list:
		    l = [kp['ucell__rnc_id'], kp['date'], kp['K19_a_sum'], kp['K19_b_sum'], kp['K19_a_sum']*100.0 / kp['K19_b_sum'] if  kp['K19_b_sum'] > 0 else 0]
		    rnc_kpi.append(l)
	    kpi_list = KPI.objects.filter(K19_b__gt=0, K19_a__gt=0).extra(select={'rate':'K19_a*100.0 / K19_b', 'all':'K19_b', 'part':'K19_a'}).order_by('-date','-rate')[:30]
	    title ='Drop Call Rate'
	    column_headers = ['Cell Name', 'RNC ID', 'Date', 'System Release', 'All Release', 'Drop Call Rate']
    elif ratetype == 'irat_ho':
	    rnc_kpi_list = KPI.objects.values('ucell__rnc_id', 'date').annotate(K18_a_sum=Sum('K18_a'), K18_b_sum=Sum('K18_b')).order_by('-date')[:4]
	    for kp in rnc_kpi_list:
		    l = [kp['ucell__rnc_id'], kp['date'], kp['K18_a_sum'], kp['K18_b_sum'], kp['K18_a_sum']*100.0 / kp['K18_b_sum'] if  kp['K18_b_sum'] > 0 else 100.0]
		    rnc_kpi.append(l)
	    kpi_list = KPI.objects.filter(K18_b__gt=0).extra(select={'rate':'K18_a*100.0 / K18_b','all':'K18_b', 'part':'K18_a'}).order_by('-date', 'rate')[:30]
	    title = 'IRAT HO Success Rate'
	    column_headers = ['Cell Name', 'RNC ID', 'Date', 'IRAT HO Success', 'IRAT HO Request', 'IRAT HO Success Rate']

    else: # default use dcr
	    return render_to_response('404.html')
    return render_to_response('worst_cells.html',  {'kpi_list':kpi_list, 'titleMsg':title, 'ColumnsHeader':column_headers, 'rnc_kpi':rnc_kpi, 'form':dateform}, RequestContext(request))
	
	
from django.db.models import Q

def tag_autocomplete(request):
    if request.GET.has_key('q'):
        q_str = request.GET['q']
        if len(q_str)>0:
            tags = (Cell.objects.filter(Q (rnc_id__icontains=request.GET['q']) | Q (cell_name__icontains=request.GET['q'])))[:10] 
            return HttpResponse('\n'.join(tag.cell_name for tag in tags))
    if request.method == 'POST': 
        form = CellNameForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            cn = form.cleaned_data['cellname']
            # print cn
            return HttpResponseRedirect(reverse('polls.views.results', args=(cn,)))
    return render_to_response('search.html', RequestContext(request))



def results(request, cellname):
    # print my_cell
    # print KPI.objects.values('ucell__rnc_id').annotate(Sum('K01'), Sum('K02')).order_by('date')[:1]
    if Cell.objects.filter(cell_name=cellname).exists():
	    # KPI.objects.values('ucell_id').order_by().annotate(Sum('K01'), Sum('K02'))
        my_cell = Cell.objects.get(cell_name=cellname)
        today = date.today() + timedelta(days=1)
        begin = today - timedelta(days=7)
        sum_columns = my_cell.kpi_set.filter(date__range=(begin, today)).aggregate(SK19_a=Sum('K19_a'), SK19_b=Sum('K19_b'), 
                                             SK20_a=Sum('K20_a'), SK20_b=Sum('K20_b'), SK21_a=Sum('K21_a'), SK21_b=Sum('K21_b'),
                                             SK18_a=Sum('K18_a'), SK18_b=Sum('K18_b'), SK16_a=Sum('K16_a'), SK16_b=Sum('K16_b'),
                                             SK17_a=Sum('K17_a'), SK17_b=Sum('K17_b'), SK06=Sum('K06'), SK07=Sum('K07'),
                                             SK01=Sum('K01'), SK02=Sum('K02'), SK03=Sum('K03'), SK04=Sum('K04'), SK05=Sum('K05'))
        kset = my_cell.kpi_set.filter(date__range=(begin, today)).order_by('date')
        category_dc = []
        category_ho = []
        category_tv = []
        for row in kset:
            l_dc = [row.date, row.K19_a, row.K19_b, row.K19_a * 100.0 / row.K19_b if row.K19_b > 0 else 0, 
                              row.K20_a, row.K20_b, row.K20_a * 100.0 / row.K20_b if row.K20_b > 0 else 0, 
                              row.K21_a, row.K21_b, row.K21_a * 100.0 / row.K21_b if row.K21_b > 0 else 0]
            category_dc.append(l_dc)
            l_ho = [row.date, row.K18_a, row.K18_b, row.K18_a * 100.0 / row.K18_b if row.K18_b > 0 else 100.0, 
                              row.K16_a, row.K16_b, row.K16_a * 100.0 / row.K16_b if row.K16_b > 0 else 100.0,
                              row.K17_a, row.K17_b, row.K17_a * 100.0 / row.K17_b if row.K17_b > 0 else 100.0]
            category_ho.append(l_ho)
            l_tv = [row.date, row.K01, row.K02, row.K03, row.K04, row.K05, row.K06, row.K07]
            category_tv.append(l_tv)

        dc_total = ['total', sum_columns['SK19_a'], sum_columns['SK19_b'], sum_columns['SK19_a'] * 100.0 / sum_columns['SK19_b'] if sum_columns['SK19_b'] > 0 else 0, 
                      sum_columns['SK20_a'], sum_columns['SK20_b'], sum_columns['SK20_a'] * 100.0 / sum_columns['SK20_b'] if sum_columns['SK20_b'] > 0 else 0, 
                      sum_columns['SK21_a'], sum_columns['SK21_b'], sum_columns['SK21_a'] * 100.0 / sum_columns['SK21_b'] if sum_columns['SK21_b'] > 0 else 0]                      
        category_dc.append(dc_total)
        ho_total = ['total', sum_columns['SK18_a'], sum_columns['SK18_b'], sum_columns['SK18_a'] * 100.0 / sum_columns['SK18_b'] if sum_columns['SK18_b'] > 0 else 100.0,
                             sum_columns['SK16_a'], sum_columns['SK16_b'], sum_columns['SK16_a'] * 100.0 / sum_columns['SK16_b'] if sum_columns['SK16_b'] > 0 else 100.0,
                             sum_columns['SK17_a'], sum_columns['SK17_b'], sum_columns['SK17_a'] * 100.0 / sum_columns['SK17_b'] if sum_columns['SK17_b'] > 0 else 100.0]
        category_ho.append(ho_total)
        tv_total = ['total', sum_columns['SK01'], sum_columns['SK02'], sum_columns['SK03'], sum_columns['SK04'], sum_columns['SK05'], sum_columns['SK06'], sum_columns['SK07']]
        category_tv.append(tv_total)
        dc_headers = ['Cell Name', 'Date', 'Sys Rls AMR', 'All Rls AMR', 'DCR AMR',
                      'Sys Rls VP', 'All Rls VP', 'DCR VP',
                      'Sys Rls PS', 'All Rls PS', 'DCR PS R99']
        ho_headers = ['Cell Name', 'Date', 'IRAT HO Ss', 'IRAT HO Rt', 'IRAT HO SRate', 
                      'ASet Update Ss', 'ASet Update Rt', 'Soft Ho SRate',
                      'IF HO Ss', 'IF HO Rt', 'IF Ho SRate']
        tv_headers = ['Cell Name', 'Date', 'AMR TV', 'CS TV', 'VP TV', 'PS UL Thrg', 'PS DL Thrg', 'EUL UL Thrg', 'HSDPA DL Thrg']
        return render_to_response('result.html', {'cell_name':cellname, 'dc_head':dc_headers, 'cate_dc':category_dc, 'ho_head':ho_headers, 'cate_ho':category_ho,'tv_head':tv_headers, 'cate_tv': category_tv})
    return render_to_response('404.html')
	
class CellNameForm(forms.Form):
    cellname = forms.CharField(max_length=100)

def about(request):
    return render_to_response('about.html')


class DateSelectForm(forms.Form):        

    selectedDate = forms.DateField(('%d/%m/%Y',), label='Date', required=False, initial=date.today(),
        widget=forms.DateTimeInput(format='%d/%m/%Y', attrs={
            'class':'input',
            'readonly':'readonly',
            'size':'15'
        })
    )

def changedate(request, ratetype):
    kpi_list = []
    title = 'Not Found'
    rnc_kpi = []
    column_headers = []
    dateform = DateSelectForm()
    if request.method == 'POST':
        dateform = DateSelectForm(request.POST) # A form bound to the POST data
        if dateform.is_valid():
            selected_date = dateform.cleaned_data['selectedDate']
            if ratetype == 'dcr':      
                rnc_kpi_list = KPI.objects.filter(date__range=(selected_date, selected_date+timedelta(days=1))).values('ucell__rnc_id', 'date').annotate(K19_a_sum=Sum('K19_a'), K19_b_sum=Sum('K19_b'))
                for kp in rnc_kpi_list:
                    l = [kp['ucell__rnc_id'], kp['date'], kp['K19_a_sum'], kp['K19_b_sum'], kp['K19_a_sum']*100.0 / kp['K19_b_sum'] if  kp['K19_b_sum'] > 0 else 0]
                    rnc_kpi.append(l)
                kpi_list = KPI.objects.filter(date__range=(selected_date, selected_date+timedelta(days=1)), K19_b__gt=0, K19_a__gt=0).extra(select={'rate':'K19_a*100.0 / K19_b', 'all':'K19_b', 'part':'K19_a'}).order_by('-rate')[:30]
                title ='Drop Call Rate'
                column_headers = ['Cell Name', 'RNC ID', 'Date', 'System Release', 'All Release', 'Drop Call Rate']
            elif ratetype == 'irat_ho':
                rnc_kpi_list = KPI.objects.filter(date__range=(selected_date, selected_date+timedelta(days=1))).values('ucell__rnc_id', 'date').annotate(K18_a_sum=Sum('K18_a'), K18_b_sum=Sum('K18_b'))
                for kp in rnc_kpi_list:
                    l = [kp['ucell__rnc_id'], kp['date'], kp['K18_a_sum'], kp['K18_b_sum'], kp['K18_a_sum']*100.0 / kp['K18_b_sum'] if  kp['K18_b_sum'] > 0 else 100.0]
                    rnc_kpi.append(l)
                kpi_list = KPI.objects.filter(date__range=(selected_date, selected_date+timedelta(days=1)), K18_b__gt=0).extra(select={'rate':'K18_a*100.0 / K18_b','all':'K18_b', 'part':'K18_a'}).order_by('rate')[:30]
                title = 'IRAT HO Success Rate'
                column_headers = ['Cell Name', 'RNC ID', 'Date', 'IRAT HO Success', 'IRAT HO Request', 'IRAT HO Success Rate']
    	    else: # 404
			    return render_to_response('404.html') 
    return render_to_response('worst_cells.html',  {'kpi_list':kpi_list, 'titleMsg':title, 'ColumnsHeader':column_headers, 'rnc_kpi':rnc_kpi, 'form':dateform}, RequestContext(request))