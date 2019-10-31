import json
import re

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def jsonImplToObj(str):
    str = re.sub("(^StatusJSONImpl{)|(}}$)", "", str)

    values = []
    key = ""
    value = ""
    i = 0
    inkey = True
    instring = False
    while (i < len(str)):
        c = str[i]
        if (inkey):
            if (c == "="):
                inkey = False
                if (str[i+1]=="'"):
                    instring = True
                    i = i + 1
            else:
                key += c
        else:
            if (instring):
                if (c == "'"):
                    instring = False
                else:
                    value += c
            else:
                if (c == ","):
                    inkey = True
                    values.append((key, value))
                    key = ""
                    value = ""
                    if (str[i+1] == " "):
                        i = i + 1
                else:
                    value += c
            

        i = i + 1


    obj = {}
    for (key, value) in values:
        if (value == "false"):
            obj[key] = False
        elif (value == "true"):
            obj[key] = True
        elif (value == "null"):
            obj[key] = None
        elif (is_number(value)):
            obj[key] = float(value)
        else:
            obj[key] = value

    return obj

w = open("sport_test.json", "w")
with open("sports_orig.txt") as f:
    for line in f:
        try:
            w.write(line)
        except:
            if (not line.startswith("StatusJSONImpl")):
                print(line)
            obj = jsonImplToObj(line)
            w.write(json.dumps(obj))
        
