from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models.KBitem import KBItem, TextKBItem, ImageKBItem
from .models.Query import Query
from .thread import KBItemBackground
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from matplotlib import cm
from matplotlib.colors import rgb2hex


def sign_up(request): 
    if request.method == 'POST': 
        form = RegisterForm(request.POST)
        if form.is_valid(): 
            user = form.save() 
            login(request,user)
            return redirect('/home')

    else: 
        form = RegisterForm() 
    
    return render(request,'registration/sign_up.html', {"form": form})

@login_required(login_url="/login")
def home(request):
    return render(request, 'kbItems/home.html')

@login_required(login_url="/login")
def addKBItem(request): 
    if request.method == 'POST': 
        userInput = request.POST.get('urlInput')

        if 'instagram' in userInput or 'twitter' in userInput: 
            kbItem = ImageKBItem(URI = userInput)
        else: 
            kbItem = TextKBItem(URI = userInput)

        kbItem.userID = request.user.id
        KBItemBackground(kbItem).start()
        response = [userInput]
        return render(request, 'kbItems/addDocument.html', {'response': response, 'submitted': True})
    return render(request, 'kbItems/addDocument.html')

@login_required(login_url="/login")
def queryItems(request): 
    if request.method == 'POST':
        userInput = request.POST.get('urlInput')
        
        query = Query(userInput,request.user.id)
        sortedKbItems = query.getMatchedDocs()

        cmap = cm.get_cmap('RdYlGn')
        closestMatches = []
        for i, item in enumerate(sortedKbItems):
            color = rgb2hex(cmap((len(sortedKbItems) - i - 1) / len(sortedKbItems)))
            closestMatches.append((item[0].URI, item[1], color))

        # client.vectorManager.emptyIndex("example1")
        return render(request, 'kbItems/searchDocuments.html', {'response': closestMatches, 'submitted': True})
    

    return render(request, 'kbItems/searchDocuments.html')
