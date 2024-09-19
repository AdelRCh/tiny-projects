#Punctuations matter enough that I will go for RegEx.
import re
from difflib import SequenceMatcher

#I would concede that, due to lack of knowledge, I wouldn't have identified that
#SequenceMatcher could impact word constructions instead of focusing on letters.
#That said, I'd rather go at it safely like this:
class WordCodec:
    words: list
    counter: int

    def __init__(self):
        '''This "word codec" class allows us to encode strings into int values
        for ease of processing in SequenceMatcher.'''
        self.words = []
        self.counter = 0

    def add_word(self, word:str):
        '''Add words from a list of words (spaces and punctuation included) to
        the WordCodec.'''
        if word not in self.words:
            self.counter+=1
            self.words.append(word)

    def encode_list(self, to_encode:list):
        '''Encodes a list, turning it from words to digits. If a word was not
        encountered during the add_word phase, it will be subsequently added.'''
        i = 0
        #output = [self.words.index(word) for word in to_encode]
        output = []

        while i < len(to_encode):
            try:
                output.append(self.words.index(to_encode[i]))
            except:
                self.add_word(to_encode[i])
                output.append(self.words.index(to_encode[i]))
            i+=1
        return output

    def decode_list(self, to_decode:list):
        '''Decodes a list into its output words. This function may not be
        necessary, but who knows.'''
        i = 0
        #output = [self.words[digit] for digit in to_decode]
        output = []

        while i < len(to_decode):
            output.append(self.words[to_decode[i]])
            i+=1
        return output

def compare_sentences(s1:str, s2:str) -> list:
    '''The function will receive two strings and return a dictionary with
    annotations.

    Input:
    - s1: string
    - s2: string

    Output:
    - strs: a list containing either sentence segments (if they are common to
    both strings), or tuples featuring (substring1, substring2) for any
    differences. Substrings can contain more than two words.

    The output is formatted so as to work with st-annotated-text, an extension
    for Streamlit. However, it can be reorganized at will.
    '''
    strs = [] # Our output will also contain a list of strings and their matches

    #We have our mask to split words and keep punctuation in place.
    regex_mask = r"[\w']+|[.,!?;-— ]"

    # Separating sentences and retaining the punctuation
    words1 = re.findall(regex_mask, s1, re.UNICODE)
    words2 = re.findall(regex_mask, s2, re.UNICODE)

    lexicon = WordCodec()
    for word in words1:
        lexicon.add_word(word)
    for word in words2:
        lexicon.add_word(word)

    w_code1 = lexicon.encode_list(words1)
    w_code2 = lexicon.encode_list(words2)

    #Using Difflib's Sequence Matcher to untangle the process that led us from
    #the first sequence to the second one
    s = SequenceMatcher(None,w_code1,w_code2)

    #Then, we reorganize our sequences into words/sentence fragments.
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == 'equal':
            strs.append(''.join(words1[i1:i2]))
        elif tag == 'replace':
            strs.append((''.join(words1[i1:i2]),''))
            strs.append(('',''.join(words2[j1:j2])))
        else:
            strs.append((''.join(words1[i1:i2]),''.join(words2[j1:j2])))

    return strs
