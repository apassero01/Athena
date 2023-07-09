from django.shortcuts import render
from django.http import JsonResponse
from .models.KBitem import KBItem, TextKBItem, ImageKBItem

def kbItems(request):
    return render(request, 'kbItemsHome.html')


def addKBItem(request): 
    if request.method == 'POST': 
        userInput = request.POST.get('urlInput')

        kbItem = ImageKBItem(URI = userInput)
        kbItem.parseURI()
        kbItem.save()

        kbItem.createVector()

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
