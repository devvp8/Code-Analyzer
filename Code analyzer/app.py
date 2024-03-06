from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 9000
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]


def generate_code_gemini(prompt):
    genai.configure(api_key='')

    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    convo = model.start_chat(history=[])
    res = convo.send_message(
        f"you are a function code checker. Check the code {prompt} and give the incorrect part and also the correct code.",
        stream=True,
    )
    response = ""
    for chunk in res:
        response += chunk.text
    # print(response)
    return response

@app.route('/')
def index():
    return render_template('indexgem.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.form['code']
    response = generate_code_gemini(code)
    return render_template('gemini.html',response = response,code=code, message='Code analysis initiated successfully.')

if __name__ == '__main__':
    app.run(debug=True)
