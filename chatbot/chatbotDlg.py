from flask import Flask, render_template, request
import requests

app = Flask(__name__)
global isNewSession
isNewSession = True

@app.route('/', methods=['GET', 'POST'])
def index():
    global isNewSession
    if request.method == 'POST':
        # Retrieve the message from the text area
        message = request.form['message']

        # Retrieve the post endpoint URL from the text field
        # endpoint_url = request.form['endpoint_url']
        endpoint_url = request.form['endpoint_url']

        # Post the message to the specified endpoint URL
        # You can use the requests library to perform this HTTP request
        response = requests.post(endpoint_url, json={'text': message, 'new_session':isNewSession})
        isNewSession = False
        botresponse = response.json()
        try:
            botmsg = botresponse['messages'][0].get('content','')
            if len(botresponse['messages']) > 1:
                botmsg2 = botresponse.get('messages','')[1].get('content','')
            else:
                botmsg2 = ''
                
        except:
            botmsg = 'Sorry, I did not understand. Can you rephrase your question?'
            botmsg2 = ''

        botmsg = botmsg.replace('<>','\n')
        botmsg2 = botmsg2.replace('<>','\n')
        
        # Append the message to the chat dialog main text area
        chat_log = f"\n\n[User]: {message}\n\n[Response]: {botmsg}\n{botmsg2}"
        # render the chat log textarea only
        return render_template('chatdata.html', chat_log=chat_log)


    # Render the chat dialog window
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
