from flask import Blueprint, request, jsonify
from openai import OpenAI
import os

api_blueprint = Blueprint('api', __name__)

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)
# Configure your OpenAI API key here


@api_blueprint.route('/ask_ai', methods=['POST'])
def ask_ai():
    data = request.json
    question = data.get('question')
    options = data.get('options')

    # Construct the prompt for the OpenAI API
    prompt = (
        f"Question: {question}\n"
        f"Options:\n"
        f"1. {options[0]}\n"
        f"2. {options[1]}\n"
        f"3. {options[2]}\n"
        f"4. {options[3]}\n"
        f"Please explain the question and the correct answer in a way that a child can understand."
    )

    # Make the API call to OpenAI
    response = client.chat.completions.create(
        model= "gpt-4o-mini",  # Specify the model you want to use
        messages=[{"role": "user", "content": prompt}]
    )

    explanation = response.choices[0].message.content
    
    return jsonify({'explanation': explanation})
