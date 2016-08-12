#!/usr/bin/env python
# -*- coding: utf-8 -*- #

""" Builds a multicolored map of tiles using a Markov chain algorithm.

Each word in the sample text corresponds to a single RGB color.
Using the frequency table we make from the text, we can procedurally
generate a map of colored tiles that follows the same pattern.

This is intended for use generating a map for some kind of 2D game. """

import random
from math import ceil
import pygame

# Size of screen
width = 800
height = 640

# Sample text
sampleText = ("Stop. Who would cross the Bridge of Death must answer me these questions three,"
                " ere the other side he see. Ask me the questions, bridgekeeper."
                " I am not afraid. What... is your name? My name is Sir Lancelot of Camelot."
                " What... is your quest? To seek the Holy Grail. What... is your favourite colour?"
                " Blue. Go on. Off you go. Oh, thank you. Thank you very much. That's easy."
                " Stop. Who would cross the Bridge of Death must answer me these questions three, ere"
                " the other side he see. Ask me the questions, bridgekeeper. I'm not afraid."
                " What... is your name? Sir Robin of Camelot. What... is your quest?"
                " To seek the Holy Grail. What... is the capital of Assyria? [pause]"
                " I don't know that. [he is thrown over the edge into the volcano]"
                " Auuuuuuuugh. Stop. What... is your name? Sir Galahad of Camelot. What... is your quest?"
                " I seek the Grail. What... is your favourite colour? Blue. No, yel..."
                " [he is also thrown over the edge] auuuuuuuugh. Hee hee heh. Stop."
                " What... is your name? It is 'Arthur', King of the Britons."
                " What... is your quest? To seek the Holy Grail. What... is the air-speed velocity of an unladen swallow?"
                " What do you mean? An African or European swallow? Huh? I... I don't know that."
                " [he is thrown over] Auuuuuuuugh. How do know so much about swallows?"
                " Well, you have to know these things when you're a king, you know.")

def buildFrequencyTable(text):
    """ Build a table pairing each word in the sample text with what word(s) are most likely to come after it. """

    # Turn the input text into a list of words/tokens
    sourceList = text.split()

    # Start our model as an empty dictionary
    markovModel = {}

    # Iterate through the sourceList to build our frequency table
    for i, word in enumerate(sourceList):

        # Check if we're at the end of the list
        if i+1 != len(sourceList):

            # If we haven't added this word to our table yet, add it
            if word not in markovModel:
                markovModel[word] = {sourceList[i+1]: 1}

            # If we have added this word to our table, record what word comes after it
            if word in markovModel:
                if sourceList[i+1] not in markovModel[word]:
                    markovModel[word][sourceList[i+1]] = 1

                else:
                    markovModel[word][sourceList[i+1]] += 1

        # If there is no following word
        else:
            markovModel[word] = {}

    return markovModel

def getColorFromString(baseString):
    """ Take an arbitrary string and return a RGB tuple from the first 3 bytes. """

    # Get byte array of string
    stringBytes = bytearray(baseString.encode('utf8'))

    # Default values in case the byte array length < 3
    rgb = [0, 0, 0]

    if len(stringBytes) <= 3:
        for i in range(len(stringBytes)):
            rgb[i] = stringBytes[i]
    else:
        for i in range(3):
            rgb[i] = stringBytes[i]

    return tuple(rgb)

def findNextWord(currentWord, markovModel):
    """ Use our frequency table to get the next word in sequence. """

    potentialWords = []

    # For each potential next word's multiplicity, add it to the potentialWords list that many times
    # This represents how some words are more frequent than others
    for word in markovModel[currentWord]:
        for i in range(markovModel[currentWord][word]):
            potentialWords.append(word)

    # Pick something out of the potentialWords list to be our next word
    nextWord = random.choice(potentialWords)

    return nextWord


def main():

    # Create screen
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill((0, 0, 0))

    # Build our Markov table
    markovModel = buildFrequencyTable(sampleText)

    # Find how many squares we can fit on our screen
    numberOfSquares = ceil((width * height) / 100)

    # Pick a random starting value
    word = random.sample(markovModel.items(), 1)[0][0]

    # Our first square will be at 0,0
    x = 0
    y = 0

    for i in range(numberOfSquares):

        # If our next word doesn't have any words after it, get us a new one.
        if not markovModel[word]:
            while not markovModel[word]:
                word = random.sample(markovModel.items(), 1)[0][0]

        # Find our next word and its respective color
        word = findNextWord(word, markovModel)
        color = getColorFromString(word)

        # Draw the tile
        pygame.draw.rect(screen, color, pygame.Rect(x, y, 10, 10))
        pygame.display.flip()

        # Change x and y so the next square is in the right place.
        # If we're at the edge of the screen, loop to the next row.
        x += 10
        if x > width:
            x = 0
            y += 10

        print(word, color)

    print("Done!")

    # Keep pygame going until we close it
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == "__main__":
    main()
