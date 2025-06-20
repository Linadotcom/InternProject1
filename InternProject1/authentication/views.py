from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_user(request): 
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password )
        if user is not None: 
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, ("Une erreur s'est produite lors de la connexion! Réessayez."))
            return redirect('login')
    else:
        return render(request, 'registration/login.html', {})

def signup_user(request):
    if request.method == 'POST': 
        form = UserCreationForm(request.POST)
        if form.is_valid(): 
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, ('Vous êtes maintenant inscris!'))
            return redirect('login')
    else: 
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, ("Vous avez été déconnecté! ") )
    return redirect('login')