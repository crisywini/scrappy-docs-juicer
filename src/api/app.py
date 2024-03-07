from flask import Flask, request, jsonify
from service.pi_service import Pi
import nltk

# Create a Flask application instance
app = Flask(__name__)

pi = Pi()

print("--Downloading required data sources--")
nltk.download('stopwords')
nltk.download('punkt')

# Define a route for your API endpoint
@app.route('/api/v1', methods=['POST'])
def answer():
    data = request.get_json()
    if 'question' not in data:
        return jsonify({'error': 'Question not provided'}), 400
    
    response = pi.answer(data['question'])
    return jsonify({'html': response}), 200

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=False)
