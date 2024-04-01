from flask import Flask, request, jsonify, render_template
from spell_checker import SpellChecker

app = Flask(__name__)

@app.route('/correct_spelling', methods=['POST'])
def correct_spelling():
  text = request.json['text']
  spell_checker = SpellChecker("../Auto-Spelling-App/vocab.pkl", "../Auto-Spelling-App/word_probabilities.pkl")  # Replace with your file paths
  corrected_text = spell_checker.correct_spelling(text)
  return jsonify({'corrected_text': corrected_text})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
  app.run()
