from django.shortcuts import render

# Create your views here.

def admin_view(request, id):
    return render(request,"admin_adds/admin_adds.html")
