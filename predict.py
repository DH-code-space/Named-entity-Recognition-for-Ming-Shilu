from flair.data import Sentence
from flair.models import SequenceTagger
import re

tagger = SequenceTagger.load('best-model.pt')

with open('gpt4_training_data.txt', 'rt', encoding='utf-8') as fi, open('msl_ner_testing.txt', 'wt', encoding='utf-8') as fo:
  for line in fi:
    seg = line.strip().replace(' ', '　') # replace whitespace with special symbol
    sent = Sentence(' '.join([i for i in seg.strip()]), use_tokenizer=False)
    tagger.predict(sent)
    temp = []
    for ne in sent.get_labels():
        se = re.search("(?P<s>[0-9]+):(?P<e>[0-9]+)", str(ne))
        la = re.search("(?P<l> ? [A-Z]+)", str(ne))
        start = int(se.group("s"))
        end = int(se.group("e"))
        label = la.group("l")
        temp.append((start, end, label.strip()))
    temp.reverse()
    temp.sort(key=lambda a: a[0], reverse=True)
    for start, end, label in temp:
        if len(line[start:end].replace('　', ' ').strip()) != 0: # if NE is not whitespace(sometimes model will act weird.)
            line = line[:start] +"<"+label+">" + line[start:end] + "</" + label + ">" + line[end:]
    print(line.strip().replace('　', ' '), file=fo)