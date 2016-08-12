#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import pygame
import collections
import random
from math import ceil
from fractions import gcd

# Size of screen
width = 800
height = 640

# Text to generate our Markov model from
sourceText = ("Stop. Who would cross the Bridge of Death must answer me these questions three,"
    " ere the other side he see. Ask me the questions, bridgekeeper." 
    " I am not afraid. What... is your name? My name is Sir Lancelot of Camelot."
    " What... is your quest? To seek the Holy Grail. What... is your favourite colour?"
    " Blue. Go on. Off you go. Oh, thank you. Thank you very much. That's easy."
    " Stop. Who would cross the Bridge of Death must answer me these questions three,"
    " ere the other side he see. Ask me the questions, bridgekeeper. I'm not afraid."
    " What... is your name? Sir Robin of Camelot. What... is your quest? To seek the Holy Grail."
    " What... is the capital of Assyria? [pause] I don't know that. [he is thrown over the edge into the volcano]"
    " Auuuuuuuugh. Stop. What... is your name? Sir Galahad of Camelot. What... is your quest?"
    " I seek the Grail. What... is your favourite colour? Blue. No, yel... [he is also thrown over the edge]"
    " auuuuuuuugh. Hee hee heh. Stop. What... is your name? It is 'Arthur', King of the Britons."
    " What... is your quest? To seek the Holy Grail. What... is the air-speed velocity of an unladen swallow?"
    " What do you mean? An African or European swallow? Huh? I... I don't know that."
    " [he is thrown over] Auuuuuuuugh. How do know so much about swallows?"
    " Well, you have to know these things when you're a king, you know.")
    
def buildFrequencyTable(sourceText):
    """ Returns a dict with the frequency of each character in the sample text. """
    
    #Turn the input text into a list of words/tokens
    sourceList = sourceText.split()
    
    #Start our model as an empty dictionary
    markovModel = {}
    
    #Iterate through the sourceList to build our frequency table
    for i, word in enumerate(sourceList):
        
        #check if we're at the end of the list
        if i+1 != len(sourceList):
        
            #if we haven't added this word to our table yet, add it
            if word not in markovModel:
                markovModel[word] = {sourceList[i+1]: 1}
                
            #if we have added this word to our table, record what word comes after it
            if word in markovModel:
                if sourceList[i+1] not in markovModel[word]:
                    markovModel[word][sourceList[i+1]] = 1
                    
                else:
                    markovModel[word][sourceList[i+1]] += 1
        
        else:
            markovModel[word] = {}
        
    return markovModel
    
def getColorFromString(baseString):
    """ Takes an arbitrary string and generates an RGB tuple from the first 3 bytes. """
    
    # Get byte array of string
    bytes = bytearray(baseString.encode('utf8'))
    
    # In case the byte array < 3
    rgb = [0, 0, 0]
    
    if len(bytes) <= 3:
        for i in range(len(bytes)):
            rgb[i] = bytes[i]
    else:
        for i in range(3):
            rgb[i] = bytes[i]
    
    return tuple(rgb)
    
def findNextWord(currentWord, markovModel):
    """ Uses our Markov frequency table to get the next word in our sequence. """
    
    potentialWords = []
    
    # For a potential next word's multiplicity, add it to the potentialWords array that many times
    for word in markovModel[currentWord]:
        for i in range(markovModel[currentWord][word]):
            potentialWords.append(word)
    
    # Pick something randomly out of the potentialWords array, and that's our next word
    nextWord = random.choice(potentialWords)
    
    return nextWord
    
    
def main():

    # Create screen
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill((0, 0, 0))
    
    # Build our Markov table
    markovModel = buildFrequencyTable(sourceText)
    
    # Find how many squares we can fit on our screen
    numberOfSquares = ceil((width * height) / 100)
    
    # Pick a random starting value.
    word = random.sample(markovModel.items(), 1)[0][0]
    
    # Our first square will be at 0,0
    x = 0
    y = 0
    
    for i in range(numberOfSquares):
    
        # If our next word doesn't have any words after it, get us a new one
        if not markovModel[word]:
            while not markovModel[word]:
                word = random.sample(markovModel.items(), 1)[0][0]
    
        # Find our next word and its respective color
        word = findNextWord(word, markovModel)
        color = getColorFromString(word)
        
        # Draw the rectangle
        pygame.draw.rect(screen, color, pygame.Rect(x, y, 10, 10))
        pygame.display.flip()
        
        # Change x and y so the next square is in the right place
        # If we're at the edge of the screen, loop to the next row
        x += 10
        if x > width:
            x = 0
            y += 10
        
        print(word, color)
        
    print("Done!")
    
    # Keep pygame chugging until we close it
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        
if __name__ == "__main__":
    main()