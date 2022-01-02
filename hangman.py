import turtle
import random
import copy

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
y=0
inputs = []
words=["bruh","cringe","based","redpilled","chad","soyboy"]

secret_word= words[random.randint(0,5)]

dashes=len(secret_word)*"_"

print(secret_word)


def get_guess():
  """
  We are asking for the user's input, if it is not a single letter
  that is lowercase it prints "invalid input" and requests again
  until a valid input is placed. It will then return ug as the 
  user's input
  """
  ug=input("enter a letter:")
  while (len(ug) != 1) or (ug.islower()==False):
    print("invalid input")
    ug=input("enter a letter")
  return ug


def update_dashes(userInput, currentString):
    ansList = make_ansList()
    dataList = currentString
    for i in range((len(secret_word))):       #count an i for every character in "secret word"
        if ansList[i] == userInput:
            dataList[i] = userInput
        elif ansList[i] != userInput and ansList[i] not in alphabet:
            if ansList[i] == " ":
                dataList[i] = " " #This may be redundant but it makes the code easier to read
            else:
                dataList[i] = "_"
    print(dataList)
    return dataList

def starter_dashes(userInput, currentString):
    ansList = make_ansList()
    dataList = currentString
    for i in range((len(secret_word))):       #count an i for every character in "secret word"
        if ansList[i] == userInput:
            dataList[i] = userInput
        elif ansList[i] != userInput and ansList[i] in alphabet:
            if ansList[i] == " ":
                dataList[i] = " " #This may be redundant but it makes the code easier to read
            else:
                dataList[i] = "_"
    print(dataList)
    return dataList

# returns a list with certain letters turned into dashes
# we will set 


def make_ansList():
  secret_list=[]
  for i in secret_word:
    secret_list+=[i]
  return secret_list
print (make_ansList())


def hangman():
  """
  
  """
  f = 0
  currentString = update_dashes("_", make_ansList())  #This creates a blank slate of "_", which allows us to change if not in alphabet

  llist=make_ansList()  #This is the answer list
  while True:
    ng = get_guess()
    if f >= 10:
      print("sorry, game over")
      break
    elif ng in secret_word:     #This will check whether our answer is valid, not complete as it does not count for when we say the same answer
        currentString = update_dashes(ng, currentString)
        print(currentString)
        

        #A function that stores our variables/data
        #Want to add ng to the list of letters in that function
        #We will then compare this list of letters to our answer and our update dashes will replace the dashes with the appropriate letters.
        
        print("correct")
    else:
        print("wrong")
        f += 1
    