from django.shortcuts import render
from django.http import JsonResponse
from .models.KBitem import KBItem, TextKBItem, ImageKBItem
from .models.Query import Query

def kbItems(request):
    return render(request, 'kbItemsHome.html')


def addKBItem(request): 
    if request.method == 'POST': 
        userInput = request.POST.get('urlInput')

        if 'instagram' in userInput or 'twitter' in userInput: 
            kbItem = ImageKBItem(URI = userInput)
        else: 
            kbItem = TextKBItem(URI = userInput)

        kbItem.parseURI()
        kbItem.save()
        kbItem.createVector()
        print("allgood")
        response = [userInput]
        return render(request, 'addDocument.html', {'response': response, 'submitted': True})
    return render(request, 'addDocument.html')

def queryItems(request): 
    if request.method == 'POST':
        userInput = request.POST.get('urlInput')
        
        query = Query(userInput)
        sortedKbItems = query.getMatchedDocs()
        closestMatches = [ (docs[0].URI,docs[1]) for docs in sortedKbItems]
        # client.vectorManager.emptyIndex("example1")
        return render(request, 'QueryDocuments.html', {'response': closestMatches, 'submitted': True})
    

    return render(request, 'QueryDocuments.html')
