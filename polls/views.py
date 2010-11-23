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
	        row[5:] = [s if s!='' else '0' for s in row[5:]]
	        if last_cell_name != cn:
	           # new cell
	           if last_cell_name != '':
	              # add to db except the first time
	              print 'push db'
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
	        print 'sum data'
	        print hdict
	        for k in header:
	            if i > 4:
	                 hdict[k] += float(row[i])
	            i += 1

    except csv.Error, e:
        # render_to_response('UploadError.html', {'message':'You need to specify a csv file'})
	    return False
    print 'push db'
    print hdict
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

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if (False == handle_uploaded_file(request.FILES['file'])):
	            # !!!not safe!!!
	            return render_to_response('UploadError.html', {'message':'You need to specify a csv file'})
            return HttpResponseRedirect('/admin/')
    else:
	    form = UploadFileForm()
    return render_to_response(
        "admin/upload.html",
        {'form': form},
        RequestContext(request),
    )

# report = staff_member_required(upload)
from pyofc2  import * 
import time
from django.core.exceptions import ObjectDoesNotExist
def chart_by_id(request, cellname, chart_id):
    # print chart_id
    my_cell = Cell.objects.get(cell_name=cellname)
    t = title(text=my_cell.cell_name)
    chart = open_flash_chart()
    chart.title = t
    b = bar()
    y = y_axis()
    y.min, y.max, y.steps = 0, 1, 0.1
    chart.y_axis = y
    
    x = x_axis()
    xlbls = x_axis_labels(steps=1, rotate='45', colour='#FF0000', size=16)
    lbls = []
    for item in my_cell.kpi_set.all():
	    lbls.append(item.date.strftime('%Y-%m-%d %H:%M:%S'))
    
    xlbls.labels = lbls 
    x.labels = xlbls
    chart.x_axis = x
    
    # l.halo_size = 10
    b.width = 4
    # l.dot_size = 4
    b.tip = 'value: #val#'
    b.text = 'AMR Traffic'
    b.values = [item.K01 for item in my_cell.kpi_set.all()]
    chart.add_element(b)

    return HttpResponse(chart.render())

def chart_data(request, cellname):

    # my_cell = Cell.objects.get(pk=1)
    my_cell = Cell.objects.get(cell_name=cellname)
    # my_cell = cellname
    t = title(text=my_cell.cell_name)
    chart = open_flash_chart()
    chart.title = t
    y = y_axis()
    y.min, y.max, y.steps = 0, 50, 5
    chart.y_axis = y
    x = x_axis()
    lbl = labels(labels=['AMR Traffic', 'VP Traffic', 'CS Traffic', 'PS Uplink throughout', 'PS Downlink throughout'])
    x.labels=lbl
    chart.x_axis = x
    # chart.bg_colour = '#121212'
    line_colors = ["#6F0073", "#3133C0", "#089C14", "#F0DFA1", "#DFC329"]
    ix = 0
    for acell in my_cell.kpi_set.all():
	    # print acell.ucell.cell_name, acell.date, acell.K01
        l = line_hollow()
        # l.halo_size = 10
        l.width = 4
        # l.dot_size = 4
        l.tip = 'value: #val#'
        l.text = 'purge line'
        l.colour = line_colors[ix]
        l.values = [acell.K01,acell.K02,acell.K03, acell.K04, acell.K05]
        chart.add_element(l)
        # b1 = bar_filled(colour='#E2D66A')
        # b1.values = [acell.K01,acell.K02,acell.K03, acell.K04, acell.K05]
        # b1.outline_colour = '#577261'   
        # chart.add_element(b1)
        ix += 1
    return HttpResponse(chart.render())

def worst_cells(request, ratetype):
    # print ratetype
    if ratetype == 'dcr':
	    kpi_list = KPI.objects.filter(K19_b__gt=0, K19_a__gt=0).extra(select={'rate':'K19_a*1.0 / K19_b', 'all':'K19_b', 'part':'K19_a'}).order_by('-rate')[:20]
	    title ='Drop Call Rate'
	    column_headers = ['Cell Name', 'Date', 'System Release', 'All Release', 'Drop Call Rate']
    elif ratetype == 'irat_ho':
	    kpi_list = KPI.objects.filter(K18_b__gt=0).extra(select={'rate':'K18_a*1.0 / K18_b','all':'K18_b', 'part':'K18_a'}).order_by('rate')[:20]
	    title = 'IRAT HO Success Rate'
	    column_headers = ['Cell Name', 'Date', 'IRAT HO Success', 'IRAT HO Request', 'IRAT HO Success Rate']
	# print kpi_list
    else: # default use dcr
	    return render_to_response('404.html')
    return render_to_response('worst_cells.html',  {'kpi_list':kpi_list, 'titleMsg':title, 'ColumnsHeader':column_headers})
	
	
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

from django.db.models import Sum
def results(request, cellname):
    # print my_cell
    # print KPI.objects.values('ucell_id').order_by().annotate(Sum('K01'), Sum('K02'))
    if Cell.objects.filter(cell_name=cellname).exists():	    
        return render_to_response('result.html', {'cell_name':cellname})
    return render_to_response('404.html')
	
class CellNameForm(forms.Form):
    cellname = forms.CharField(max_length=100)


