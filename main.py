from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

# Key map dictionary
keydict = {
    'q':0,
    'w':1,
    'e':2,
    'r':3,
    't':4,
    'y':5,
    'u':6,
    'i':7,
    'o':8,
    'p':9,
    'a':10,
    's':11,
    'd':12,
    'f':13,
    'g':14,
    'h':15,
    'j':16,
    'k':17,
    'l':18,
    'z':20,
    'x':21,
    'c':22,
    'v':23,
    'b':24,
    'n':25,
    'm':26,
}

def check_result():
    currentRow = driver.find_elements_by_class_name("Row-locked-in")[guesses]
    if not currentRow.find_elements_by_class_name("letter-absent") and not currentRow.find_elements_by_class_name("letter-elsewhere"):
        word = ""
        for letter in currentRow.find_elements_by_class_name("letter-correct"):
            word += letter.text
        print("Game Won!")
        print("Word: " + word)
        time.sleep(2)
        driver.find_elements_by_class_name("restart_btn")[0].click()
        return True
    else:
        count = 0
        for element in currentRow.find_elements_by_class_name("Row-letter"):
            if str(element.get_attribute("class")).split()[1] == "letter-absent":
                absentLetters.append(str(element.text).lower())
            elif str(element.get_attribute("class")).split()[1] == "letter-elsewhere":
                elsewhereLetters[count].append(str(element.text).lower())
            elif str(element.get_attribute("class")).split()[1] == "letter-correct":
                correctLetters[count].append(str(element.text).lower())
            else:
                print("Error unexpected element class on check_result: " + str(element.get_attribute("class")))
            count += 1
        print("Absent: " + str(absentLetters))
        print("Elsewhere: " + str(elsewhereLetters))
        print("Correct: " + str(correctLetters))
        return False

def type_word(word):
    for i in word:
        driver.find_elements_by_class_name("Game-keyboard-button")[keydict.get(i)].click()
    driver.find_elements_by_class_name("Game-keyboard-button-wide")[1].click() # enter
    time.sleep(1)

    
def check_correct(word, correctLetters):
    count = 0
    for char in word: 
        if char not in correctLetters.get(count) and len(correctLetters.get(count)) > 0:
            return False
        count += 1
    return all([char in word for char in [item for sublist in correctLetters.values() for item in sublist]])

def check_elsewhere(word, elsewhereLetters):
    count = 0
    for char in word: 
        if char in elsewhereLetters.get(count):
            return False
        count += 1
    return all([char in word for char in [item for sublist in elsewhereLetters.values() for item in sublist]])


    
def find_words(words, absentLetters, elsewhereLetters, correctLetters, guessedWords):
    wordList = []
    for word in words:
        if not any([char in word for char in list(set(absentLetters) - (set([item for sublist in correctLetters.values() for item in sublist]).union(set([item for sublist in elsewhereLetters.values() for item in sublist]))))]):
            if check_correct(word, correctLetters):
                if check_elsewhere(word, elsewhereLetters):
                    if word not in guessedWords:
                        wordList.append(word)
    return wordList
    
words = open("words-five.txt").read().splitlines()
driver = webdriver.Firefox()
driver.get("https://wordlegame.org/")
startingWords = ['adieu', 'soare', 'snare', 'cough', 'pious', 'maker', 'teary']
while(True):
    print("New Game")
    gameWon = False
    guesses = 0
    guessedWords = []
    absentLetters = []
    elsewhereLetters = {0:[], 1:[], 2:[], 3:[], 4:[]}
    correctLetters = {0:[], 1:[], 2:[], 3:[], 4:[]}
    time.sleep(4)
    startingWord=random.choice(startingWords)
    type_word(startingWord)
    check_result()
    guesses += 1
    while(guesses < 6 and not gameWon):
        guessedWord = random.choice(find_words(words, absentLetters, elsewhereLetters, correctLetters, guessedWords))
        guessedWords.append(guessedWord)
        time.sleep(0.5)
        type_word(guessedWord)
        time.sleep(0.5)
        gameWon = check_result()
        if gameWon:
            break
        guesses += 1
    if guesses == 6:
        print("Game Lost!")
        time.sleep(2)
        driver.find_elements_by_class_name("restart_btn")[0].click()
