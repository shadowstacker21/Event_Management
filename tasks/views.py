from django.shortcuts import render,redirect
from tasks.forms import EventForm,CategoryForm,ParticipantForm
from tasks.models import Event,Category,Particpant
from django.db.models import Q,Count
from django.contrib import messages

# Create your views here.
def view(request):
    type = request.GET.get('type', 'all')
    search_query = request.GET.get('q', '')

    counts = Event.objects.aggregate(
        total=Count('id'),
        up_coming=Count('id', filter=Q(status="upcoming")),
        on_going=Count('id', filter=Q(status="ongoing")),
        completed=Count('id', filter=Q(status="completed"))
    )

    query = Event.objects.select_related('category').prefetch_related('particpant')

    if type == 'up_coming':
        query = query.filter(status='upcoming')
    elif type == 'on_going':
        query = query.filter(status='ongoing')
    elif type == 'completed':
        query = query.filter(status='completed')
    elif type == 'all':
        pass

    if search_query:
        query = query.filter(
            Q(name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    tasks = query

    context = {
        'tasks': tasks,
        'counts': counts,
        'search_query': search_query,
    }

    return render(request, 'dashboard/dashboard.html', context)


def button(request):
    type=request.GET.get('type')
    tasks=Event.objects.select_related('category').prefetch_related('particpant')
    context={
        'tasks':tasks,
        
    }  
    if type=='event' :
     return render(request,'event_list.html',context)
    
    if type=='participant' :
     return render(request,'show_participant.html',context)
    
    if type=='category' :
     return render(request,'show_category.html',context)

def add_event(request):
    if request.method == "POST":
        event_form = EventForm(request.POST, prefix='event')
        participant_form = ParticipantForm(request.POST, prefix='participant')
        category_form = CategoryForm(request.POST, prefix='category')
        
        if event_form.is_valid() and participant_form.is_valid() and category_form.is_valid():
            category = category_form.save()
            event = event_form.save(commit=False)
            event.category = category
            event.save()
            participant = participant_form.save()
            event.particpant.add(participant)
            messages.success(request, "Task Created Successfully")
            return redirect('add-event')
    else:
        event_form = EventForm(prefix='event')
        participant_form = ParticipantForm(prefix='participant')
        category_form = CategoryForm(prefix='category')
    
    context = {
        "event_form": event_form,
        "participant_form": participant_form,
        "category_form": category_form
    }
    return render(request, "show_task.html", context)


def update_event(request,id):
   event=Event.objects.get(id=id)
   participant=event.particpant.first()
   category=event.category

   if request.method == "POST":
      event_form=EventForm(request.POST,instance=event,prefix='event')
      participant_form=ParticipantForm(request.POST,instance=participant,prefix='participant')
      category_form=CategoryForm(request.POST,instance=category,prefix='category')

      if event_form.is_valid() and participant_form.is_valid() and category_form.is_valid():
            category = category_form.save()
            event = event_form.save(commit=False)
            event.category = category
            event.save()
            participant = participant_form.save()
            event.particpant.set([participant]) 
            messages.success(request, "Event Updated Successfully")
            return redirect('update-event',id=event.id)

   else:
        event_form = EventForm(instance=event,prefix='event')
        participant_form = ParticipantForm(instance=participant,prefix='participant')
        category_form = CategoryForm(instance=category,prefix='category')
    
   context = {
        "event_form": event_form,
        "participant_form": participant_form,
        "category_form": category_form,
        "update":True
    }
   return render(request, "show_task.html", context) 

def delete_event(request,id):
    if request.method == 'POST':
        event=Event.objects.get(id=id)
        event.delete()
        messages.success(request,"Task Delete Successfully")
        return redirect('admin-dashboard')
    else:
        messages.error(request,"Something went wrong")
        return redirect('admin-dashboard')



   