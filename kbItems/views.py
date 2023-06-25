from django.shortcuts import render
from django.http import JsonResponse
import model.Client as Client

def kbItems(request):
    return render(request, 'kbItemsHome.html')
def addKBItem(request): 
    if request.method == 'POST': 
        userInput = request.POST.get('urlInput')
        client = Client.Client("example1")
        client.addURI(str(userInput))
        response = userInput
        return JsonResponse({'response': response})
    return render(request, 'addDocument.html')

def queryItems(request): 
    if request.method == 'POST':
        userInput = request.POST.get('urlInput')
        client = Client.Client("example1")
        matchedDocs = client.queryDocuments(userInput)
        closestMatches = [docs.metadata['uri'] for docs in matchedDocs]
        # client.vectorManager.emptyIndex("example1")
        return JsonResponse({'response': closestMatches})
    

    return render(request, 'queryDocument.html')
