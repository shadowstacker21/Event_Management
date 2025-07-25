from django.shortcuts import render,redirect
from tasks.forms import EventForm,CategoryForm
from tasks.models import Event,Category
from django.db.models import Q,Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from users.views import is_admin
# Create your views here.
def is_manager(user):
   return user.groups.filter(name='Organizer').exists()

def is_user(user):
   return user.groups.filter(name='User').exists()

user_passes_test(is_manager,login_url='no-permission')
def view(request):
    type = request.GET.get('type', 'all')
    search_query = request.GET.get('q', '')
    
    counts = Event.objects.aggregate(
        total=Count('id'),
        up_coming=Count('id', filter=Q(status="upcoming")),
        on_going=Count('id', filter=Q(status="ongoing")),
        completed=Count('id', filter=Q(status="completed"))
    )

    query = Event.objects.select_related('category').prefetch_related('participant')
    upcoming_events = Event.objects.filter(status='upcoming').order_by('date') 
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
         'upcoming_events': upcoming_events,
    }


    return render(request, 'dashboard/dashboard.html', context)
   
    
user_passes_test(is_user,login_url='no-permission')
def user_view(request):
    
    counts = Event.objects.aggregate(
        total=Count('id'),
        up_coming=Count('id', filter=Q(status="upcoming")),
        on_going=Count('id', filter=Q(status="ongoing")),
        completed=Count('id', filter=Q(status="completed"))
    )

    query = Event.objects.select_related('category').prefetch_related('participant')
    upcoming_events = Event.objects.filter(status='upcoming').order_by('date') 
    
    tasks = query

    context = {
        'tasks': tasks,
        'counts': counts,
         'upcoming_events': upcoming_events,
    }

   
    return render(request, 'dashboard/user_dashboard.html', context)    


def button(request):
    type=request.GET.get('type')
    tasks=Event.objects.select_related('category').prefetch_related('participant')
    context={
        'tasks':tasks,
        
    }  
    if type=='event' :
     return render(request,'event_list.html',context)
    
    if type=='participant' :
     rows = []
     for task in tasks:
       for participant in task.participant.all():
        rows.append({
            'participant': participant,
            'task_name': task.name
        })

     return render(request,'show_participant.html',{'rows':rows})
    
    if type=='category' :
     return render(request,'show_category.html',context)

def add_event(request):
    if request.method == "POST":
        event_form = EventForm(request.POST,request.FILES, prefix='event')
      
        category_form = CategoryForm(request.POST, prefix='category')
        
        if event_form.is_valid()  and category_form.is_valid():
            category = category_form.save()
            event = event_form.save(commit=False)
            event.category = category
            event.save()
            
            
            messages.success(request, "Event Created Successfully")
            return redirect('admin-dashboard')
    else:
        event_form = EventForm(prefix='event')
       
        category_form = CategoryForm(prefix='category')
    
    context = {
        "event_form": event_form,
       
        "category_form": category_form
    }
    return render(request, "show_task.html", context)


def update_event(request,id):
   event=Event.objects.get(id=id)
  
   category=event.category

   if request.method == "POST":
      event_form=EventForm(request.POST,instance=event,prefix='event')
      
      category_form=CategoryForm(request.POST,instance=category,prefix='category')

      if event_form.is_valid() and  category_form.is_valid():
            category = category_form.save()
            event = event_form.save(commit=False)
            event.category = category
            event.save()
           
             
            messages.success(request, "Event Updated Successfully")
            return redirect('update-event',id=event.id)

   else:
        event_form = EventForm(instance=event,prefix='event')
       
        category_form = CategoryForm(instance=category,prefix='category')
    
   context = {
        "event_form": event_form,
       
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

@login_required
def event_details(request,event_id):
    event = Event.objects.get(id=event_id)
    status_choices = Event.STATUS_CHOICES
    if request.method == 'POST':
        selected_status = request.POST.get('event_status')
        event.status = selected_status
        event.save()
        return redirect('event-details',event.id)
    return render(request,'event_details.html',{'event':event,'status_choices':status_choices})


@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('admin-dashboard')
    elif is_user(request.user):
        return redirect("user-dashboard")
    elif is_admin(request.user):
        return redirect('admin')
    return redirect('no-permission')

@login_required
def user_details(request,event_id):
    event = Event.objects.get(id=event_id)
    return render(request,'rsvp.html',{'event':event})

@login_required
def rsvp_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        if request.user not in event.participant.all():
            event.participant.add(request.user)
            messages.success(request, 'You have successfully joined this event!')
        else:
            messages.info(request, 'You have already joined this event.')
    return redirect('user-dashboard')

# def change_status(request,event_id):
#     if request.method == 'POST':
