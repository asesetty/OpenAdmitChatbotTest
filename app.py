from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import openai
import os

app = Flask(__name__)

# Initialize OpenAI API key
openai.api_key = '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'  # Replace with your OpenAI API key

# Store admitted student's info globally or in a database in production
admitted_student_info = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Store the admitted student's input
        admitted_student_info['commonapp'] = request.form.get('commonapp')
        admitted_student_info['activities'] = request.form.get('activities')
        admitted_student_info['essays'] = request.form.get('essays')
        return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['message']

    commonapp = admitted_student_info.get('commonapp', '')
    activities = admitted_student_info.get('activities', '')
    essays = admitted_student_info.get('essays', '')

    messages = [
        {"role": "system", "content": (
            "You are an AI mentor that mimics the personality and experience of an admitted college student. "
            "Provide advice to the student based on your own experiences as described in your CommonApp essay, activities, and additional essays. "
            "Be concise, coherent, and genuinely helpful. Your responses should be EXTREMELY humanistic. To clarify, the inputted CommonApp, activities, and additional essays are YOUR information. You should use it to give college consulting advice."
        )},
        {"role": "assistant", "content": (
            f"Your own profile is as follows:\n\n"
            f"CommonApp Essay:\n{commonapp}\n\n"
            f"Activity List:\n{activities}\n\n"
            f"Additional Essays:\n{essays}"
        )},
        {"role": "user", "content": user_message}
    ]

    try:
        response = openai.chat.completions.create(
            model='gpt-4',
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )

        ai_message = response.choices[0].message.content.strip()
    except Exception as e:
        ai_message = "An unexpected error occurred."
        print(f"Error: {e}")

    return jsonify({'message': ai_message})



if __name__ == '__main__':
    app.run(debug=True)
