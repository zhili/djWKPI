# # 
#  views.py
#  mysite
#  
#  Created by zhili hu on 2010-12-04.
#  Copyright 2010 __MyCompanyName__. All rights reserved.
# 

from django.http import HttpResponseRedirect, HttpResponse
from polls.models import Cell, KPI
from django.template import Context, loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse


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
	            break
	        rid= row[0]
	        cn = row[1]
	        # get rid of '' to in error
	        row[5:] = [s if s!='' and s!='#EMPTY' else '0' for s in row[5:]]
	        if last_cell_name != cn:
	           # new cell
	           if last_cell_name != '':
	              # add the parsed cell's content to db, except for the 1st time
	              # print 'push db'
	              if Cell.objects.filter(cell_name=hdict['UCell Name']).exists():
	                 ucell = Cell.objects.get(cell_name=hdict['UCell Name'])
	              else:
	                 ucell = Cell.objects.create(rnc_id=hdict['RNC Id'],cell_name=hdict['UCell Name'])
	              item_date = datetime.strptime(hdict['Date'], '%m/%d/%Y %I:%M:%S %p') + timedelta(hours=int(hdict['Hour']), minutes=int(hdict['Min']))
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
	           # clear dict content and add to new cell's info to the dict
	           i = 0
	           for k in header:
	                if i > 4:
	                    hdict[k] = float(row[i])
	                else:
		                hdict[k] = row[i]             
	                i += 1
	           # print hdict
	           last_cell_name = cn
	        else:
               # sum the data with the same hour
	           i = 0 # the perf data start with index: 5
	           for k in header:
	               if i > 4:
	                   hdict[k] += float(row[i])
	               i += 1

    except csv.Error, e:
        # render_to_response('UploadError.html', {'message':'You need to specify a csv file'})
	    return False
    if Cell.objects.filter(cell_name=hdict['UCell Name']).exists():
       ucell = Cell.objects.get(cell_name=hdict['UCell Name'])
    else:
       ucell = Cell.objects.create(rnc_id=hdict['RNC Id'],cell_name=hdict['UCell Name'])
    item_date = datetime.strptime(hdict['Date'], '%m/%d/%Y %I:%M:%S %p') + timedelta(hours=int(hdict['Hour']), minutes=int(hdict['Min']))
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


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        # data =  request.FILES['qqfile']
        #        print data.name
        # form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        #          print 'valid'
        #          if (False == handle_uploaded_file(request.FILES['qqfile'])):
        # 	            # !!!not safe!!!
        # 	            return render_to_response('UploadError.html', {'message':'You need to specify a csv file'})
        # return HttpResponseRedirect('/admin/')
        # print 'at post'
        for field_name in request.FILES:
            uploaded_file = request.FILES[field_name]
            if (False == handle_uploaded_file(uploaded_file)):
                return render_to_response('UploadError.html', {'message':'You need to specify a csv file'})
        # indicate that everything is OK for SWFUpload
        return HttpResponse("ok", mimetype="text/plain")

    return render_to_response(
        "admin/upload.html", context_instance=RequestContext(request)
    )

# report = staff_member_required(upload)
from pyofc2  import * 
import time
from django.core.exceptions import ObjectDoesNotExist
def chart_by_id(request, cellname, chart_id):
    my_cell = Cell.objects.get(cell_name=cellname)
    edate_tmp = datetime.strptime(request.GET.get('edate', date.today()), "%m/%d/%Y")
    sdate_tmp = datetime.strptime(request.GET.get('sdate', date.today()), "%m/%d/%Y")
    if edate_tmp - sdate_tmp < timedelta (days = 1):
        temp = edate_tmp
        edate_tmp = sdate_tmp
        sdate_tmp = temp
    sdate = sdate_tmp.strftime("%Y-%m-%d")
    edate = (edate_tmp + timedelta (days = 1)).strftime("%Y-%m-%d")
    t = title(text=my_cell.cell_name)
    chart = open_flash_chart()
    chart.title = t
    chart.bg_colour = '#FFFFFF'
    y = y_axis()
    y.min, y.max, y.steps = 0, 105, 10
    y.grid_colour = '#EDF5F9'
    y.colour = '#FF6600'
    chart.y_axis = y     
    x = x_axis()
    x.grid_colour = '#EDF5F9'
    x.colour = '#FF6600'
    xlbls = x_axis_labels(steps=1, rotate='45', colour='#FF0000', size=16)
    lbls = []
    
    cell_kpi_set = my_cell.kpi_set.filter(date__range=(sdate, edate))

    # if cell_kpi_set.count() > 0: no need to check this becausee ofc can handle empty value list and leave basic graph structure

    for item in cell_kpi_set:
        lbls.append(item.date.strftime('%Y-%m-%d %H:%M:%S'))
    xlbls.labels = lbls 
    x.labels = xlbls
    chart.x_axis = x
    
    if chart_id == '1':
        l_K18 = line()
        l_K18.colour = "#1DB3D9"
        l_K18.width = 4
         # l_K18.halo_size = 2
         # l_K18.dot_size = 4
        l_K18.tip = '#key#:#val#'
        l_K18.text = 'IRAT HO'
        l_K18.values = [float(item.K18_a * 100.0 / item.K18_b) if item.K18_b > 0 else 100.0 for item in cell_kpi_set]
        l_K18.font_size = 14
        
        l_K25 = line_hollow()
        l_K25.colour = "#FF1493"
        l_K25.width = 4
        l_K25.halo_size = 2
        l_K25.dot_size = 4
        l_K25.tip = '#key#:#val#'
        l_K25.text = 'HSDPA RAB'
        l_K25.values = [float(item.K25_a * 100.0 / item.K25_b) if item.K25_b > 0 else 100.0 for item in cell_kpi_set]
        l_K25.font_size = 14
        
        l_K30 = line_hollow()
        l_K30.colour = "#54FF9F"
        l_K30.width = 4
         # l_K18.halo_size = 2
         # l_K18.dot_size = 4
        l_K30.tip = '#key#:#val#'
        l_K30.text = 'HSUPA RAB'
        l_K30.values = [float(item.K30_a * 100.0 / item.K30_b) if item.K30_b > 0 else 100.0 for item in cell_kpi_set]
        l_K30.font_size = 14
        
        chart.add_element(l_K30)
        chart.add_element(l_K18)
        chart.add_element(l_K25)

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

def maxinum(iterable, default=1):
    try:
        return max(max(iterable), default)
    except ValueError:
        return default
        
def chart_data(request, cellname):

    my_cell = Cell.objects.get(cell_name=cellname)
    # today = date.today() + timedelta(days=1)
    # begin = date.today() - timedelta(days=10)

    edate_tmp = datetime.strptime(request.GET.get('edate', date.today()), "%m/%d/%Y")
    sdate_tmp = datetime.strptime(request.GET.get('sdate', date.today()), "%m/%d/%Y")
    if edate_tmp - sdate_tmp < timedelta (days = 1):
        temp = edate_tmp
        edate_tmp = sdate_tmp
        sdate_tmp = temp
    sdate = sdate_tmp.strftime("%Y-%m-%d")
    edate = (edate_tmp + timedelta (days = 1)).strftime("%Y-%m-%d")
    
    t = title(text=my_cell.cell_name)
    chart = open_flash_chart()
    chart.title = t
    chart.bg_colour = '#FFFFFF'
    y = y_axis()
    # y.min, y.max, y.steps = 0, 100, 10
    y.grid_colour = '#EDF5F9'
    y.colour = '#FF6600'
    chart.y_axis = y     
    x = x_axis()
    x.grid_colour = '#EDF5F9'
    x.colour = '#FF6600'
    xlbls = x_axis_labels(steps=1, rotate='45', colour='#FF0000', size=16)
    lbls = []
    
    cell_kpi_set = my_cell.kpi_set.filter(date__range=(sdate, edate))

    # if cell_kpi_set.count() > 0: no need to check this becausee ofc can handle empty value list and leave basic graph structure

    for item in cell_kpi_set:
        lbls.append(item.date.strftime('%Y-%m-%d %H:%M:%S'))
    xlbls.labels = lbls 
    x.labels = xlbls
    chart.x_axis = x



    l_K19 = line_hollow()
    l_K19.colour = "#00FF00"
    l_K19.width = 4
    # l_K19.halo_size = 2
    # l_K19.dot_size = 4
    l_K19.tip = '#key#:#val#'
    l_K19.text = 'DCR AMR'
    l_K19.values = [float(item.K19_a * 100.0 / item.K19_b) if item.K19_b > 0 else 0 for item in cell_kpi_set]
    l_K19.font_size = 14

    l_K26 = line_hollow()
    l_K26.colour = "#A60289"
    l_K26.width = 4
    l_K26.halo_size = 2
    l_K26.dot_size = 4
    l_K26.tip = '#key#:#val#'
    l_K26.text = 'DCR HSDPA'
    l_K26.values = [float(item.K26_a * 100.0 / item.K26_b) if item.K26_b > 0 else 0 for item in cell_kpi_set]
    l_K26.font_size = 14

    l_K31 = line_hollow()
    l_K31.colour = "#FF2626"
    l_K31.width = 4
    # l_K31.halo_size = 2
    # l_K31.dot_size = 4
    l_K31.tip = '#key#:#val#'
    l_K31.text = 'DCR HSUPA'
    l_K31.values = [float(item.K31_a * 100.0 / item.K31_b) if item.K31_b > 0 else 0 for item in cell_kpi_set]
    l_K31.font_size = 14
    
    yxis_max = maxinum(l_K19.values+l_K26.values+l_K31.values)

    y.min, y.max, y.steps = 0, round(yxis_max) + 1, round(yxis_max / 10)
    # chart.add_element(l_K18)
    chart.add_element(l_K19)
    chart.add_element(l_K26)
    chart.add_element(l_K31)
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
    latest_datetime = KPI.objects.order_by('-date').values('date')[0]
    latest_day = latest_datetime['date'].date()
    if ratetype == 'dcr':
	    # kpi_list = KPI.objects.filter(date__range=(begin, today), K19_b__gt=0, K19_a__gt=0).extra(select={'rate':'K19_a*1.0 / K19_b', 'all':'K19_b', 'part':'K19_a'}).order_by('-rate')[:20]
	    rnc_kpi_list = KPI.objects.values('ucell__rnc_id', 'date').annotate(K19_a_sum=Sum('K19_a'), K19_b_sum=Sum('K19_b')).order_by('-date')[:8]

	    for kp in rnc_kpi_list:
		    l = [kp['ucell__rnc_id'], kp['date'], kp['K19_a_sum'], kp['K19_b_sum'], kp['K19_a_sum']*100.0 / kp['K19_b_sum'] if  kp['K19_b_sum'] > 0 else 0]
		    rnc_kpi.append(l)
	    kpi_list = KPI.objects.filter(date__range=(latest_day, latest_day+timedelta(days=1)), K19_b__gt=0, K19_a__gt=1).extra(select={'rate':'K19_a*100.0 / K19_b', 'all':'K19_b', 'part':'K19_a'}).order_by('-K19_a','-rate')
	    title ='Drop Call Rate'
	    column_headers = ['Cell Name', 'RNC ID', 'Date', 'System Release', 'All Release', 'Drop Call Rate']
    elif ratetype == 'irat_ho':
	    rnc_kpi_list = KPI.objects.values('ucell__rnc_id', 'date').annotate(K18_a_sum=Sum('K18_a'), K18_b_sum=Sum('K18_b')).order_by('-date')[:8]
	    for kp in rnc_kpi_list:
		    l = [kp['ucell__rnc_id'], kp['date'], kp['K18_a_sum'], kp['K18_b_sum'], kp['K18_b_sum']-kp['K18_a_sum'], kp['K18_a_sum']*100.0 / kp['K18_b_sum'] if  kp['K18_b_sum'] > 0 else 100.0]
		    rnc_kpi.append(l)
	    kpi_list = KPI.objects.filter(date__range=(latest_day, latest_day+timedelta(days=1)), K18_b__gt=0).extra(select={'rate':'K18_a*100.0 / K18_b','all':'K18_b', 'part':'K18_a'}, where=['K18_b - K18_a >= 2']).order_by('rate')
	    title = 'IRAT HO Success Rate'
	    column_headers = ['Cell Name', 'RNC ID', 'Date', 'IRAT HO Success', 'IRAT HO Request', 'IRAT Failure', 'IRAT HO Success Rate']
    elif ratetype == 'hdrab':
	    rnc_kpi_list = KPI.objects.values('ucell__rnc_id', 'date').annotate(K25_a_sum=Sum('K25_a'), K25_b_sum=Sum('K25_b')).order_by('-date')[:8]
	    for kp in rnc_kpi_list:
		    l = [kp['ucell__rnc_id'], kp['date'], kp['K25_a_sum'], kp['K25_b_sum'], kp['K25_b_sum']-kp['K25_a_sum'], kp['K25_a_sum']*100.0 / kp['K25_b_sum'] if  kp['K25_b_sum'] > 0 else 100.0]
		    rnc_kpi.append(l)
	    kpi_list = KPI.objects.filter(date__range=(latest_day, latest_day+timedelta(days=1)), K25_b__gt=0).extra(select={'rate':'K25_a*100.0 / K25_b','all':'K25_b', 'part':'K25_a'}, where=['K25_b - K25_a >= 50']).order_by('rate')
	    title = 'HSDPA Rab EST Success Rate'
	    column_headers = ['Cell Name', 'RNC ID', 'Date', 'HSDPA Rab EST Ss', 'HSDPA Rab EST Att', 'HSDPA Rab Failure', 'RAB EST SRate(HSDPA)']
    elif ratetype == 'hurab':
	    rnc_kpi_list = KPI.objects.values('ucell__rnc_id', 'date').annotate(K30_a_sum=Sum('K30_a'), K30_b_sum=Sum('K30_b')).order_by('-date')[:8]
	    for kp in rnc_kpi_list:
		    l = [kp['ucell__rnc_id'], kp['date'], kp['K30_a_sum'], kp['K30_b_sum'], kp['K30_b_sum']-kp['K30_a_sum'], kp['K30_a_sum']*100.0 / kp['K30_b_sum'] if  kp['K30_b_sum'] > 0 else 100.0]
		    rnc_kpi.append(l)
	    kpi_list = KPI.objects.filter(date__range=(latest_day, latest_day+timedelta(days=1)), K30_b__gt=0).extra(select={'rate':'K30_a*100.0 / K30_b','all':'K30_b', 'part':'K30_a'}, where=['K30_b - K30_a >= 50']).order_by('rate')
	    title = 'HSUPA Rab EST Success Rate'
	    column_headers = ['Cell Name', 'RNC ID', 'Date', 'EUL Rab EST Ss', 'EUL Rab EST Att', 'HSUPA Rab Failure','RAB EST SRate (HSUPA)']
    elif ratetype == 'rrc':
	    rnc_kpi_list = KPI.objects.values('ucell__rnc_id', 'date').annotate(K08_a_sum=Sum('K08_a'), K08_b_sum=Sum('K08_b')).order_by('-date')[:8]
	    for kp in rnc_kpi_list:
	        l = [kp['ucell__rnc_id'], kp['date'], kp['K08_a_sum'], kp['K08_b_sum'], kp['K08_b_sum']-kp['K08_a_sum'],kp['K08_a_sum']*100.0 / kp['K08_b_sum'] if  kp['K08_b_sum'] > 0 else 100.0]
	        rnc_kpi.append(l)
	    kpi_list = KPI.objects.filter(date__range=(latest_day, latest_day+timedelta(days=1)), K08_b__gt=0).extra(select={'rate':'K08_a*100.0 / K08_b','all':'K08_b', 'part':'K08_a'}, where=['K08_b - K08_a >= 3']).order_by('rate')
	    title = 'RRC Setup Success Rate'
	    column_headers = ['Cell Name', 'RNC ID', 'Date', 'RRC Conn SS', 'RRC Conn Att', 'RRC Conn Failure','RRC Setup SRate']
    else: # default use dcr
	    return render_to_response('404.html')
    return render_to_response('worst_cells.html',  {'kpi_list':kpi_list, 'titleMsg':title, 'ColumnsHeader':column_headers, 'rnc_kpi':rnc_kpi, 'form':dateform}, RequestContext(request))
	
	
from django.db.models import Q

def tag_autocomplete(request):
    if request.GET.has_key('name_startsWith'):
        q_str = request.GET['name_startsWith']
        if len(q_str)>0:
            tags = (Cell.objects.filter(Q (rnc_id__icontains=q_str) | Q (cell_name__icontains=q_str)))[:10] 
            response_dict = {}
            response_dict.update({'cellnames':[tag.cell_name for tag in tags]})
            return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    if request.method == 'POST': 
        form = CellNameForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            cn = form.cleaned_data['cellname']
 
            return HttpResponseRedirect(reverse('polls.views.results', args=(cn.strip(),)))
    return render_to_response('search.html', RequestContext(request))


def prettyfloat(number):
    return "%0.2f" % number  # Works the same.

def results(request, cellname, sdate = date.today() - timedelta(days=10), edate = date.today() + timedelta(days=1)):
    # print my_cell
    # print KPI.objects.values('ucell__rnc_id').annotate(Sum('K01'), Sum('K02')).order_by('date')[:1]
    dateform = DateRangeSelectForm()
    if request.method == 'POST':
        dateform = DateRangeSelectForm(request.POST) # A form bound to the POST data
        if dateform.is_valid():
           sdate = dateform.cleaned_data['startDate']
           edate = dateform.cleaned_data['endDate']
           if edate - sdate < timedelta (days = 1):
               temp = edate
               edate = sdate
               sdate = temp
           edate += timedelta(days=1)
    if Cell.objects.filter(cell_name=cellname).exists():
	    # KPI.objects.values('ucell_id').order_by().annotate(Sum('K01'), Sum('K02'))
        my_cell = Cell.objects.get(cell_name=cellname)

        kset = my_cell.kpi_set.filter(date__range=(sdate, edate)).order_by('date')
        category_dc = []
        category_ho = []
        category_tv = []
        if kset.count() > 0:
            for row in kset:
                l_dc = [row.date, row.K19_a, row.K19_b, prettyfloat(row.K19_a * 100.0 / row.K19_b if row.K19_b > 0 else 0), 
                                  row.K20_a, row.K20_b, prettyfloat(row.K20_a * 100.0 / row.K20_b if row.K20_b > 0 else 0), 
                                  row.K21_a, row.K21_b, prettyfloat(row.K21_a * 100.0 / row.K21_b if row.K21_b > 0 else 0)]
                category_dc.append(l_dc)
                l_ho = [row.date, row.K18_a, row.K18_b, prettyfloat(row.K18_a * 100.0 / row.K18_b if row.K18_b > 0 else 100.0), 
                                  row.K16_a, row.K16_b, prettyfloat(row.K16_a * 100.0 / row.K16_b if row.K16_b > 0 else 100.0),
                                  row.K17_a, row.K17_b, prettyfloat(row.K17_a * 100.0 / row.K17_b if row.K17_b > 0 else 100.0)]
                category_ho.append(l_ho)
                l_tv = [row.date, prettyfloat(row.K01), prettyfloat(row.K02), prettyfloat(row.K03), prettyfloat(row.K04), prettyfloat(row.K05), prettyfloat(row.K06), prettyfloat(row.K07)]
                category_tv.append(l_tv)
            sum_columns = my_cell.kpi_set.filter(date__range=(sdate, edate)).aggregate(SK19_a=Sum('K19_a'), SK19_b=Sum('K19_b'), 
                                                 SK20_a=Sum('K20_a'), SK20_b=Sum('K20_b'), SK21_a=Sum('K21_a'), SK21_b=Sum('K21_b'),
                                                 SK18_a=Sum('K18_a'), SK18_b=Sum('K18_b'), SK16_a=Sum('K16_a'), SK16_b=Sum('K16_b'),
                                                 SK17_a=Sum('K17_a'), SK17_b=Sum('K17_b'), SK06=Sum('K06'), SK07=Sum('K07'),
                                                 SK01=Sum('K01'), SK02=Sum('K02'), SK03=Sum('K03'), SK04=Sum('K04'), SK05=Sum('K05'))
            dc_total = ['total', sum_columns['SK19_a'], sum_columns['SK19_b'], prettyfloat(sum_columns['SK19_a'] * 100.0 / sum_columns['SK19_b'] if sum_columns['SK19_b'] > 0 else 0), 
                          sum_columns['SK20_a'], sum_columns['SK20_b'], prettyfloat(sum_columns['SK20_a'] * 100.0 / sum_columns['SK20_b'] if sum_columns['SK20_b'] > 0 else 0), 
                          sum_columns['SK21_a'], sum_columns['SK21_b'], prettyfloat(sum_columns['SK21_a'] * 100.0 / sum_columns['SK21_b'] if sum_columns['SK21_b'] > 0 else 0)]                      
            category_dc.append(dc_total)
            ho_total = ['total', sum_columns['SK18_a'], sum_columns['SK18_b'], prettyfloat(sum_columns['SK18_a'] * 100.0 / sum_columns['SK18_b'] if sum_columns['SK18_b'] > 0 else 100.0),
                                 sum_columns['SK16_a'], sum_columns['SK16_b'], prettyfloat(sum_columns['SK16_a'] * 100.0 / sum_columns['SK16_b'] if sum_columns['SK16_b'] > 0 else 100.0),
                                 sum_columns['SK17_a'], sum_columns['SK17_b'], prettyfloat(sum_columns['SK17_a'] * 100.0 / sum_columns['SK17_b'] if sum_columns['SK17_b'] > 0 else 100.0)]
            category_ho.append(ho_total)
            tv_total = ['total', prettyfloat(sum_columns['SK01']), prettyfloat(sum_columns['SK02']), prettyfloat(sum_columns['SK03']), prettyfloat(sum_columns['SK04']), prettyfloat(sum_columns['SK05']), prettyfloat(sum_columns['SK06']), prettyfloat(sum_columns['SK07'])]
            category_tv.append(tv_total)
        dc_headers = ['Cell Name', 'Date', 'Sys Rls AMR', 'All Rls AMR', 'DCR AMR',
                      'Sys Rls VP', 'All Rls VP', 'DCR VP',
                      'Sys Rls PS', 'All Rls PS', 'DCR PS R99']
        ho_headers = ['Cell Name', 'Date', 'IRAT HO Ss', 'IRAT HO Rt', 'IRAT HO SRate', 
                      'ASet Update Ss', 'ASet Update Rt', 'Soft Ho SRate',
                      'IF HO Ss', 'IF HO Rt', 'IF Ho SRate']
        tv_headers = ['Cell Name', 'Date', 'AMR TV', 'VP TV', 'CS TV', 'PS UL Thrg', 'PS DL Thrg', 'EUL UL Thrg', 'HSDPA DL Thrg']
        hsdpa_headers = ['Cell Name', 'Date', 'Sys Rls HS-DSCH', 'All Rls HS-DSCH', 'DCR HSDPA', 'HSDPA Rab EST Ss', 'HSDPA Rab EST Att','RAB EST SRate(HSDPA)', 'HSDPA RLC TV(Mbytes)', 'HSDPA RLC Thrg(kbps)', 'Avg HSDPA user', 'Iu-PS DL TV(MB)']
        hsupa_headers = ['Cell Name', 'Date', 'Sys Rls E-DCH', 'All Rls E-DCH', 'DCR (HSUPA)', 'EUL Rab EST Ss', 'EUL Rab EST Att', 'RAB EST SRate (HSUPA)', 'HSUPA RLC TV(Mbytes)', 'HSUPA RLC Thrg(kbps)', 'Avg HSUPA user', 'Iu-PS UL TV(MB)']	
        rrc_headers = ['Cell Name', 'Date', 'RRC Conn Ss (Sv)',	'RRC Conn Att (Sv)', 'RRC Setup SRate(Sv)', 'RRC Con Ss(Oth)','RRC Conn Att(Oth)', 'RRC Setup SRate(Oth)', 'RRC Conn Ss(CS)', 'RRC Conn Att(CS)', 'RRC Con Ss(PS)', 'RRC Conn Att(PS)']
        rab_headers = ['Cell Name', 'Date', 'CS Rab EST Ss', 'CS Rab EST Att','CS Rab EST SRate', 'PS Rab EST Ss','PS Rab EST Att', 'RAB EST SRate(PS)', 'AMR Rab EST Ss', 'AMR Rab EST Att', 'VP Rab EST Ss', 'VP Rab EST Att']
        return render_to_response('result.html', {'cell_name':cellname, 'dc_head':dc_headers, 'cate_dc':category_dc, 'ho_head':ho_headers, 'cate_ho':category_ho,'tv_head':tv_headers, 'cate_tv': category_tv, 'hsdpa_head':hsdpa_headers, 'hsupa_head':hsupa_headers, 'rrc_head':rrc_headers, 'rab_head':rab_headers, 'form':dateform}, RequestContext(request))
    return render_to_response('404.html')
	
class CellNameForm(forms.Form):
    cellname = forms.CharField(max_length=100)

def about(request):
    return render_to_response('about.html', RequestContext(request))


class DateSelectForm(forms.Form):        

    selectedDate = forms.DateField(('%d/%m/%Y',), label='Date', required=False, initial=date.today(),
        widget=forms.DateTimeInput(format='%d/%m/%Y', attrs={
            'class':'input',
            'readonly':'readonly',
            'size':'15'
        })
    )

class DateRangeSelectForm(forms.Form):        

    startDate = forms.DateField(('%m/%d/%Y',), label='From', required=False, initial=date.today() - timedelta(days=10),
        widget=forms.DateTimeInput(format='%m/%d/%Y', attrs={
            'class':'input',
            'readonly':'readonly',
            'size':'15'
        })
    )
    endDate = forms.DateField(('%m/%d/%Y',), label='To', required=False, initial=date.today(),
        widget=forms.DateTimeInput(format='%m/%d/%Y', attrs={
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
                kpi_list = KPI.objects.filter(date__range=(selected_date, selected_date+timedelta(days=1)), K19_b__gt=0, K19_a__gt=1).extra(select={'rate':'K19_a*100.0 / K19_b', 'all':'K19_b', 'part':'K19_a'}).order_by('-K19_a','-rate')
                title ='Drop Call Rate'
                column_headers = ['Cell Name', 'RNC ID', 'Date', 'System Release', 'All Release', 'Drop Call Rate']
            elif ratetype == 'irat_ho':
                rnc_kpi_list = KPI.objects.filter(date__range=(selected_date, selected_date+timedelta(days=1))).values('ucell__rnc_id', 'date').annotate(K18_a_sum=Sum('K18_a'), K18_b_sum=Sum('K18_b'))
                for kp in rnc_kpi_list:
                    l = [kp['ucell__rnc_id'], kp['date'], kp['K18_a_sum'], kp['K18_b_sum'], kp['K18_b_sum']-kp['K18_a_sum'], kp['K18_a_sum']*100.0 / kp['K18_b_sum'] if  kp['K18_b_sum'] > 0 else 100.0]
                    rnc_kpi.append(l)
                kpi_list = KPI.objects.filter(date__range=(selected_date, selected_date+timedelta(days=1)), K18_b__gt=0).extra(select={'rate':'K18_a*100.0 / K18_b','all':'K18_b', 'part':'K18_a'}, where=['K18_b - K18_a >= 2']).order_by('rate')
                title = 'IRAT HO Success Rate'
                column_headers = ['Cell Name', 'RNC ID', 'Date', 'IRAT HO Success', 'IRAT HO Request', 'IRAT Failure', 'IRAT HO Success Rate']
            elif ratetype == 'hdrab':
                rnc_kpi_list = KPI.objects.filter(date__range=(selected_date, selected_date+timedelta(days=1))).values('ucell__rnc_id', 'date').annotate(K25_a_sum=Sum('K25_a'), K25_b_sum=Sum('K25_b'))
                for kp in rnc_kpi_list:
                    l = [kp['ucell__rnc_id'], kp['date'], kp['K25_a_sum'], kp['K25_b_sum'], kp['K25_b_sum']-kp['K25_a_sum'], kp['K25_a_sum']*100.0 / kp['K25_b_sum'] if  kp['K25_b_sum'] > 0 else 100.0]
                    rnc_kpi.append(l)
                kpi_list = KPI.objects.filter(date__range=(selected_date, selected_date+timedelta(days=1)), K25_b__gt=0).extra(select={'rate':'K25_a*100.0 / K25_b','all':'K25_b', 'part':'K25_a'}, where=['K25_b - K25_a >= 50']).order_by('rate')
                title = 'HSDPA Rab EST Success Rate'
                column_headers = ['Cell Name', 'RNC ID', 'Date', 'HSDPA Rab EST Ss', 'HSDPA Rab EST Att', 'HSDPA Rab Failure', 'RAB EST SRate(HSDPA)']
            elif ratetype == 'hurab':
                rnc_kpi_list = KPI.objects.filter(date__range=(selected_date, selected_date+timedelta(days=1))).values('ucell__rnc_id', 'date').annotate(K30_a_sum=Sum('K30_a'), K30_b_sum=Sum('K30_b'))
                for kp in rnc_kpi_list:
                    l = [kp['ucell__rnc_id'], kp['date'], kp['K30_a_sum'], kp['K30_b_sum'], kp['K30_b_sum']-kp['K30_a_sum'], kp['K30_a_sum']*100.0 / kp['K30_b_sum'] if  kp['K30_b_sum'] > 0 else 100.0]
                    rnc_kpi.append(l)
                kpi_list = KPI.objects.filter(date__range=(selected_date, selected_date+timedelta(days=1)), K30_b__gt=0).extra(select={'rate':'K30_a*100.0 / K30_b','all':'K30_b', 'part':'K30_a'}, where=['K30_b - K30_a >= 50']).order_by('rate')
                title = 'HSUPA Rab EST Success Rate'
                column_headers = ['Cell Name', 'RNC ID', 'Date', 'EUL Rab EST Ss', 'EUL Rab EST Att', 'HSUPA Rab Failure', 'RAB EST SRate (HSUPA)']
            elif ratetype == 'rrc':
                rnc_kpi_list = KPI.objects.filter(date__range=(selected_date, selected_date+timedelta(days=1))).values('ucell__rnc_id', 'date').annotate(K08_a_sum=Sum('K08_a'), K08_b_sum=Sum('K08_b'))
                for kp in rnc_kpi_list:
                    l = [kp['ucell__rnc_id'], kp['date'], kp['K08_a_sum'], kp['K08_b_sum'], kp['K08_b_sum']-kp['K08_a_sum'], kp['K08_a_sum']*100.0 / kp['K08_b_sum'] if  kp['K08_b_sum'] > 0 else 100.0]
                    rnc_kpi.append(l)
                kpi_list = KPI.objects.filter(date__range=(selected_date, selected_date+timedelta(days=1)), K08_b__gt=0).extra(select={'rate':'K08_a*100.0 / K08_b','all':'K08_b', 'part':'K08_a'}, where=['K08_b - K08_a >= 3']).order_by('rate')
                title = 'RRC Setup Success Rate'
                column_headers = ['Cell Name', 'RNC ID', 'Date', 'RRC Conn SS', 'RRC Conn Att', 'RRC Conn Failure', 'RRC Setup SRate'] 
            else: # 404
                return render_to_response('404.html') 
    return render_to_response('worst_cells.html',  {'kpi_list':kpi_list, 'titleMsg':title, 'ColumnsHeader':column_headers, 'rnc_kpi':rnc_kpi, 'form':dateform}, RequestContext(request))

from django.utils import simplejson
def loadExtraData(request, cellname, data_id):

    if Cell.objects.filter(cell_name=cellname).exists():
        
        sEcho = int(request.GET.get('sEcho',0))
	    # cols = int(request.GET.get('iColumns',0)) 
        my_cell = Cell.objects.get(cell_name=cellname)
        edate_tmp = datetime.strptime(request.GET.get('edate', date.today()), "%m/%d/%Y")#date.today() + timedelta(days=1))
        sdate_tmp = datetime.strptime(request.GET.get('sdate', date.today()), "%m/%d/%Y")#edate - timedelta(days=10))
        # print sdate_tmp, edate_tmp
        if edate_tmp - sdate_tmp < timedelta (days = 1):
            temp = edate_tmp
            edate_tmp = sdate_tmp
            sdate_tmp = temp
        sdate = sdate_tmp.strftime("%Y-%m-%d")
        edate = (edate_tmp + timedelta (days = 1)).strftime("%Y-%m-%d") 
        aaData = []
        iTotalRecords = iTotalDisplayRecords = 0
        if data_id == '1':
            kset = my_cell.kpi_set.filter(date__range=(sdate, edate)).order_by('date')
            if kset.count() > 0:
                for row in kset:
                    l_dc = [cellname, row.date.strftime('%Y-%m-%d %H:%M:%S'), row.K26_a, row.K26_b, prettyfloat(row.K26_a * 100.0 / row.K26_b if row.K26_b > 0 else 0), 
                                  row.K25_a, row.K25_b, prettyfloat(row.K25_a * 100.0 / row.K25_b if row.K25_b > 0 else 100.0), 
                                  prettyfloat(row.K22_ucell), prettyfloat(row.K23), prettyfloat(row.K24), prettyfloat(row.K34_ucell)]
                    aaData.append(l_dc)
                
                sum_columns = my_cell.kpi_set.filter(date__range=(sdate, edate)).aggregate(SK26_a=Sum('K26_a'), SK26_b=Sum('K26_b'), 
                                                 SK25_a=Sum('K25_a'), SK25_b=Sum('K25_b'), SK22_ucell=Sum('K22_ucell'), SK23=Sum('K23'),
                                                 SK24=Sum('K24'), SK34_ucell=Sum('K34_ucell'))
                hsdpa_total = [cellname,'total', sum_columns['SK26_a'], sum_columns['SK26_b'], prettyfloat(sum_columns['SK26_a'] * 100.0 / sum_columns['SK26_b'] if sum_columns['SK26_b'] > 0 else 0),
                                     sum_columns['SK25_a'], sum_columns['SK25_b'], prettyfloat(sum_columns['SK25_a'] * 100.0 / sum_columns['SK25_b'] if sum_columns['SK25_b'] > 0 else 100.0),
                                    prettyfloat(sum_columns['SK22_ucell']), prettyfloat(sum_columns['SK23']), prettyfloat(sum_columns['SK24']), prettyfloat(sum_columns['SK34_ucell'])]
                aaData.append(hsdpa_total)
                iTotalRecords = iTotalDisplayRecords =  kset.count() + 1

        elif data_id == '2':

            kset = my_cell.kpi_set.filter(date__range=(sdate, edate)).order_by('date')
            if kset.count() > 0:
                for row in kset:
                    l_dc = [cellname, row.date.strftime('%Y-%m-%d %H:%M:%S'), row.K31_a, row.K31_b, prettyfloat(row.K31_a * 100.0 / row.K31_b if row.K31_b > 0 else 0), 
                                  row.K30_a, row.K30_b, prettyfloat(row.K30_a * 100.0 / row.K30_b if row.K30_b > 0 else 100), 
                                  prettyfloat(row.K27), prettyfloat(row.K28), prettyfloat(row.K29), prettyfloat(row.K33_ucell)]
                    aaData.append(l_dc)
                
                sum_columns = my_cell.kpi_set.filter(date__range=(sdate, edate)).aggregate(SK31_a=Sum('K31_a'), SK31_b=Sum('K31_b'), 
                                                 SK30_a=Sum('K30_a'), SK30_b=Sum('K30_b'), SK27=Sum('K27'), SK28=Sum('K28'),
                                                 SK29=Sum('K29'), SK33_ucell=Sum('K33_ucell'))
                hsupa_total = [cellname,'total', sum_columns['SK31_a'], sum_columns['SK31_b'], prettyfloat(sum_columns['SK31_a'] * 100.0 / sum_columns['SK31_b'] if sum_columns['SK31_b'] > 0 else 0),
                                     sum_columns['SK30_a'], sum_columns['SK30_b'], prettyfloat(sum_columns['SK30_a'] * 100.0 / sum_columns['SK30_b'] if sum_columns['SK30_b'] > 0 else 100),
                                     prettyfloat(sum_columns['SK27']), prettyfloat(sum_columns['SK28']), prettyfloat(sum_columns['SK29']), prettyfloat(sum_columns['SK33_ucell'])]
                aaData.append(hsupa_total)
                iTotalRecords = iTotalDisplayRecords =  kset.count() + 1
        elif data_id == '3':
            kset = my_cell.kpi_set.filter(date__range=(sdate, edate)).order_by('date')
            if kset.count() > 0:
                for row in kset:
                    l_dc = [cellname, row.date.strftime('%Y-%m-%d %H:%M:%S'), row.K08_a, row.K08_b, prettyfloat(row.K08_a * 100.0 / row.K08_b if row.K08_b > 0 else 100), 
                                  row.K09_a, row.K09_b, prettyfloat(row.K09_a * 100.0 / row.K09_b if row.K09_b > 0 else 100), 
                                  row.K13_1a, row.K13_1b, row.K14_1a, row.K14_1b]
                    aaData.append(l_dc)
                
                sum_columns = my_cell.kpi_set.filter(date__range=(sdate, edate)).aggregate(SK08_a=Sum('K08_a'), SK08_b=Sum('K08_b'), 
                                                 SK09_a=Sum('K09_a'), SK09_b=Sum('K09_b'), SK13_1a=Sum('K13_1a'), SK13_1b=Sum('K13_1b'),
                                                 SK14_1a=Sum('K14_1a'), SK14_1b=Sum('K14_1b'))
                rrc_total = [cellname,'total', sum_columns['SK08_a'], sum_columns['SK08_b'], prettyfloat(sum_columns['SK08_a'] * 100.0 / sum_columns['SK08_b'] if sum_columns['SK08_b'] > 0 else 100),
                                     sum_columns['SK09_a'], sum_columns['SK09_b'], prettyfloat(sum_columns['SK09_a'] * 100.0 / sum_columns['SK09_b'] if sum_columns['SK09_b'] > 0 else 100),
                                     sum_columns['SK13_1a'], sum_columns['SK13_1b'], sum_columns['SK14_1a'], sum_columns['SK14_1b']]
                aaData.append(rrc_total)
                iTotalRecords = iTotalDisplayRecords =  kset.count() + 1
        elif data_id == '4':
            kset = my_cell.kpi_set.filter(date__range=(sdate, edate)).order_by('date')
            if kset.count() > 0:
                for row in kset:
                    l_dc = [cellname, row.date.strftime('%Y-%m-%d %H:%M:%S'), row.K13_2a, row.K13_2b, prettyfloat(row.K13_2a * 100.0 / row.K13_2b if row.K13_2b > 0 else 100), 
                                  row.K12_a, row.K12_b, prettyfloat(row.K12_a * 100.0 / row.K12_b if row.K12_b > 0 else 100), 
                                  row.K10_a, row.K10_b, row.K11_a, row.K11_b]
                    aaData.append(l_dc)
                
                sum_columns = my_cell.kpi_set.filter(date__range=(sdate, edate)).aggregate(SK13_2a=Sum('K13_2a'), SK13_2b=Sum('K13_2b'), 
                                                 SK12_a=Sum('K12_a'), SK12_b=Sum('K12_b'), SK10_a=Sum('K10_a'), SK10_b=Sum('K10_b'),
                                                 SK11_a=Sum('K11_a'), SK11_b=Sum('K11_b'))
                rab_total = [cellname,'total', sum_columns['SK13_2a'], sum_columns['SK13_2b'], prettyfloat(sum_columns['SK13_2a'] * 100.0 / sum_columns['SK13_2b'] if sum_columns['SK13_2b'] > 0 else 100),
                                     sum_columns['SK12_a'], sum_columns['SK12_b'], prettyfloat(sum_columns['SK12_a'] * 100.0 / sum_columns['SK12_b'] if sum_columns['SK12_b'] > 0 else 100),
                                     sum_columns['SK10_a'], sum_columns['SK10_b'], sum_columns['SK11_a'], sum_columns['SK11_b']]
                aaData.append(rab_total)
                iTotalRecords = iTotalDisplayRecords =  kset.count() + 1
        else:
            None
        response_dict = {}
        response_dict.update({'aaData':aaData})
        response_dict.update({'sEcho': sEcho, 'iTotalRecords': iTotalRecords, 'iTotalDisplayRecords':iTotalDisplayRecords})
        response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    else:
        response = HttpResponse(simplejson.dumps({"success": "false"}))
    return response


def summary_kpi(request, rnc_kpi_list, dateform):
    title = 'Summary by RNC'
    rnc_kpi = []
    sum_cols_keys = ['K19_a_sum', 'K19_b_sum', 'K18_a_sum', 'K18_b_sum', 'K13_2a_sum', 'K13_2b_sum',
                    'K12_a_sum', 'K12_b_sum', 'K25_a_sum', 'K25_b_sum', 'K30_a_sum', 'K30_b_sum', 
                    'K08_a_sum', 'K08_b_sum']
    # rnc_total_list_init = 
    rnc_sum_dict = {}

    for kp in rnc_kpi_list:
        # irat failure
        irat_ft = kp['K18_b_sum']-kp['K18_a_sum']
        # cs rab failure
        cs_rab_ft = kp['K13_2b_sum']-kp['K13_2a_sum']
        # ps rab: ps = hsdpa + r99 + elu
        ps_rab_a = kp['K25_a_sum'] + kp['K12_a_sum'] + kp['K30_a_sum'] 
        ps_rab_b = kp['K25_b_sum'] + kp['K12_b_sum'] + kp['K30_b_sum']
        ps_rab_ft = ps_rab_b - ps_rab_a
        # rrc failure
        rrc_ft = kp['K08_b_sum'] - kp['K08_a_sum']
        
        l = [kp['ucell__rnc_id'], kp['date'], kp['K19_a_sum'], prettyfloat(kp['K19_a_sum']*100.0 / kp['K19_b_sum'] if  kp['K19_b_sum'] > 0 else 0), # dcr
            irat_ft, prettyfloat(kp['K18_a_sum']*100.0 / kp['K18_b_sum'] if  kp['K18_b_sum'] > 0 else 100.0), # irat
            cs_rab_ft, prettyfloat(kp['K13_2a_sum']*100.0 / kp['K13_2b_sum'] if  kp['K13_2b_sum'] > 0 else 100.0), # cs rab
            ps_rab_ft, prettyfloat(ps_rab_a *100.0 / ps_rab_b if  ps_rab_b > 0 else 100.0), # ps rab
            rrc_ft, prettyfloat(kp['K08_a_sum']*100.0 / kp['K08_b_sum'] if  kp['K08_b_sum'] > 0 else 100.0)] # rrc service
        rnc_kpi.append(l)

        if kp['date'] not in rnc_sum_dict.keys():        
            rnc_sum_dict[kp['date']] = [0 for i in range(len(sum_cols_keys))]
        i = 0
        for k in sum_cols_keys:
            rnc_sum_dict[kp['date']][i] += kp[k]
            i += 1
    # print idates

    for date_key in rnc_sum_dict.keys():
        irat_ft = rnc_sum_dict[date_key][3] - rnc_sum_dict[date_key][2]
        cs_rab_ft = rnc_sum_dict[date_key][5] - rnc_sum_dict[date_key][4]
        ps_rab_a = rnc_sum_dict[date_key][6] + rnc_sum_dict[date_key][8] + rnc_sum_dict[date_key][10]
        ps_rab_b = rnc_sum_dict[date_key][7] + rnc_sum_dict[date_key][9] + rnc_sum_dict[date_key][11]
        ps_rab_ft = ps_rab_b - ps_rab_a
        rrc_ft = rnc_sum_dict[date_key][13] - rnc_sum_dict[date_key][12]
        rnc_kpi.append(['Network', date_key, rnc_sum_dict[date_key][0], prettyfloat(rnc_sum_dict[date_key][0] * 100.0 / rnc_sum_dict[date_key][1] if rnc_sum_dict[date_key][1] > 0 else 0), # dcr
                        irat_ft, prettyfloat(rnc_sum_dict[date_key][2] * 100.0 / rnc_sum_dict[date_key][3] if rnc_sum_dict[date_key][3] > 0 else 100.0), # irat
                        cs_rab_ft, prettyfloat(rnc_sum_dict[date_key][4] * 100.0 / rnc_sum_dict[date_key][5] if rnc_sum_dict[date_key][5] > 0 else 100.0), # cs rab
                        ps_rab_ft, prettyfloat(ps_rab_a * 100.0 / ps_rab_b if ps_rab_b > 0 else 100.0), # ps rab
                        rrc_ft, prettyfloat(rnc_sum_dict[date_key][12] * 100.0 / rnc_sum_dict[date_key][13] if rnc_sum_dict[date_key][13] > 0 else 100.0)]) # rrc
    title = 'Summary by RNC'
    column_headers = ['RNC ID', 'Date', 'DCT', 'DCR', 
                        'IRAT FT', 'IRAT SRate',
                        'CS Rab FT', 'CS Rab SRate', 
                        'PS Rab FT', 'PS Rab SRate',
                        'RRC FT', 'RRC SRate']
    return render_to_response('summary.html',  {'titleMsg':title, 'cheads':column_headers, 'rnc_kpi':rnc_kpi, 'form':dateform}, RequestContext(request))
    
def summary_changedate(request):
    if request.method == 'POST':
        dateform = DateSelectForm(request.POST) # A form bound to the POST data
        if dateform.is_valid():
            selected_date = dateform.cleaned_data['selectedDate']
            rnc_kpi_list = KPI.objects.filter(date__range=(selected_date, selected_date+timedelta(days=1))).values('ucell__rnc_id', 'date').annotate(K19_a_sum=Sum('K19_a'), K19_b_sum=Sum('K19_b'), # dcr 
                                                                                K18_a_sum=Sum('K18_a'), K18_b_sum=Sum('K18_b'), # irat
                                                                                K13_2a_sum=Sum('K13_2a'), K13_2b_sum=Sum('K13_2b'), # csrab
                                                                                K12_a_sum=Sum('K12_a'), K12_b_sum=Sum('K12_b'), # ps r99 rab
                                                                                K25_a_sum=Sum('K25_a'), K25_b_sum=Sum('K25_b'), # hd rab
                                                                                K30_a_sum=Sum('K30_a'), K30_b_sum=Sum('K30_b'), # elu rab
                                                                                K08_a_sum=Sum('K08_a'), K08_b_sum=Sum('K08_b')) # rrc service
            return summary_kpi(request, rnc_kpi_list, dateform)

def summary(request):
    dateform = DateSelectForm()
    rnc_kpi_list = KPI.objects.values('ucell__rnc_id', 'date').annotate(K19_a_sum=Sum('K19_a'), K19_b_sum=Sum('K19_b'), # dcr 
                                                                        K18_a_sum=Sum('K18_a'), K18_b_sum=Sum('K18_b'), # irat
                                                                        K13_2a_sum=Sum('K13_2a'), K13_2b_sum=Sum('K13_2b'), # csrab
                                                                        K12_a_sum=Sum('K12_a'), K12_b_sum=Sum('K12_b'), # ps r99 rab
                                                                        K25_a_sum=Sum('K25_a'), K25_b_sum=Sum('K25_b'), # hd rab
                                                                        K30_a_sum=Sum('K30_a'), K30_b_sum=Sum('K30_b'), # elu rab
                                                                        K08_a_sum=Sum('K08_a'), K08_b_sum=Sum('K08_b') # rrc service
                                                                        ).order_by('-date')[:8]
    return summary_kpi(request, rnc_kpi_list, dateform)
