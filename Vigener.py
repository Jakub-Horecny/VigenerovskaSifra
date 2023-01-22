import math

from fileManager import FileManager
from LetterProb import LetterProb


class Vigener:

    def __init__(self):

        self.file_manager = FileManager()

        self.alphabet: list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                               'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.prob_en: list = [0.0657, 0.0126, 0.0399, 0.0322, 0.0957, 0.0175, 0.0145, 0.0404,
                              0.0701, 0.0012, 0.0049, 0.0246, 0.0231, 0.0551, 0.0603, 0.0298, 0.0005, 0.0576, 0.0581,
                              0.0842, 0.0192, 0.0081, 0.0086, 0.0007, 0.0167, 0.0005]

        self.prob_sk: list = [0.0995, 0.0118, 0.0266, 0.0436, 0.0698, 0.0113, 0.0017, 0.0175, 0.0711, 0.0157, 0.0406,
                              0.0262, 0.0354, 0.0646, 0.0812, 0.0179, 0.0000, 0.0428, 0.0463, 0.0432, 0.0384, 0.0314,
                              0.0000, 0.0004, 0.0170, 0.0175]

        self.min = 15
        self.max = 25

        self.contents = self.file_manager.load_data()[0]
        self.original = self.contents

    def cipher(self):
        """pole = self.file_manager.load_data(self.path)
        data: str = pole[0]
        print(data)"""

        self.contents = self.contents.replace(" ", "")  # Remove White Spaces
        print(self.contents)

        diffrences: list = self.FindTreeLetters(self.contents)
        print(diffrences)

        devisors: list = self.FindDevisor(diffrences, self.min, self.max)
        print(devisors)

        splited: list = self.SplitMessage(self.contents, self.MostUsedValue(devisors))
        print(splited)

        messy: list = []
        for w in splited:
            messy.append(self.Decipher(w, True, self.GetProbabilities(w)))

        self.Repair(messy)

    def FindTreeLetters(self, input: str):
        result: list = []
        for i in range(len(input) - 4):

            """for j, inp in enumerate(input[:len(input)-3], start=i + 1):
                if j > len(input) - 3:
                    break
                if input[i] == input[j] and \
                        input[i + 1] == input[j + 1] and \
                        input[i + 2] == input[j + 2]:
                    result.append(j - 1)"""
            j: int = i + 1
            while j < len(input) - 3:
                if input[i] == input[j] and \
                        input[i + 1] == input[j + 1] and \
                        input[i + 2] == input[j + 2]:
                    result.append(j - i)
                j += 1
        return result

    def FindDevisor(self, diff: list, lower: int, upper: int):
        devisors: list = []
        for d in diff:
            i: int = lower
            while i <= upper:
                if d % i == 0:
                    devisors.append(i)
                i += 1

        return devisors

    def MostUsedValue(self, devs: list):
        max_count: int = 0
        max_freg: int = 0

        for i in range(len(devs)):
            count: int = 0
            for j in range(len(devs)):
                if devs[i] == devs[j]:
                    count += 1

            if count > max_count:
                max_count = count
                max_freg = devs[i]

        return max_freg

    def SplitMessage(self, msg: str, dev: int):
        splited: list = []
        for i in range(dev):
            s: str = ""
            j: int = i

            while j < len(msg):
                s = s + msg[j]
                j += dev
            splited.append(s)
        return splited

    def GetProbabilities(self, substring: str) -> list:
        source = substring
        count_all = len(substring)
        count_unique = len(set(substring))
        probabilities: list = []

        for l in self.alphabet:
            probabilities.append(LetterProb(l, 0))

        for i in range(count_unique - 1):
            countF: int = substring.count(source[0])

            for j in probabilities:
                if j.letter == source[0]:
                    j.probability = float(countF / count_all)

            source = source.replace(source[0], "")

        return probabilities

    def Decipher(self, word, slovak, letterProbs):
        decipher: str = ""
        ascii_int: list = []

        # to ASCII
        for w in word:
            ascii_int.append(ord(w) - 65)

        # asi môže ísť do piče
        if slovak:
            decipher = self.GetSlovakString(letterProbs, ascii_int)

        return decipher

    def GetSlovakString(self, letterProbs: list, ascii_int):
        prob: int = 999_999
        bestShift: int = 0

        for i in range(len(self.prob_sk)):
            helper: int = 0
            shift: int = 0
            for item in letterProbs:

                if shift + i >= len(self.prob_sk):
                    helper += abs(self.prob_sk[(shift + i) - len(self.prob_sk)] -
                                  item.probability)
                else:
                    helper += abs(self.prob_sk[shift + i] - item.probability)
                shift += 1
            if helper < prob:
                prob = helper
                bestShift = i

        pom: list = []

        for i in ascii_int:
            pom.append(((i + bestShift) % 26) + 65)

        word: str = ""
        for i in pom:
            word = word + chr(i)

        return word

    def Repair(self, mess: list):
        decodeWord: str = ""

        for i in range(len(mess[0])):
            for word in mess:
                if i >= len(word):
                    continue
                decodeWord = decodeWord + word[i]

        print("---------------------------")
        print("Message is: ")

        WhiteSpacesIndexes: list = []

        for i, letter in enumerate(self.original):
            if letter == " ":
                WhiteSpacesIndexes.append(i)

        for i in range(len(WhiteSpacesIndexes)):
            decodeWord = decodeWord[:WhiteSpacesIndexes[i]] + " " + decodeWord[WhiteSpacesIndexes[i]:]

        print(decodeWord)
        return decodeWord
