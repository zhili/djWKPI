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
# 
# def detail(request, poll_id):
#     try:
#         p = Poll.objects.get(pk=poll_id)
#     except Poll.DoesNotExist:
#         raise Http404
#     return render_to_response('detail.html', {'poll': p},
#                                context_instance=RequestContext(request))
#  
# 
# def results(request, poll_id):
#     p = get_object_or_404(Poll, pk=poll_id)
#     return render_to_response('result.html', {'poll': p})
# 
# def vote(request, poll_id):
#     p = get_object_or_404(Poll, pk=poll_id)
#     try:
#         selected_choice = p.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#       # Redisplay the poll voting form.
#         return render_to_response('detail.html', {
#             'poll': p,
#             'error_message': "You didn't select a choice.",
#         }, context_instance=RequestContext(request))
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#       # Always return an HttpResponseRedirect after successfully dealing
#       # with POST data. This prevents data from being posted twice if a
#       # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls.views.results', args=(p.id,)))


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
	    print header
	    for row in reader:
		    if not row:
			    break
		    rid= row[0]
		    cn = row[1]
		    
		    if Cell.objects.filter(cell_name=cn).exists():
			    ucell = Cell.objects.get(cell_name=cn)
		    else:
		        ucell = Cell.objects.create(rnc_id=rid,cell_name=cn)
		    item_date = datetime.strptime(row[2], '%m/%d/%Y %I:%M:%S %p') + timedelta(hours=int(row[3]), minutes=int(row[4]))
		    # get rid of '' to in error
		    row[5:] = [s if s!='' else '0' for s in row[5:]]
		    kpi = KPI(date = item_date, K01=row[5], K02=row[6], K03=row[7], K04=row[8], K05=row[9],
		              K08_a = row[10], K08_b = row[11], K09_a = row[12], K09_b = row[13], K10_a=row[14], 
		              K10_b=row[15], K11_a=row[16], K11_b=row[17], K12_a=row[18], K12_b=row[19], K13_1a=row[20], 
		              K13_1b=row[21], K13_2a=row[22], K13_2b=row[23], K14_1a=row[24], K14_1b=row[25], K15=row[26], 
		              K16_a=row[27], K16_b=row[28], K19_a=row[29], K19_b=row[30], K20_a=row[31], K20_b=row[32], 
		              K21_a=row[33], K21_b=row[34], K22_ucell=row[35], K24=row[36], K25_a=row[37], K25_b=row[38],
		              K26_a=row[39], K26_b=row[40], K27=row[41], K29=row[42], K30_a=row[43], K30_b=row[44], 
		              K31_a=row[45], K31_b=row[46], K33_ucell=row[47], K34_ucell=row[48], K06=row[49], K28=row[50],
		              K07=row[51], K23=row[52], K17_a=row[53], K17_b=row[54], K18_a=row[55], K18_b=row[56], K32_a=row[57], K32_b=row[58])
		    ucell.kpi_set.add(kpi)
    except csv.Error, e:
	    # render_to_response('UploadError.html', {'message':'You need to specify a csv file'})
	    return False
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

def chart_data(request):

    my_cell = Cell.objects.get(pk=1)
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
        l = line()
        l.colour = line_colors[ix]
        l.values = [acell.K01,acell.K02,acell.K03, acell.K04, acell.K05]
        chart.add_element(l)
        ix += 1
    return HttpResponse(chart.render())

def worst_dcr_cells(request):
	kpi_list = KPI.objects.filter(K19_b__gt=0, K19_a__gt=0).extra(select={'dcr':'K19_a*1.0 / K19_b'}).order_by('-dcr')[:10]
	print kpi_list
	return render_to_response('worst_cells.html', {'kpi_list':kpi_list})
	
	
from django.db.models import Q

def tag_autocomplete(request):
    if request.GET.has_key('q'):
        q_str = request.GET['q']
        if len(q_str)>0:
            tags = (Cell.objects.filter(Q (rnc_id__icontains=request.GET['q']) | Q (cell_name__icontains=request.GET['q'])))[:10] 
            return HttpResponse('\n'.join(tag.cell_name for tag in tags))
    return render_to_response('search.html')
