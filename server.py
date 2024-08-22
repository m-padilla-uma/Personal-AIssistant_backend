from flask import Flask, jsonify, request, json
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
# GLOBAL VARIABLES
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

@app.route('/get-assistance', methods=['POST'])
def get_assistance():
    # Set all variables and prompt
    print(request.json)
    items = request.json.get('list')
    print(items)
    success = False
    msg = ('Here is a list of items:\n'
           + items + '\n'
           'Read each item carefully and come up with a step-by-step plan to tackle each on of them individually. Be '
           'concise and direct and have any personal nuances inferred from the list items into account.\n'
           'These items do not necessarily correlate, so make a new plan for each one of them!\n'
           'Keep in mind that you must use your internet access (or most updated information) to search for '
           'alternatives ideas or propositions to fulfill each item.\n'
           'Any lists you make have to be create using the <l> or <ul> tag with the corresponding <li> entries as '
           'items.\n'
           'Return the response in a format that can be inserted into an <textarea [innerHTML]> element that keeps the styling you '
           'have chosen to the response, that is, italics, links or other designs you may have used. With links, make '
           'sure the user can click them from the text area window and enter the link on a new tab. Keep in mind'
           'adding extra spacing between paragraphs, sections and divs properly.\n'
           'As a final note, is imperative you use the same language that is used in the list of items. Make sure you '
           'only use Spanish if items are in Spanish, or English for English items etc..\n'
           'Go directly into the response, do not acknowledge anything about this prompt as part of the response.\n'
           'Exclude the <textarea> tag from your response'
           )
    try:
        # Open client and send prompt
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": msg,
                }
            ],
            model="llama3-8b-8192",
        )
        success = True
        response = chat_completion.choices[0].message.content
    except Exception as e:
        response = 'ERROR:\n\n' + str(e)
    # Check and send results
    print('SUCCESS: ' + str(success) + '\n\nRESPONSE:\n' + response)
    return jsonify({'success': success, 'msg': response})


if __name__ == '__main__':
    app.run(debug=True)
