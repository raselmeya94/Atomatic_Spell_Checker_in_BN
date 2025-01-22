
# Automatic Spell Checker in Bengali

Welcome to the **Automatic Spell Checker in Bengali**! This web application is designed to automatically identify and correct spelling mistakes in Bengali text as you type. Built with Flask, this app leverages advanced algorithms and a trained vocabulary model to detect and suggest corrections for misspelled Bengali words.

## Features

- **Real-time Spelling Correction**: As you type, the app detects the last word you typed and automatically corrects it if a spelling mistake is found.
- **Interactive User Interface**: A simple and intuitive interface for easy interaction with the spell checker.
- **Bengali Character Support**: The spell checker is specifically trained to work with Bengali characters, ensuring accurate spelling suggestions.
- **Misspelled Words Counter**: A count of the total misspelled words detected and corrected during your session.

## Tech Stack

- **Backend**: Python, Flask
- **Spelling Correction Algorithm**: Levenshtein Distance, Edit Operations, Word Probability Models
- **Frontend**: HTML, JavaScript (jQuery)
- **Data**: Pre-trained vocabulary and word probabilities in Bengali

## How It Works

### Backend

- **SpellChecker Class**: This class implements various operations (insert, delete, swap, replace) to generate spelling correction suggestions based on the Levenshtein distance. It uses a trained vocabulary and word probabilities stored in pickle files.
- **Flask Server**: The backend is powered by Flask. It exposes two routes:
  - `/correct_spelling`: Takes user input as JSON, processes the text using the `SpellChecker`, and returns the corrected text.
  - `/`: Displays the frontend HTML page.

### Frontend

- **Textarea Input**: Users type Bengali text in the textarea provided.
- **Real-Time Spell Checking**: The app constantly monitors your text input and suggests corrections when you type.
- **Misspelled Word Counter**: It tracks and displays the number of corrected words in real time.

## How to Run

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/raselmeya94/automatic_spell_checker_in_bn.git
   cd automatic_spell_checker_in_bn
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python app.py
   ```

4. Visit `http://127.0.0.1:5000/` in your browser to start using the spell checker.

## Project Structure

```bash
raselmeya94-automatic_spell_checker_in_bn/
│
├── app.py                  # Flask application logic
├── requirements.txt        # Python dependencies
├── spell_checker.py        # Core spelling correction logic
├── vocab.pkl               # Pre-trained vocabulary for Bengali words
├── word_probabilities.pkl  # Word probability model
│
├── static/                 
│   └── js/
│       └── spell-checker.js # JavaScript for real-time spell check functionality
│
└── templates/
    └── index.html          # Frontend HTML template
```

## Contributions

Feel free to contribute to this project! You can:

- Open issues if you encounter bugs.
- Submit pull requests for bug fixes or new features.

To contribute, please fork the repository and submit your changes via pull requests. Make sure to write tests for any new functionality added.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

#### Acknowledgments

This project uses the **Levenshtein distance** algorithm and **edit operations** (insert, delete, swap, and replace) for detecting and correcting spelling errors. The word probability model is based on a custom-trained dataset for Bengali words.

---

We hope you find the Bengali spell checker useful! 😊
