import speech_recognition as sr
from translate import Translator
import requests
from collections import defaultdict

qwestions = {'Как тебя зовут' : "Я супер-крутой-бот и мое ппредназначение помогать тебе!",
             "Сколько тебе лет" : "Это слишком философский вопрос"}

class TextAnalysis():   
    
    memory = defaultdict(list)

    def __init__(self, text, owner):

        TextAnalysis.memory[owner].append(self)

        self.text = text
        self.translation = self.__translate(self.text, "ru", "en")

        if self.text in qwestions.keys():
            self.response = qwestions[self.text]
        else:
            self.response = self.get_answer() 

    
    def get_answer(self):
        res = self.__translate(self.__deep_pavlov_answer(), "en", "ru")
        return res

    def __translate(self, text, from_lang, to_lang):
        try:
            translator= Translator(from_lang=from_lang, to_lang=to_lang)
            translation = translator.translate(text)
            return translation
        except:
            return "Перевод не удался"

    def __deep_pavlov_answer(self):
        try:
            API_URL = "https://7038.deeppavlov.ai/model"
            data = {"question_raw": [ self.translation ]}
            res = requests.post(API_URL, json=data).json()
            res = res[0][0]
        except:
            res = "I don't know how to help"
        return res

