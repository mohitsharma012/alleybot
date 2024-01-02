from django.shortcuts import render
from userauth.models import users, users_messages
import openai
from django.conf import settings
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def process_voice(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id') # gets user_id from session 

        transcript = request.POST.get('transcript')


        ai_response = ask_openai(user_id,transcript)
        
        store_conversation(user_id,transcript,ai_response)


        return JsonResponse({'response': ai_response})
    return JsonResponse({'message': 'Invalid request'}, status=400)

# OpenAI API to ask questions 
def ask_openai(user_id, question):
    openai.api_key = os.getenv('OPENAI_API_KEY')


    user_messages = users_messages.objects.filter(user_id=user_id).order_by('created_at')  # Assuming there's a 'created_at' field for ordering

    conversation_history = "\n".join([f"User: {msg.message_text}\nAI: {msg.ai_response}" for msg in user_messages])  # Adjust according to your model fields


    # prompt = ALLY_INTRODUCTION + conversation_history + "\nUser: " + question + "\nAlly:"
    conversation_history = fetch_conversation_history(user_id)

    # open('path/to/your/file.txt', 'r'):
    data = open('static/intoduction_message.txt', 'r').read()



    introduction_message = {
        "role": "system",
        "content": "You're my human buddy, Ally. Respond with warmth, empathy, and friendliness. Be supportive and considerate in your responses, showing emotion and understanding, You are not an AI model "
    }
    messages = [introduction_message] + conversation_history + [{"role": "user", "content": question}]


    
    # print(messages)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        # prompt=prompt,
        temperature=1,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )


    
    # ai_text_response = response.choices[0].text.strip()
    ai_text_response = response.choices[0].message['content']

    # return ai_text_response
    return ai_text_response
    # return response.choices[0].message['content']

# function to helps new converstion in database 
def store_conversation(user_id, message, ai_response):
    # Create a new message instance for each interaction
    new_message = users_messages(user_id=user_id, message_text=message, ai_response=ai_response)
    new_message.save()

# function to get previous conversations   
def fetch_conversation_history(user_id):
    # Placeholder for fetching messages from the database
    # Replace this with your actual database query logic
    # The returned list should be in the format:
    # [{"role": "user/assistant", "content": "message text"}, ...]

    user_messages = users_messages.objects.filter(user_id=user_id).order_by('created_at')

    conversation_history = []

    for msg in user_messages:
        # Add the user's message
        conversation_history.append({"role": "user", "content": msg.message_text})

        # Add the AI's response, if it exists
        if msg.ai_response:
            conversation_history.append({"role": "assistant", "content": msg.ai_response})


    return conversation_history

# the main dahboard function 
def dashboard(request):
    user_id = request.session.get('user_id') # get user if from the session 
    data = users.objects.get(user_id=user_id) # get logined user data from the database using user_id
    user_data = {
        'user_name':data.user_name,
        'user_email':data.user_email
    }
   
    return render(request,'dashboard.html',{'user_data':user_data})
