import json

tag_list = ["PER", "LOC", "WEI", "ORG", "OFF"]

with open('training_data_with_span.txt', 'rt', encoding='utf-8') as fi, open('dataset/train.txt', 'wt', encoding='utf-8') as fo:
    corpus = fi.read().strip().split("\n")
    counter = 0
    for paragraph in corpus:
        counter += 1
        if counter % 10 == 0:
            continue
        end = 0
        for i in range(len(paragraph)):
            if i < end:
                continue
            has_entity = False
            for tag in tag_list:
                if paragraph[i: i + 4] == "<" + tag:
                    has_entity = True
                    while paragraph[i] != ">":
                        i += 1
                    i += 1
                    fo.write(paragraph[i] + " " + "B-" + tag + "\n")
                    i += 1
                    if paragraph[i] == "<":
                        while paragraph[i] != ">":
                            i += 1
                        end = i + 1
                        continue
                    while paragraph[i + 1] != "<":
                        fo.write(paragraph[i] + " " + "I-" + tag + "\n")
                        i += 1
                    fo.write(paragraph[i] + " " + "E-" + tag + "\n")
                    while paragraph[i] != ">":
                        i += 1
                    end = i + 1
                    break
            if not has_entity:
                fo.write(paragraph[i] + " " + "O\n")
        fo.write('\n')

with open('training_data_with_span.txt', 'rt', encoding='utf-8') as fi, open('dataset/dev.txt', 'wt', encoding='utf-8') as fo:
    corpus = fi.read().strip().split("\n")
    counter = 0
    for paragraph in corpus:
        counter += 1
        if counter % 10 != 0:
            continue
        end = 0
        for i in range(len(paragraph)):
            if i < end:
                continue
            has_entity = False
            for tag in tag_list:
                if paragraph[i: i + 4] == "<" + tag:
                    has_entity = True
                    while paragraph[i] != ">":
                        i += 1
                    i += 1
                    fo.write(paragraph[i] + " " + "B-" + tag + "\n")
                    i += 1
                    if paragraph[i] == "<":
                        while paragraph[i] != ">":
                            i += 1
                        end = i + 1
                        continue
                    while paragraph[i + 1] != "<":
                        fo.write(paragraph[i] + " " + "I-" + tag + "\n")
                        i += 1
                    fo.write(paragraph[i] + " " + "E-" + tag + "\n")
                    while paragraph[i] != ">":
                        i += 1
                    end = i + 1
                    break
            if not has_entity:
                fo.write(paragraph[i] + " " + "O\n")
        fo.write('\n')

with open('testing_data_gt.json', 'rt', encoding='utf-8-sig') as fi, open('dataset/test.txt', 'wt', encoding='utf-8') as fo:
    corpus = [line["text"] for line in json.load(fi)]
    for paragraph in corpus:
        end = 0
        for i in range(len(paragraph)):
            if i < end:
                continue
            has_entity = False
            for tag in tag_list:
                if paragraph[i: i + 4] == "<" + tag:
                    has_entity = True
                    while paragraph[i] != ">":
                        i += 1
                    i += 1
                    fo.write(paragraph[i] + " " + "B-" + tag + "\n")
                    i += 1
                    if paragraph[i] == "<":
                        while paragraph[i] != ">":
                            i += 1
                        end = i + 1
                        continue
                    while paragraph[i + 1] != "<":
                        fo.write(paragraph[i] + " " + "I-" + tag + "\n")
                        i += 1
                    fo.write(paragraph[i] + " " + "E-" + tag + "\n")
                    while paragraph[i] != ">":
                        i += 1
                    end = i + 1
                    break
            if not has_entity:
                fo.write(paragraph[i] + " " + "O\n")
        fo.write('\n')
