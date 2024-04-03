import re
import pickle
from collections import Counter
import Levenshtein

class SpellChecker:
    def __init__(self, vocab_file, probabilities_file):
        with open(vocab_file, 'rb') as f:
            self.vocab = pickle.load(f)
        with open(probabilities_file, 'rb') as f:
            self.word_probabilities = pickle.load(f)

    def split_operation(self, word):
        return [(word[:i], word[i:]) for i in range(len(word) + 1)]

    def delete_operation(self, word):
        return [l + r[1:] for l, r in self.split_operation(word) if r]

    def swap_operation(self, word):
        return [l + r[1] + r[0] + r[2:] for l, r in self.split_operation(word) if len(r) > 1]

    def replace_operation(self, word):
        bengali_characters = ['অ', 'আ', 'ই', 'ঈ', 'উ', 'ঊ', 'ঋ', 'এ', 'ঐ', 'ও', 'ঔ',
                               'ক', 'খ', 'গ', 'ঘ', 'ঙ', 'চ', 'ছ', 'জ', 'ঝ', 'ঞ', 'ট',
                               'ঠ', 'ড', 'ঢ', 'ণ', 'ত', 'থ', 'দ', 'ধ', 'ন', 'প', 'ফ',
                               'ব', 'ভ', 'ম', 'য', 'র', 'ল', 'শ', 'ষ', 'স', 'হ', 'ড়',
                               'ঢ়', 'য়', 'ৎ', 'ং', 'ঃ', '‍ঁ', 'া' , 'ি', 'ী', 'ু', 'ূ', 'ৃ',
                               'ৄ', 'ে', 'ৈ', 'ো', 'ৌ', '্']
        return [word[:i] + char + word[i + 1:] for i in range(len(word)) for char in bengali_characters if
                char != word[i]]

    def insert_operation(self, word):
        bengali_characters = ['অ', 'আ', 'ই', 'ঈ', 'উ', 'ঊ', 'ঋ', 'এ', 'ঐ', 'ও', 'ঔ',
                               'ক', 'খ', 'গ', 'ঘ', 'ঙ', 'চ', 'ছ', 'জ', 'ঝ', 'ঞ', 'ট',
                               'ঠ', 'ড', 'ঢ', 'ণ', 'ত', 'থ', 'দ', 'ধ', 'ন', 'প', 'ফ',
                               'ব', 'ভ', 'ম', 'য', 'র', 'ল', 'শ', 'ষ', 'স', 'হ', 'ড়',
                               'ঢ়', 'য়', 'ৎ', 'ং', 'ঃ', '‍ঁ', 'া' ,  'ি', 'ী', 'ু', 'ূ', 'ৃ',
                               'ৄ', 'ে', 'ৈ', 'ো', 'ৌ', '্']
        return [word[:i] + char + word[i:] for i in range(len(word) + 1) for char in bengali_characters]

    def level_one_edit(self, word):
        return set(self.delete_operation(word) + self.swap_operation(word) +
                   self.replace_operation(word) + self.insert_operation(word))

    def level_two_edit(self, word):
        return set(word2 for word1 in self.level_one_edit(word) for word2 in self.level_one_edit(word1))
    
    import Levenshtein

    def calculate_text_distance(self, text1, text2):
        distance = Levenshtein.distance(text1, text2)
        return distance

    def word_similarity_checker(self, misspelled_word, predicted_word=None):
        bengali_characters = ['অ', 'আ', 'ই', 'ঈ', 'উ', 'ঊ', 'ঋ', 'এ', 'ঐ', 'ও', 'ঔ',
                            'ক', 'খ', 'গ', 'ঘ', 'ঙ', 'চ', 'ছ', 'জ', 'ঝ', 'ঞ', 'ট',
                            'ঠ', 'ড', 'ঢ', 'ণ', 'ত', 'থ', 'দ', 'ধ', 'ন', 'প', 'ফ',
                            'ব', 'ভ', 'ম', 'য', 'র', 'ল', 'শ', 'ষ', 'স', 'হ', 'ড়',
                            'ঢ়', 'য়', 'ৎ']
        misspelled_chars= [chac_ for chac_ in (list(misspelled_word)) if chac_ in bengali_characters]
        misspelled_chars.sort()
        misspelled_chars="".join(misspelled_chars)
        if predicted_word is None:
            return misspelled_chars
            
        predicted_chars= [chac_ for chac_ in (list(predicted_word)) if chac_ in bengali_characters]
        predicted_chars.sort()
        predicted_chars="".join(predicted_chars)
        distance=self.calculate_text_distance(misspelled_chars, predicted_chars )
        if distance in [0,1]:
            return predicted_chars
        else:
            return ""
    def best_words(self, misspelled_word):
        
        suggestions=  self.level_one_edit(misspelled_word) and self.level_two_edit(misspelled_word) or [misspelled_word]

        best_guesses=[word for word in suggestions if word in self.vocab]

        word_len=len(self.word_similarity_checker(misspelled_word))
        return [(word , self.word_probabilities[word]) for word in best_guesses if word_len<=len(self.word_similarity_checker(misspelled_word , word)) ]
        

    def correct_word(self, misspelled_word):
        if misspelled_word in self.vocab:
            return misspelled_word
        
        best_guesses = self.best_words(misspelled_word)
        # print(best_guesses, sep=" \n")
        if best_guesses:
            return max(best_guesses, key=lambda x: x[1], default=('', 0))[0]
        return misspelled_word

    def correct_spelling(self, text):

        corrected_words = self.correct_word(text)
        return corrected_words
