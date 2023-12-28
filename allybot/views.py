from django.shortcuts import render



def index (request):
   
    # user_input = "hi this side mohit "
    # ai_response = ask_openai(user_input)
    # print(ai_response)
    return render(request,'index.html')

