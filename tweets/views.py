import random

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

#Checks that the URL is safe. Included in settings
from django.utils.http import is_safe_url
#Imports settings, than assign ALLOWED_HOSTS down below
from django.conf import settings

from tweets.serializers import TweetSerializer
from .models import Tweet

from .forms import TweetForm

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    #return HttpResponse(f"<h1>Hello World</h1>")

    #Templates, status defaults to 200 
    return render(request, "pages/home.html", context={}, status=200)


def tweet_create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data= request.POST or None)

    if serializer.is_valid():
        serializer.save(user = request.user)
        return JsonResponse(serializer.data, status=201)
    return JsonResponse({}, status=400)


# Pure Django
def tweet_create_view_pure_django(request, *args, **kwargs):
    print("reached")
    user = request.user
    # Checks if user session is active
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)

    # TweetForm class can be initialized with data or not 
    form = TweetForm(request.POST or None)
    # Gets the value of the input field name=next
    next_url = request.POST.get("next") or None
    print('post data is', request.POST)
    #If the form is valid it saves it, otherwise returns the form
    if form.is_valid():
        
        obj = form.save(commit=False)
        obj.user = user
        #You can do other form related logic in here
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
        #And then reinitialize a new blank form
        form = TweetForm()
    return render(request, 'components/form.html', context={"form": form})

#Uses the django form, rewriting for the by-hand form
#def tweet_create_view(request, *args, **kwargs):
    # TweetForm class can be initialized with data or not 
    form = TweetForm(request.POST or None)
    print('post data is', request.POST)
    #If the form is valid it saves it, otherwise returns the form
    if form.is_valid():
        obj = form.save(commit=False)
        #You can do other form related logic in here
        obj.save()
        #And then reinitialize a new blank form
        form = TweetForm()
    return render(request, 'components/form.html', context={"form": form})

def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all() #List
    #tweets_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 122)} for x in qs] #List
    #Serialzie DMO
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list, #List
        
    }

    return JsonResponse(data)#List



def tweet_detail_view(request, tweet_id):
    """
    REST API VIEW
    Consume JS, SWIFT, Java, IOS/Android
    return json data
   """
    status = 200
    data={
        "id": tweet_id,
    }
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"] = obj.content
    except:
        data['message'] = "Not found"
        #raise Http404
        status = 404
   
    return JsonResponse(data, status=status) #json.dumps content_type='application/json
    #status is an arguement option JsonResponse has, hover over JsonResponse

    #return HttpResponse(f"Hello {tweet_id} - {obj.content}")
