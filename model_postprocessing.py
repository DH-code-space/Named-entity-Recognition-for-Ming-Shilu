import re

with open('ner.txt', 'rt', encoding='UTF-8') as fi, open('ner_fixed.txt', 'wt', encoding='UTF-8') as fo:
    whole = fi.read().split('\n')
    for line in whole:
        for match in reversed(list(re.finditer("<LOC>(.?)</LOC><WEI>(.?)</WEI>", line))):
            start, end = match.start(), match.end()
            line = line[:start] + line[start:end].replace("</LOC><WEI>", "").replace("</WEI>", "</LOC>") + line[end:]
        for match in reversed(list(re.finditer("<WEI>(.?)</WEI><LOC>(.?)</LOC>", line))):
            start, end = match.start(), match.end()
            line = line[:start] + line[start:end].replace("</WEI><LOC>", "").replace("<WEI>", "<LOC>") + line[end:]
        for match in reversed(list(re.finditer("<ORG>(.?)</ORG><(LOC|WEI)>(.?)</(LOC|WEI)><ORG>", line))):
            start, end = match.start(), match.end()
            line = line[:start] + "<ORG>" + re.sub("<[A-Z/]+>", "", line[start:end]) + line[end:]
        for match in reversed(list(re.finditer("<(LOC|WEI|ORG)>(.?)</(LOC|WEI|ORG)><", line))):
            start, end = match.start(), match.end()
            line = line[:start] + line[end - 1:end + 4] + re.sub("<[A-Z/]+>", "", line[start:end - 1]) + line[end + 4:]
        for match in re.finditer("王</PER>", line):
            start, end = match.start(), match.end()
            while line[start] != "<":
                start -= 1
            line = line[:start] + "<OFF>" + re.sub("<[A-Z/]+>", "", line[start:end]) + "</OFF>" + line[end:]
        for match in re.finditer("[王侯公伯]</(LOC|WEI|ORG)>", line):
            start, end = match.start(), match.end()
            while line[start] != "<":
                start -= 1
            line = line[:start] + "<OFF>" + re.sub("<[A-Z/]+>", "", line[start:end]) + "</OFF>" + line[end:]
        for match in re.finditer("[王侯公伯]</(LOC|WEI|ORG)>", line):
            start, end = match.start(), match.end()
            while line[start] != "<":
                start -= 1
            line = line[:start] + "<OFF>" + re.sub("<[A-Z/]+>", "", line[start:end]) + "</OFF>" + line[end:]
        for match in re.finditer("殿</(WEI|ORG)>", line):
            start, end = match.start(), match.end()
            while line[start] != "<":
                start -= 1
            line = line[:start] + "<LOC>" + re.sub("<[A-Z/]+>", "", line[start:end]) + "</LOC>" + line[end:]
        for match in reversed(list(re.finditer("<(WEI|ORG)>(等|各)", line))):
            start, end = match.start(), match.end()
            while line[end] != ">":
                end += 1
            line = line[:start] + re.sub("<[A-Z/]+>", "", line[start:end]) + line[end:]
        for match in re.finditer("司</OFF>", line):
            start, end = match.start(), match.end()
            while line[start] != "<":
                start -= 1
            line = line[:start] + "<ORG>" + re.sub("<[A-Z/]+>", "", line[start:end]) + "</ORG>" + line[end:]
        line = line.replace("<ORG>司</ORG>", "司")
        fo.write(line + '\n')
