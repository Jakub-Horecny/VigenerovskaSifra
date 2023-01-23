from fileManager import FileManager
from LetterProb import LetterProb


class Vigener:

    """
    Dešifrujte všetky nižšie uvedené texty zašifrované vigenerovskou šifrou a určte použité heslá.
    Šifrujú sa len písmená veľkej telegrafnej abecedy (mod 26), všetky ostatné (väčšinou formátovacie) znaky ignorujte.
    Heslo je náhodne vygenerované, primerane dlhé (od 15 do 25 znakov vrátane).
    Pôvodné (priame texty) môžu byť v slovenskom aj anglickom jazyku!
    """
    def __init__(self):

        self.file_manager = FileManager()

        self.alphabet: list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                               'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.probabilities_en: list = [0.0657, 0.0126, 0.0399, 0.0322, 0.0957, 0.0175, 0.0145, 0.0404,
                                       0.0701, 0.0012, 0.0049, 0.0246, 0.0231, 0.0551, 0.0603, 0.0298, 0.0005, 0.0576, 0.0581,
                                       0.0842, 0.0192, 0.0081, 0.0086, 0.0007, 0.0167, 0.0005]

        self.probabilities_sk: list = [0.0995, 0.0118, 0.0266, 0.0436, 0.0698, 0.0113, 0.0017, 0.0175, 0.0711, 0.0157, 0.0406,
                                       0.0262, 0.0354, 0.0646, 0.0812, 0.0179, 0.0000, 0.0428, 0.0463, 0.0432, 0.0384, 0.0314,
                                       0.0000, 0.0004, 0.0170, 0.0175]

        self.min = 15
        self.max = 25

        self.message = self.file_manager.load_data()[0]
        self.message_original = self.message

    def start(self):
        self.message = self.message.replace(" ", "")  # Remove White Spaces
        print("***********************************")
        print(self.message)

        diffrences: list = self.find_tree_same_letters(self.message)
        print("***********************************")
        print(diffrences)

        devisors: list = self.find_divisor(diffrences)
        print("***********************************")
        print(devisors)

        print(len(diffrences))
        print(len(devisors))

        key = max(set(devisors), key=devisors.count)  # most frequent value
        print("***********************************")
        print("Key Length: " + str(key))

        splited: list = self.split_message(self.message, key)
        print("***********************************")
        print(splited)

        messy: list = []
        for w in splited:
            messy.append(self.decode(w, True, self.count_probabilities(w)))

        self.repair(messy)

    def find_tree_same_letters(self, message: str) -> list:
        result: list = []
        for i in range(len(message) - 3):
            j: int = i + 1
            while j < len(message) - 3:
                if message[i] == message[j] and \
                        message[i + 1] == message[j + 1] and \
                        message[i + 2] == message[j + 2]:
                    result.append(j - i)
                j += 1

        return result

    def find_divisor(self, diff: list):
        result: list = []
        for d in diff:
            i: int = self.min
            while i <= self.max:
                if d % i == 0:
                    result.append(i)
                i += 1

        return result

    def split_message(self, message: str, key_length: int):
        temp_list: list = []

        for i in range(key_length):
            s = message[i::key_length]
            temp_list.append(s)
        return temp_list

    def count_probabilities(self, substr: str) -> list:
        substr_original = substr
        count_all = len(substr)
        count_unique = len(set(substr))
        probabilities: list = []

        for letter in self.alphabet:
            probabilities.append(LetterProb(letter, 0))

        for i in range(count_unique - 1):
            count_f: int = substr.count(substr_original[0])

            for j in probabilities:
                if j.letter == substr_original[0]:
                    j.probability = float(count_f / count_all)

            substr_original = substr_original.replace(substr_original[0], "")

        return probabilities

    def decode(self, substr: list, slovak: bool, letter_probs):
        ascii_int: list = []

        # to ASCII
        for letter in substr:
            ascii_int.append(ord(letter) - 65)

        if slovak:
            decipher = self.get_original_message(letter_probs, ascii_int, self.probabilities_sk)
        else:
            decipher = self.get_original_message(letter_probs, ascii_int, self.probabilities_en)

        return decipher

    def get_original_message(self, letter_probs: list, ascii_int: list, language_prob: list):
        probability: int = 1_000_000_000
        lowest_probability_index: int = 0

        for i in range(len(language_prob)):
            temp_probability: int = 0
            index: int = 0
            for letter in letter_probs:

                if index + i >= len(language_prob):
                    temp_probability += abs(language_prob[(index + i) - len(language_prob)] -
                                            letter.probability)
                else:
                    temp_probability += abs(language_prob[index + i] - letter.probability)
                index += 1

            if temp_probability < probability:
                probability = temp_probability
                lowest_probability_index = i

        word: str = ""

        for i in ascii_int:
            word = word + chr(((i + lowest_probability_index) % 26) + 65)

        return word

    def repair(self, mess: list):
        decode_message: str = ""

        for i in range(len(mess[0])):
            for word in mess:
                if i >= len(word):
                    continue
                decode_message = decode_message + word[i]

        # add whitespace
        for i, letter in enumerate(self.message_original):
            if letter == " ":
                decode_message = decode_message[:i] + " " + decode_message[i:]

        print("***********************************")
        print("Decoded Message: ")
        print(decode_message)

        return decode_message
