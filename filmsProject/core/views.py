from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.

def index (request):
    return render(request, 'core/index.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'core/signup.html', {'form': form})
    