from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from .models import Task



from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.

class CustomLoginView(LoginView):
  template_name = 'todo/login.html'
  fields = '__all__'
  redirect_authenticated_user = True
  
  def get_success_url(self):
    return reverse_lazy('tasks')

class SignUpPage(FormView):
  template_name = 'todo/register.html'
  form_class = UserCreationForm
  redirect_authenticated_user = True
  success_url = reverse_lazy('tasks')

  def form_valid(self, form) :
    user = form.save()
    if user is not None:
      login(self.request, user)
    return super(SignUpPage, self).form_valid(form)

  def get(self, *args, **kwargs):
    if self.request.user.is_authenticated:
      return redirect('tasks')
    return super(SignUpPage, self).get( *args, **kwargs) 


    

class TaskList(LoginRequiredMixin,ListView):
  model = Task
  context_object_name = 'task'

  def get_context_data(self, **kwargs):
    context =  super().get_context_data(**kwargs)
    context['task'] = context['task'].filter(user=self.request.user)
    context['count'] = context['task'].filter(complete=False).count()

    search_input = self.request.GET.get('search-area') or ''
    if search_input :
      context['task'] = context['task'].filter(
        title__startswith=search_input
      )
      context['search_input'] = search_input
    

      
    return context

  

class TaskDetail(LoginRequiredMixin,DetailView):
  model = Task
  context_object_name = 'task'
  template_name = 'todo/task_detail.html'

class TaskCreate(LoginRequiredMixin,CreateView):
  model =Task
  fields = ['title', 'description', 'complete']
  success_url = reverse_lazy('tasks')

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(TaskCreate, self).form_valid(form)
  
   

class TaskUpdate(LoginRequiredMixin,UpdateView):
  model =Task 
  fields = ['title', 'description', 'complete']
  success_url = reverse_lazy('tasks') 

class TaskDelete(LoginRequiredMixin,DeleteView):
  model = Task
  context_object_name = 'task'
  success_url = reverse_lazy('tasks')






  

  

