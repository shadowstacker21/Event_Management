from django.shortcuts import render,redirect
from tasks.forms import EventForm,CategoryForm
from tasks.models import Event,Category
from django.db.models import Q,Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from users.views import is_admin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.base import ContextMixin
from django.views.generic import DeleteView,ListView,UpdateView
from django.views import View
# Create your views here.
def is_manager(user):
   return user.groups.filter(name='Organizer').exists()

def is_participant(user):
   return user.groups.filter(name='Participant').exists()


@method_decorator(user_passes_test(is_manager,login_url='no-permission'),name='dispatch')
class ManagerDashboardView(ListView):
    model = Event
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        type = self.request.GET.get('type','all')
        search_query = self.request.GET.get('q', '')
        queryset = Event.objects.select_related('category').prefetch_related('participant')

        if type == 'up_coming':
            queryset = queryset.filter(status='upcoming')
        elif type == 'on_going':
            queryset = queryset.filter(status='ongoing')
        elif type == 'completed':
            queryset = queryset.filter(status='completed')

        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)|
                Q(category__name__icontains=search_query)
            )

        return queryset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['role'] = 'Organizer'
        context['counts'] = Event.objects.aggregate(
                            total=Count('id'),
                            up_coming=Count('id', filter=Q(status="upcoming")),
                            on_going=Count('id', filter=Q(status="ongoing")),
                            completed=Count('id', filter=Q(status="completed"))
                        )
        
        context['upcoming_events'] = Event.objects.filter(status='upcoming').order_by('date')

        return context

@method_decorator(user_passes_test(is_participant,login_url='no-permission'),name='dispatch')
class UserView(ListView):
    model = Event
    template_name =  'dashboard/user_dashboard.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Event.objects.select_related('category').prefetch_related('participant')
        return queryset
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['role'] = 'Participant'
       context['counts'] = Event.objects.aggregate(
                    total=Count('id'),
                    up_coming=Count('id', filter=Q(status="upcoming")),
                    on_going=Count('id', filter=Q(status="ongoing")),
                    completed=Count('id', filter=Q(status="completed"))
                )
       context['upcoming_events'] = Event.objects.filter(status='upcoming').order_by('date')
       return context

"""
user_passes_test(is_participant,login_url='no-permission')
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
"""    

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


class AddTask(ContextMixin,PermissionRequiredMixin,LoginRequiredMixin,View):
    permission_required = 'tasks.add_event'
    login_url = 'sign-in'
    template_name = "show_task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_form'] = kwargs.get('event_form',EventForm(prefix='event'))
        context['category_form'] = kwargs.get('category_form',CategoryForm( prefix='category'))
        return context
    
    def get(self,request,*args, **kwargs):
        context = self.get_context_data()
        return render(request,self.template_name,context)
    
    def post(self,request,*args, **kwargs):
        event_form = EventForm(request.POST,request.FILES,prefix='event')
        category_form = CategoryForm(request.POST, prefix='category')

        if event_form.is_valid() and category_form.is_valid():
            category = category_form.save()
            event = event_form.save(commit=False)
            event.category = category
            event.save()

            messages.success(request, "Event Created Successfully")
            
            return redirect('admin-dashboard')
        context = self.get_context_data(event_form=event_form,category_form=category_form)
        return render(request, self.template_name, context)


"""
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
"""

class UpdateEventView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = "show_task.html"
    context_object_name = 'event'
    pk_url_kwarg = 'id'


    def get_form(self, form_class=None):
        form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        kwargs['prefix'] = 'event'  
        return form_class(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_form'] = self.get_form()
    
        if hasattr(self.object,'category') and self.object.category:
            context['category_form'] = CategoryForm(instance = self.object.category,prefix='category')

        else:
            context['category_form'] = CategoryForm(prefix='category')
        
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        event_form = EventForm(request.POST,request.FILES,instance = self.object,prefix='event')
        category_form = CategoryForm(request.POST,instance=getattr(self.object,'category',None),prefix='category')

        if event_form.is_valid() and category_form.is_valid():
            category = category_form.save()
            event = event_form.save(commit=False)
            event.category = category
            event.save()

            messages.success(request, "Event Updated Successfully")
            
            return redirect('admin-dashboard')   
        return redirect('admin-dashboard')

"""
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
"""    

class DeleteEventView(DeleteView):
    model = Event
    template_name = 'event_details.html'
    permission_required = "tasks.delete_event"
    login_required = "no-permission"
    success_url = reverse_lazy("admin-dashboard")
    pk_url_kwarg = 'id'
    

    def delete(self, request, *args, **kwargs):
        messages.success(self.request,"Task Delete Successfully")
        return super().delete(request, *args, **kwargs)

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
    elif is_participant(request.user):
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
