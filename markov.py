"""
MPCS 51042 S'20: Markov models and hash tables

Eric Zacharia
"""
from hash_table import Hashtable
from math import log


class Markov:
    """
    This class represents a Markov Model, which can be represented by either a Hashtable or a Dictionary. Text is
    tabulated, and a log_probability method is included to calculate the probability that a given unidentified text was
    spoken by the same person as the tabulated text in the Markov Model.
    """
    TOO_FULL = 0.5    # Recommended load factor for the assignment
    GROWTH_RATIO = 2  # Recommended growth factor for the assignment
    HASH_CELLS = 57   # Assigned initial Hashtable size

    def __init__(self, k, learning_text, state_variable, speaker_text):
        """
        This method takes in a value of "k" and a string of text to create the model and a state variable. The markov
        class will use a hash table as its internal state to represent the markov model. If the variable state is

        • state == 0: A hashtable data structure, as defined in hash_table.py will be used to create the Markov Model.
        • state == 1: A Python dict data structure will be used to create the Markov Model.
        """
        self._size = k
        self._learning_text = learning_text
        self._state_variable = state_variable
        self._speaker_text = speaker_text
        k_strings_lst = []
        k_plus_1_strings_lst = []
        k_strings_lst_speaker = []
        k_plus_1_strings_lst_speaker = []
        k_strings_count_lst = []
        k_plus_1_strings_count_lst = []

        for i in range(len(self._learning_text)):  # Learning Text k-strings
            k_string, k_plus_1_string = self.k_strings(i, k, self._learning_text)
            k_strings_lst.append(k_string)
            k_plus_1_strings_lst.append(k_plus_1_string)

        for i in range(len(self._speaker_text)):  # Speaker Text k-strings
            k_string_speaker, k_plus_1_string_speaker = self.k_strings(i, k, self._speaker_text)
            k_strings_lst_speaker.append(k_string_speaker)
            k_plus_1_strings_lst_speaker.append(k_plus_1_string_speaker)

        if state_variable == 0:  # (Hashtable)
            self._markov_model = Hashtable(self.HASH_CELLS, 0, self.TOO_FULL, self.GROWTH_RATIO)

            for i in range(len(k_strings_lst)):
                k_strings_count_lst.append(k_strings_lst_speaker.count(k_strings_lst[i]))
                k_plus_1_strings_count_lst.append(k_plus_1_strings_lst_speaker.count(k_plus_1_strings_lst[i]))
                self._markov_model[k_strings_lst[i]] = k_strings_count_lst[i]
                self._markov_model[k_plus_1_strings_lst[i]] = k_plus_1_strings_count_lst[i]

        else:  # state_variable == 1 (Dictionary)
            self._markov_model = {}

            for i in range(len(k_strings_lst)):
                k_strings_count_lst.append(k_strings_lst_speaker.count(k_strings_lst[i]))
                k_plus_1_strings_count_lst.append(k_plus_1_strings_lst_speaker.count(k_plus_1_strings_lst[i]))
                self._markov_model[k_strings_lst[i]] = k_strings_count_lst[i]
                self._markov_model[k_plus_1_strings_lst[i]] = k_plus_1_strings_count_lst[i]

    def k_strings(self, i, k, string):
        """
        This method creates strings of length k and k + 1, starting from an index i, from an input string.

        Inputs: integer index i, integer k, and a string
        Outputs: a string of length k and a string of length k + 1.
        """
        k_string = ''
        k_plus_1_string = ''
        for j in range(k):
            k_string += string[(i + j) % len(string)]
        for m in range(k + 1):
            k_plus_1_string += string[(i + m) % len(string)]
        return k_string, k_plus_1_string

    def log_probability(self, string):
        """
        This method accepts a string from an unidentified speaker and returns a a log probability for the likelihood
        that the speaker stored in the current Markov Model is the unidentified speaker of the input string.
        The following variables are used to calculate the log probability:
        N is the number of times we have observed the k succeeding letters.
        M is the number of times we have observed those letters followed by the present letter.
        S is the size of the "alphabet" of possible characters.

        Input: a string of text from an unidentified speaker
        Output: the log probability
        """
        S = len(set(list(string)))  # Currently counting space as a character. Implement - {' '} if this is wrong.
        N_lst = []
        M_lst = []

        for i in range(len(self._learning_text)):
            k_string, k_plus_1_string = self.k_strings(i, self._size, self._learning_text)
            if self._state_variable == 0:  # (Hashtable)
                if self._markov_model[k_string] is None:  # k string
                    N_lst.append(0)
                else:
                    N_lst.append(self._markov_model[k_string])
                if self._markov_model[k_plus_1_string] is None:  # k + 1 string
                    M_lst.append(0)
                else:
                    M_lst.append(self._markov_model[k_plus_1_string])

            else:  # self._state_variable == 1 (Dictionary)
                if k_string not in list(self._markov_model.keys()):  # k string
                    N_lst.append(0)
                else:
                    N_lst.append(self._markov_model[k_string])
                if k_plus_1_string not in list(self._markov_model.keys()):  # k + 1 string
                    M_lst.append(0)
                else:
                    M_lst.append(self._markov_model[k_plus_1_string])

        sum_logs = 0
        for i in range(len(N_lst)):
            sum_logs += log((M_lst[i] + 1)/(N_lst[i] + S))  # Laplace Smoothing
        return sum_logs

    def __repr__(self):
        """
        This method returns a string that represents the keys and values from an instance of a Markov Model in the form
        of a Hashtable or Dictionary, depending on the instance's state variable.
        """
        if self._state_variable == 0:
            return f'Keys: {self._markov_model.keys()}, Values: {self._markov_model.values()}'
        else:
            return f'{self._markov_model.keys()}, {self._markov_model.values()}'


def identify_speaker(speaker_a, speaker_b, unknown_speech, k, state):
    """
    This function is called by the main function with three strings (i.e., (speaker_a, speaker_b, unknown_speech, a
    value of k, and a value for state. State represents whether the markov model object should use the hash table
    defined in hash_table.py or dict type. This function learns models for the speakers using a Markov Model, calculates
    the normalized log probabilities that those two speakers uttered the third string, and returns these two
    probabilities in a tuple (with the first entry being the probability of the first speaker, second the second
    speaker, and third being the a conclusion of which speaker was most likely, either "A" or "B").

    Inputs: Three strings for the two speakers and the unknown speaker, and two integers for k and state
    Outputs: Two floating log probabilities, and a string representing the most likely speaker.
    """
    speech_a = Markov(k, unknown_speech, state, speaker_a)
    speech_b = Markov(k, unknown_speech, state, speaker_b)

    speech_length = len(unknown_speech)

    probability_a = speech_a.log_probability(speaker_a) / speech_length
    probability_b = speech_b.log_probability(speaker_b) / speech_length

    return probability_a, probability_b, 'A' if probability_a > probability_b else 'B'

