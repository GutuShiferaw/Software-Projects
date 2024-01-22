from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home/')
        else:
            # Invalid login details provided
            print("Invalid login details")
            return render(request, 'login.html', {'error': 'Invalid login details'})
    else:
        return render(request, 'login.html')
