from django.shortcuts import render
import json
from django.http import HttpResponse
# Create your views here.
import urllib.request


from django.shortcuts import render,redirect
from django.contrib import messages
# Create your views here.
from main_app.forms import TodoForm
from main_app.models import TodoModel



def index(request):
    data = {}
    if request.method == 'POST':
        city = request.POST['city']
        try :
            source = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=b035d121ff439c272df931cfce3dbeec').read()
        except :
            data = {'error' : 'Not found '+"'"+city+"'"+' city!'}
            return render(request,'main_app/index.html',data)

        else:
            list_of_data = source.decode('utf-8')
            list_of_data = json.loads(list_of_data)
            data = {
                "city_name":str(list_of_data['name']),
                "country_code":(str(list_of_data['sys']['country']).lower()),
                "coordinate":str(list_of_data['coord']['lon'])+' | '+str(list_of_data['coord']['lat']),
                "temp":str(round(list_of_data['main']['temp'] - 273.15,2))+'°C',
                "pressure":str(list_of_data['main']['pressure'])+' hpa',
                "humidity":str(list_of_data['main']['humidity'])+'%',
                }
    return render(request,'main_app/index.html',data)


def to_do_list(request):
    items_list = TodoModel.objects.order_by('-date')
    if request.method == 'POST':
        form_ = TodoForm(request.POST)
        if form_.is_valid():
            form_.save()
            return redirect('to_do_list')
    form_ = TodoForm()
    page = {
        'form_':form_,
        'list':items_list,
        'title':'TODO LIST',
    }
    return render(request,'todolist/todolist.html',page)

def remove_item(request,item_id):
    # print('test remove!')
    item = TodoModel.objects.get(id=item_id)
    item.delete()
    messages.info(request,"Item removed!")      # send to template
    return redirect('to_do_list')
