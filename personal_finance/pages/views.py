from django.shortcuts import render

def login_view(request):
    return render(request, 'pages/login.html')

def dashboard_view(request):
    return render(request, 'pages/dashboard.html')