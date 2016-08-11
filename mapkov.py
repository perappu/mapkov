import pygame
import collections
import binascii

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
    print(sourceList)
    
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
        
    return markovModel
    
def getColorFromString(baseString):
    hexValue = binascii.hexlify(baseString.encode('utf-8'))
    
    return Color(hexValue)
    
def main():
    markovModel = buildFrequencyTable(sourceText)
    getColorFromString("blah")
    
    
    
if __name__ == "__main__":
    main()