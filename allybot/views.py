from django.shortcuts import render
from userauth.models import users_messages,users



def index (request):
   
    # user_input = "hi this side mohit "
    # ai_response = ask_openai(user_input)
    # print(ai_response)
    return render(request,'index.html')


def conversations(request):
    user_id = request.session.get('user_id') # gets user_id from session 
    user_data = users.objects.get(user_id=user_id) # get logined user data from the database using user_id
    user_messages = users_messages.objects.filter(user_id=user_id).order_by('-created_at')  # Assuming there's a 'created_at' field for ordering

    return render(request,"conversations.html",{'user_messages':user_messages,'user_data':user_data})


def about_us(request):
    user_id = request.session.get('user_id') # gets user_id from session 
    user_data = users.objects.get(user_id=user_id) # get logined user data from the database using user_id


    return render(request,"about_us.html",{'user_data':user_data})

def contact_us(request):
    user_id = request.session.get('user_id') # gets user_id from session 
    user_data = users.objects.get(user_id=user_id) # get logined user data from the database using user_id


    return render(request,"contact_us.html",{'user_data':user_data})

