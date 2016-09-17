import string
from math import cos,sin
from tkinter import *
from tkinter import ttk

def rgbString(red, green, blue):
    #http://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
    return "#%02x%02x%02x" % (red, green, blue)

################################
# syntax highlighting
def recolorize(text):
    for line in range(1, int(text.index('end').split('.')[0])):
        colorizeLine(text,line)
    addComment(text)
    tripleQuote(text)
    lineMax = 200
    if int(text.index("end").split(".")[0]) < lineMax:
        checkBracket(text)
    else:
        start = text.index("insert linestart")
        end = text.index("insert lineend")
        checkBracket(text,start,end)

def tripleQuote(text):
    #check for triple quotes in the text
    content = text.get("1.0","end")
    unbalanced,start,triples = 0,0,[]
    for i in range(len(content)-len("''")):
        if unbalanced == 0:
            if content[i:i+len("'''")] == "'''":
                unbalanced = 1
                unmatched = "'''"
                start = i
            elif content[i:i+len('"""')] == '"""':
                unbalanced = 1
                unmatched = '"""'
                start = i
        else:
            if content[i:i+len("'''")] == unmatched:
                unbalanced,unmatched = 0,""
                end = i + len("'''")
                triples.append((start,end))
    if unbalanced == 1: triples.append((start,len(content)))
    addTriple(text,triples,content)

#add tags to the triple quotes identified
def addTriple(text,triples,content):
    for (start,end) in triples:
        string = content[start:end]
        index = text.search(string,"1.0",stopindex="end")
        text.tag_add("string",index,"{0} +{1}c".format(index,len(string)))

def recolorizeAll(text,root):
    recolorize(text)
    delay = 300
    root.time += delay
    root.callback = text.after(delay,recolorizeAll,text,root)

def colorizeLine(text,line):
    content = text.get("{0}.0".format(line),"{0}.end".format(line))
    addTags(lineParsing(content),text,line)

#recursively colorize commented lines
def addComment(text,startIndex = "1.0"):
    startIndex = text.search("#", startIndex,stopindex=END)
    if not startIndex:
        return None
    endIndex = '{0}.end'.format(startIndex.split(".")[0])
    if "string" not in text.tag_names(startIndex):
        clearTagsRange(text,startIndex,endIndex)
        text.tag_add("comment",startIndex,endIndex)
    addComment(text,endIndex)

#analyze a line into its parts and describe their syntactic roles.
def lineParsing(s):
    (parsed,word,unbalanced,possible) = initParsing()
    for c in s:
        if unbalanced != 0:
            word += c
            if c == quotation:
                parsed.append(word)
                word,unbalanced,quotation = "",0,None
        elif c in possible:
            word += c
        else:
            if word: parsed.append(word)
            word = ""
            if c in ["'",'"']:
                quotation = "'" if c == "'" else '"'
                unbalanced += 1
                word += c
            else:
                parsed.append(c)
    if word: parsed.append(word)
    return parsed

def initParsing():
    possible = set([c for c in string.ascii_letters+string.digits])
    (parsed,word,unbalanced) = ([],"",0)
    return (parsed,word,unbalanced,possible)

#add tags to the parsed parts according to their syntactic role
def addTags(parsed,text,line,index=0):
    clearLineTags(text,line)
    definition,statement,value = initWords()
    for word in parsed:
        if word in definition:
            text.tag_add("definition","{0}.{1}".format(line,index),
                        "{0}.{1}".format(line,index+len(word)))
        elif word in statement:
            text.tag_add("statement","{0}.{1}".format(line,index),
                        "{0}.{1}".format(line,index+len(word)))
        elif word in value or isNumber(word):
            text.tag_add("value","{0}.{1}".format(line,index),
                        "{0}.{1}".format(line,index+len(word)))
        else:
            try:
                if type(eval(word)) == str:
                    text.tag_add("string","{0}.{1}".format(line,index),
                                "{0}.{1}".format(line,index+len(word)))
            except:
                pass
        index += len(word)

def isNumber(word):
    for c in word:
        if c not in string.digits:
            return False
    return True

#clears tags from beginning to end
def clearLineTags(text,line):
    text.tag_remove("definition","{0}.0".format(line),"{0}.end".format(line))
    text.tag_remove("statement","{0}.0".format(line),"{0}.end".format(line))
    text.tag_remove("value","{0}.0".format(line),"{0}.end".format(line))
    text.tag_remove("string","{0}.0".format(line),"{0}.end".format(line))
    text.tag_remove("comment","{0}.0".format(line),"{0}.end".format(line))
    text.tag_remove("openBracket","{0}.0".format(line),"{0}.end".format(line))

#clears tags in a certain range
def clearTagsRange(text,startIndex,endIndex):
    text.tag_remove("definition",startIndex,endIndex)
    text.tag_remove("statement",startIndex,endIndex)
    text.tag_remove("value",startIndex,endIndex)
    text.tag_remove("string",startIndex,endIndex)
    text.tag_remove("comment",startIndex,endIndex)
    text.tag_remove("openBracket",startIndex,endIndex)

def initWords():
    definition = set(["def", "class", "lambda", "abs", "dict", "help", "min",
            "setattr", "all", "dir ", "hex ", "next", "slice", "any ",
            "divmod", "id", "object", "sorted", "ascii", "enumerate",
            "input", "oct", "staticmethod", "bin", "eval", "int",
            "open", "str", "bool", "isinstance ", "ord", "sum",
            "bytearray", "filter", "issubclass ", "pow", "super",
            "bytes", "float", "iter", "tuple", "callable", "format",
            "len", "property", "type", "chr", "frozenset", "list",
            "range", "vars", "classmethod", "getattr", "locals",
            "repr", "zip", "compile ", "globals", "map", "reversed",
            "complex", "hasattr", "max", "round", "delattr",
            "hash", "memoryview", "set"])
    statement = set(["print", "exec", "and", "or", "not", "<", ">",
            "=", "!", "is", "in", "*", "/", "-", "+",
            "|", "^", "%", "~","from","import","return",
            "assert", "pass", "del", "yield", "raise", "break",
            "continue", "global", "nonlocal","for","while","if","else",
            "try","except","finally","with","elif"])
    value = set(["None", "True", "False", "NotImplemented", "Ellipsis"])
    return definition,statement,value

def initTags(text):
    text.tag_configure("exceed", underline = True)
    text.tag_configure("definition",foreground = "#64d6eb")
    text.tag_configure("statement",foreground = "#f92672")
    text.tag_configure("value",foreground = "#ae81ff")
    text.tag_configure("string",foreground = "#d7cc6c")
    text.tag_configure("comment",foreground = "#75715e")
    text.tag_configure("openBracket", background = "red")


################################
# bracket check

# loop through the text once and mark the unbalanced brackets using
# the Stack defined earlier. Takes time of O(n).
def checkBracket(text,start="1.0",end="end"):
    text.tag_remove("openBracket",start,end)
    content,stack,pairing,reverse = initBracket(text,start,end)
    for i in range(len(content)): #loop through text
        if ("string" not in text.tag_names("{0} +{1}c".format(start,i))
            and "comment" not in text.tag_names("{0} +{1}c".format(start,i))):
            #only check for brackets out of strings
            current = text.get("{0} +{1}c".format(start,i))
            if current in pairing: #if current is start of bracket
                stack.push((current,i)) #push into stack
            elif current in reverse: #if it is close bracket
                if stack.isEmpty():
                    #it is a unbalanced bracket if there is no start bracket
                    text.tag_add("openBracket","{0} +{1}c".format(start,i))
                else:
                    #check for matching bracket
                    if stack.peek()[0] != reverse[current][0]:
                        text.tag_add("openBracket","{0} +{1}c".format(start,i))
                    else:
                        stack.pop()
    #tag brackets if there are still brackets unmatched
    if not stack.isEmpty():
        for (c,i) in stack:
            text.tag_add("openBracket","{0} +{1}c".format(start,i))

def initBracket(text,start="1.0",end="end"):
    content = text.get(start,end)
    stack = Stack()
    pairing = {"[":"]","{":"}","(":")"}
    reverse = dict()
    for key in pairing:
        reverse[pairing[key]] = key
    return content,stack,pairing,reverse

################################
# defining Stack class/Exceptions for bracket matching
class EmptyStackError(Exception):
    def __init__(self):
            super().__init__("Stack is empty")

class FullStackError(Exception):
        def __init__(self):
                super().__init__("Stack is full")

class Stack(object):
        def __init__(self, maxSize=100):
            self.maxSize = maxSize
            self.data = []

        def isEmpty(self):
            if self.size() == 0:
                return True
            else:
                return False

        def isFull(self):
            if self.size() == self.maxSize:
                return True
            else:
                return False

        def push(self, data):
            if not self.isFull():
                self.data.append(data)
                return data
            else:
                raise FullStackError()

        def pop(self):
            if not self.isEmpty():
                output = self.data[self.size()-1]
                del self.data[self.size()-1]
                return output
            else:
                raise EmptyStackError()

        def size(self):
            return len(self.data)

        def peek(self):
            if self.isEmpty():
                raise EmptyStackError
            return self.data[self.size()-1]

        def __iter__(self):
            return iter(self.data)