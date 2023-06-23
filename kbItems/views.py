from django.shortcuts import render
from django.http import JsonResponse
import model.Client as Client

# Create your views here.
def addKBItem(request): 
    if request.method == 'POST': 
        userInput = request.POST.get('urlInput')
        client = Client.Client("example1")
        client.addURI(str(userInput))
        response = userInput
        return JsonResponse({'response': response})
    return render(request, 'addDocument.html')
