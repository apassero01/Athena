from django.shortcuts import render

# Create your views here.
def importDocument(request): 
    return render(request, 'addDocument.html')