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

    list_instructions = ('Read each item carefully and come up with a step-by-step plan to tackle each on of them '
                         'individually. Be concise and direct and have any personal nuances inferred from the list '
                         'items into account.\n'
                         'Assume each item is independent, and approach each one without making assumptions about '
                         'relationships between them., so make a new plan for each one of them!\n')

    internet_access = ('Keep in mind that you must use your internet access (or most updated information) to search '
                       'for alternatives ideas or propositions to fulfill each item. Whenever applicable, '
                       'propose resources for each step.\n')

    response_formatting = ('Return the response in a format that can be inserted into an <textarea [innerHTML]> '
                           'element that keeps the styling you have chosen to the response, that is, use the <i> tag '
                           'for italics, the <a> tags for links (make them open in another tab when te user clicks '
                           'them). Use the <strong> tag for bold fonts and the <u> tag to underline other text such '
                           'as titles or headers os important information. Keep in mind, use one <br> tag to add '
                           'spacing between lines with one break line and between paragraphs using two break lines in '
                           'a row (<br><br>).Finally, surround every link with the <strong> and <u> tags for better '
                           'user recognition. Refrain from using MarkDown to format the text, only these tags as '
                           'instructed.\n')

    example = ('For example, given a list with two items, your response format should look a little like this:\n'
               '<strong><u>Item #1</u></strong><br>'
               'Make a brief introduction before jumping to the instructions<br><br>'
               '<strong>1.Step title:</strong> I am describing step 1 in greater detail with a <strong><u><a href="reference" target="_blank">link</a></strong></u>.<br>'
               '<strong>2.Step title:</strong> Step 2 is similar but I am putting subtle emphasis <i>here</i> using italics.<br>'
               '<strong>3.Step title:</strong> After completing steps 1 and 2, you can log in or access another useful link with information <strong><u><a href="another_reference" target="_blank">here</a></strong></u>.<br>'
               '<strong>4.Step title:</strong> etc...<br><br>'
               '<strong><u>Item #2</u></strong><br>'
               'Make another brief introduction overviewing the steps before detailing them:<br><br>'
               '<strong>1. Step title:</strong> etc...<br>'
               '<strong>2. Step title:</strong> etc...<br>'
               '<strong>3. Step title:</strong> etc...<br><br>'
               'End with a summarizing encouraging conclusion.\n')

    language = ('As a final note, is imperative you use the same language that is used in the list of items. Make sure '
                'you only use Spanish if items are in Spanish, or English for English items etc..\n')

    prompt_instructions = 'Go directly into the response, do not acknowledge anything about this prompt as part of the response.'


    msg = ('Here is a list of items:\n' + items + '\n' + list_instructions + internet_access + response_formatting +
           example + language + prompt_instructions)
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
