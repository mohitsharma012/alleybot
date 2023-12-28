from django.shortcuts import render
from userauth.models import users, users_messages

import openai
from django.conf import settings
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def dashboard(request,user_id):
    request.session['user_id'] = user_id

    data = users.objects.get(user_id=user_id)

    user_data = {
        'user_name':data.user_name,
        'user_email':data.user_email

    }
    # user_input = "hi this side mohit "
    # ai_response = ask_openai(user_input)
    # print(ai_response)


    return render(request,'dashboard.html',{'user_data':user_data})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def process_voice(request):
    if request.method == 'POST':
        transcript = request.POST.get('transcript')

        user_id = request.session.get('user_id')

        ai_response = ask_openai(user_id,transcript)
        
        store_conversation(user_id,transcript,ai_response)


        return JsonResponse({'response': ai_response})
    return JsonResponse({'message': 'Invalid request'}, status=400)




# def ask_openai(user_id,question):
#     ALLY_INTRODUCTION = ("My name is Ally, and I am an AI friend. I am here to listen, help, and provide friendly, emotionally-aware responses. ")

    

#     try:
#         conversation = users_messages.objects.get(user_id=user_id)
#         user_messages = users_messages.objects.filter(user_id=user_id).order_by('created_at')  # Assuming there's a 'created_at' field for ordering

#         conversation_history = conversation.conversation_history
       

#     except users_messages.DoesNotExist:
#         conversation_history = ""

#     openai.api_key = os.getenv('OPENAI_API_KEY')

#     prompt = ALLY_INTRODUCTION + conversation_history + "\nUser: " + question + "\nAlly:"



#     response = openai.Completion.create(
#         engine="text-davinci-003",  # Choose the appropriate model
#         prompt=prompt,
#         max_tokens=150  # Adjust as needed
#     )
#     ai_text_response = response.choices[0].text.strip()

        
#     return ai_text_response


def ask_openai(user_id, question):
    ALLY_INTRODUCTION = ("You're my human buddy, ally. Respond with emotion, respond in a fuly relaxed manner")

    user_messages = users_messages.objects.filter(user_id=user_id).order_by('created_at')  # Assuming there's a 'created_at' field for ordering

    conversation_history = "\n".join([f"User: {msg.message_text}\nAI: {msg.ai_response}" for msg in user_messages])  # Adjust according to your model fields

    openai.api_key = os.getenv('OPENAI_API_KEY')

    prompt = ALLY_INTRODUCTION + conversation_history + "\nUser: " + question + "\nAlly:"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    ai_text_response = response.choices[0].text.strip()

    return ai_text_response



def store_conversation(user_id, message, ai_response):
    # Create a new message instance for each interaction
    new_message = users_messages(user_id=user_id, message_text=message, ai_response=ai_response)
    new_message.save()

    
