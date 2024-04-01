import re
import pickle
from collections import Counter

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
                               'ঢ়', 'য়', 'ৎ', 'ং', 'ঃ', '‍ঁ', 'ি', 'ী', 'ু', 'ূ', 'ৃ',
                               'ৄ', 'ে', 'ৈ', 'ো', 'ৌ', '্']
        return [word[:i] + char + word[i + 1:] for i in range(len(word)) for char in bengali_characters if
                char != word[i]]

    def insert_operation(self, word):
        bengali_characters = ['অ', 'আ', 'ই', 'ঈ', 'উ', 'ঊ', 'ঋ', 'এ', 'ঐ', 'ও', 'ঔ',
                               'ক', 'খ', 'গ', 'ঘ', 'ঙ', 'চ', 'ছ', 'জ', 'ঝ', 'ঞ', 'ট',
                               'ঠ', 'ড', 'ঢ', 'ণ', 'ত', 'থ', 'দ', 'ধ', 'ন', 'প', 'ফ',
                               'ব', 'ভ', 'ম', 'য', 'র', 'ল', 'শ', 'ষ', 'স', 'হ', 'ড়',
                               'ঢ়', 'য়', 'ৎ', 'ং', 'ঃ', '‍ঁ', 'ি', 'ী', 'ু', 'ূ', 'ৃ',
                               'ৄ', 'ে', 'ৈ', 'ো', 'ৌ', '্']
        return [word[:i] + char + word[i:] for i in range(len(word) + 1) for char in bengali_characters]

    def level_one_edit(self, word):
        return set(self.delete_operation(word) + self.swap_operation(word) +
                   self.replace_operation(word) + self.insert_operation(word))

    def level_two_edit(self, word):
        return set(word2 for word1 in self.level_one_edit(word) for word2 in self.level_one_edit(word1))

    def correct_word(self, word):
        if word in self.vocab:
            return word
        suggestions = self.level_one_edit(word) or self.level_two_edit(word) or [word]
        best_guesses = [word for word in suggestions if word in self.vocab]
        if best_guesses:
            return max(best_guesses, key=lambda x: self.word_probabilities[x])
        return word

    def correct_spelling(self, text):
        words = text.split()
        corrected_words = [self.correct_word(word) for word in words]
        return ' '.join(corrected_words)