import json
import re


# original_context_path = 'Dataset/training_data.txt'
original_context_path = 'Dataset/testing_data.txt'
# llm_output_path = 'Dataset/training_data_gpt4output.txt'
# llm_output_path = 'Dataset/testing_data_gpt3.5output.txt'
llm_output_path = 'Dataset/testing_data_gpt4output.txt'
# context_with_span_path = 'Dataset/training_data_with_span.txt'
context_with_span_path = 'Dataset/testing_data_with_span.txt'

predict_with_span = []
with open(original_context_path, 'rt', encoding='UTF-8') as fi1, open(llm_output_path, 'rt', encoding='UTF-8') as fi2, open(context_with_span_path, 'wt', encoding='UTF-8') as fo:
    origin = fi1.read().strip().replace("'", '"').split("\n")
    predict = fi2.read().strip().replace("'", '"').split("\n")
    predict = [json.loads(line) for line in predict]
    
    tags = []
    OFFICIAL = set()
    for line_origin, line_predict in zip(origin, predict):
        line_predict['LOC'], line_predict['WEI'], line_predict['ORG'] = [], [], []
        if line_predict['LOCWEIORG'][0] != "None":
            for entity in line_predict['LOCWEIORG']:
                entity = entity.split("(")
                if len(entity) == 1:
                    line_predict['OFFICIAL'].append(entity[0])
                elif entity[1][:-1] == "LOC":
                    line_predict['LOC'].append(entity[0])
                elif entity[1][:-1] == "WEI":
                    line_predict['WEI'].append(entity[0])
                elif entity[1][:-1] == "ORG":
                    line_predict['ORG'].append(entity[0])
                elif entity[1][:-1] == "PERSON":
                    line_predict['PERSON'].append(entity[0])
                elif entity[1][:-1] == "OFFICIAL":
                    line_predict['OFFICIAL'].append(entity[0])
        if len(line_predict['LOC']) == 0:
            line_predict['LOC'].append("None")
        if len(line_predict['WEI']) == 0:
            line_predict['WEI'].append("None")
        if len(line_predict['ORG']) == 0:
            line_predict['ORG'].append("None")
        
        if line_predict['PERSON'][0] != "None":
            person_after_processing = []
            for entity in line_predict['PERSON']:
                if len(entity) > 3 and len(entity.split("子")) == 2 and entity.split("子")[0] != "" and entity.split("子")[1] != "":
                    person_after_processing.append(entity.split("子")[0])
                    person_after_processing.append(entity.split("子")[1])
                elif len(entity) > 3 and len(entity.split("弟")) == 2 and entity.split("弟")[0] != "" and entity.split("弟")[1] != "":
                    person_after_processing.append(entity.split("弟")[0])
                    person_after_processing.append(entity.split("弟")[1])
                elif len(entity) > 3 and len(entity.split("姪")) == 2 and entity.split("姪")[0] != "" and entity.split("姪")[1] != "":
                    person_after_processing.append(entity.split("姪")[0])
                    person_after_processing.append(entity.split("姪")[1])
                else:
                    entity = entity.split("(")
                    if len(entity) == 1:
                        person_after_processing.append(entity[0])
                    elif entity[1][:-1] == "LOC":
                        line_predict['LOC'].append(entity[0])
                    elif entity[1][:-1] == "WEI":
                        line_predict['WEI'].append(entity[0])
                    elif entity[1][:-1] == "ORG":
                        line_predict['ORG'].append(entity[0])
                    elif entity[1][:-1]  == "OFFICIAL":
                        line_predict['OFFICIAL'].append(entity[0])
            line_predict['PERSON'] = person_after_processing

        if line_predict['OFFICIAL'][0] != "None":
            officical_after_processing = []
            for entity in line_predict['OFFICIAL']:
                if len(entity.split("兼")) == 2 and entity.split("兼")[0] != "" and entity.split("兼")[1] != "":
                    officical_after_processing.append(entity.split("兼")[0])
                    officical_after_processing.append(entity.split("兼")[1])
                else:
                    officical_after_processing.append(entity)
            line_predict['OFFICIAL'] = officical_after_processing

        loc_dic = ['直隸', '南直隸', '北直隸', '山東', '山西', '河南', '陝西', '陜西', '四川', '江西', '湖廣', '浙江', '福建', '廣東', '廣西', '雲南', '貴州', '交趾', '薊鎮', '延綏', '寧夏', '鳳陽', '遼東', '海西', '甘肅', '大同', '固原', '石匣']

        if line_predict['LOC'][0] != "None":
            loc_after_processing = []
            for entity in line_predict['LOC']:
                if len(entity) > 3 and re.search("[司路]", entity) == None:
                    nested = False
                    for loc in loc_dic:
                        if re.search('^' + loc, entity) != None:
                            loc_after_processing.append(entity[:re.search('^' + loc, entity).end()])
                            loc_after_processing.append(entity[re.search('^' + loc, entity).end():])
                            nested = True
                            break
                    if not nested:
                        loc_after_processing.append(entity)
                else:
                    loc_after_processing.append(entity)
            line_predict['LOC'] = loc_after_processing

        if line_predict['WEI'][0] != "None":
            loc_after_processing, wei_after_processing = [], []
            if line_predict['LOC'][0] != "None":
                for entity in line_predict['LOC']:
                    loc_after_processing.append(entity)
            for entity in line_predict['WEI']:
                if len(entity) > 4 and re.search("[司路]", entity) == None:
                    nested = False
                    for loc in loc_dic:
                        if re.search('^' + loc, entity) != None:
                            loc_after_processing.append(entity[:re.search('^' + loc, entity).end()])
                            wei_after_processing.append(entity[re.search('^' + loc, entity).end():])
                            nested = True
                            break
                    if not nested:
                        wei_after_processing.append(entity)
                else:
                    wei_after_processing.append(entity)
            if len(loc_after_processing) == 0:
                loc_after_processing.append("None")
            line_predict['LOC'] = loc_after_processing
            line_predict['WEI'] = wei_after_processing

        if line_predict['LOC'][0] != "None":
            loc_after_processing = []
            for entity in line_predict['LOC']:
                if re.search("[府縣州]", entity) != None and re.search("[府縣州]", entity).end() + 1 < len(entity):
                    loc_after_processing.append(entity[:re.search("[府縣州]", entity).end()])
                    loc_after_processing.append(entity[re.search("[府縣州]", entity).end():])
                else:
                    loc_after_processing.append(entity)
            line_predict['LOC'] = loc_after_processing
        
        if line_predict['LOC'][0] != "None":
            loc_after_processing = []
            for entity in line_predict['LOC']:
                if re.search("[府縣州]", entity) != None and re.search("[府縣州]", entity).end() + 1 < len(entity):
                    loc_after_processing.append(entity[:re.search("[府縣州]", entity).end()])
                    loc_after_processing.append(entity[re.search("[府縣州]", entity).end():])
                else:
                    loc_after_processing.append(entity)
            line_predict['LOC'] = loc_after_processing

        line_predict['PERSON'] = sorted(list(set(line_predict['PERSON'])), key=lambda ne : len(ne), reverse=True)
        line_predict['LOC'] = sorted(list(set(line_predict['LOC'])), key=lambda ne : len(ne), reverse=True)
        line_predict['WEI'] = sorted(list(set(line_predict['WEI'])), key=lambda ne : len(ne), reverse=True)
        line_predict['ORG'] = sorted(list(set(line_predict['ORG'])), key=lambda ne : len(ne), reverse=True)
        line_predict['OFFICIAL'] = sorted(list(set(line_predict['OFFICIAL'])), key=lambda ne : len(ne), reverse=True)

        line_predict['LOCWEIORG'] = []
        if line_predict['LOC'][0] != "None":
            for entity in line_predict['LOC']:
                line_predict['LOCWEIORG'].append(entity + "-LOC")
        if line_predict['WEI'][0] != "None":
            for entity in line_predict['WEI']:
                line_predict['LOCWEIORG'].append(entity + "-WEI")
        if line_predict['ORG'][0] != "None":
            for entity in line_predict['ORG']:
                line_predict['LOCWEIORG'].append(entity + "-ORG")
        if len(line_predict['LOCWEIORG']) == 0:
            line_predict['LOCWEIORG'].append("None")
        line_predict['LOCWEIORG'] = sorted(line_predict['LOCWEIORG'], key=lambda ne : len(ne), reverse=True)
        
        line_tags = ['O'] * len(line_origin)

        if line_predict['PERSON'][0] != "None":
            for person in line_predict['PERSON']:
                for match in re.finditer(person, line_origin):
                    duplicate = False
                    for i in range(match.start(), match.end()):
                        if line_tags[i] != "O":
                            duplicate = True
                            break
                    if not duplicate:
                        line_tags[match.end() - 1] = "E-PER"
                        line_tags[match.start()] = "B-PER"
                        for i in range(match.start() + 1, match.end() - 1):
                            line_tags[i] = "I-PER"

        if line_predict['LOCWEIORG'][0] != "None":
            for entity in line_predict['LOCWEIORG']:
                entity, tag = entity.split("-")
                if (tag == "LOC" or tag == "WEI") and re.search(entity, line_origin) == None and len(entity) >= 2:
                    if entity[-3:] == "安撫司":
                        entity = entity[:-3]
                    elif entity[-1:] == "關" and re.search(entity[:-1] + "関", line_origin) != None:
                        entity = entity[:-1] + "関"
                    else:
                        entity = entity[:-1]
                elif tag == "WEI" and re.search("^[一二三四五六七八九十]+[衛衞]$", entity) != None or re.search("[本原]", entity) != None:
                    continue
                elif tag == "WEI" and re.search("等?[一二三四五六七八九十]+[衛衞]$", entity) != None:
                    entity = entity[:re.search("等?[一二三四五六七八九十]+[衛衞]$", entity).start()]
                elif re.search("按察司", entity) != None:
                    tag = "ORG"
                elif re.search("都察院", entity) != None:
                    tag = "ORG"
                elif re.search("都督府", entity) != None:
                    tag = "WEI"
                elif re.search("布政司", entity) != None:
                    if re.search("^布政司$", entity) == None:
                        tag = "LOC"
                elif re.search("[廵巡]檢司", entity) != None:
                    if re.search("^[廵巡]檢司$", entity) == None:
                        tag = "LOC"
                    else:
                        tag = "ORG"
                elif re.search("布政使司", entity) != None:
                    if re.search("^布政使司$", entity) == None:
                        tag = "LOC"
                elif re.search("營$", entity) != None:
                    tag = "WEI"
                elif re.search("府$", entity) != None:
                    tag = "LOC"
                for match in re.finditer(entity, line_origin):
                    duplicate = False
                    for i in range(match.start(), match.end()):
                        if line_tags[i] != "O":
                            duplicate = True
                            break
                    if not duplicate:
                        line_tags[match.end() - 1] = "E-" + tag
                        line_tags[match.start()] = "B-" + tag
                        for i in range(match.start() + 1, match.end() - 1):
                            line_tags[i] = "I-" + tag

        for match in re.finditer("南[吏戶禮兵刑工六][部科]", line_origin):
            if line_tags[match.start()] == "O":
                line_predict['LOCWEIORG'].append(match.group() + "-ORG")
                line_tags[match.start()] = "B-ORG"
                line_tags[match.start() + 1] = "I-ORG"
                line_tags[match.start() + 2] = "E-ORG"
        for match in re.finditer("[吏戶禮兵刑工六][部科]", line_origin):
            if line_tags[match.start()] == "O":
                line_predict['LOCWEIORG'].append(match.group() + "-ORG")
                line_tags[match.start()] = "B-ORG"
                line_tags[match.start() + 1] = "E-ORG"
        line_predict['LOCWEIORG'] = sorted(line_predict['LOCWEIORG'], key=lambda ne : len(ne), reverse=True)
        
        if line_predict['PERSON'][0] != "None":
            for person in line_predict['PERSON']:
                if len(person) >= 2:
                    person = person[1:]
                if person in line_predict['OFFICIAL']:
                    for match in re.finditer(person, line_origin):
                        duplicate = False
                        for i in range(match.start(), match.end()):
                            if line_tags[i] != "O":
                                duplicate = True
                                break
                        if not duplicate:
                            line_tags[match.end() - 1] = "E-PER"
                            line_tags[match.start()] = "B-PER"
                            for i in range(match.start() + 1, match.end() - 1):
                                line_tags[i] = "I-PER"

        if line_predict['OFFICIAL'][0] != "None":
            official_after_processing = []
            for official in line_predict['OFFICIAL']:
                if line_predict['LOCWEIORG'][0] != "None":
                    nested = False
                    for entity in line_predict['LOCWEIORG']:
                        entity, tag = entity.split("-")
                        if official != entity and re.search("^" + entity, official) != None:
                            official_after_processing.append(official[re.search("^" + entity, official).end():])
                            nested = True
                    if not nested:
                        official_after_processing.append(official)
                else:
                    official_after_processing.append(official)
            if len(official_after_processing) == 0:
                official_after_processing.append("None")
            line_predict['OFFICIAL'] = sorted(official_after_processing, key=lambda ne : len(ne), reverse=True)

        if line_predict['OFFICIAL'][0] != "None":
            for official in line_predict['OFFICIAL']:
                if re.search("[科部寺院]$", official) != None:
                    for match in re.finditer(official, line_origin):
                        duplicate = False
                        for i in range(match.start(), match.end()):
                            if line_tags[i] != "O":
                                duplicate = True
                                break
                        if not duplicate:
                            line_tags[match.end() - 1] = "E-ORG"
                            line_tags[match.start()] = "B-ORG"
                            for i in range(match.start() + 1, match.end() - 1):
                                line_tags[i] = "I-ORG"
                    continue
                if re.search("^[廵巡]檢司$", official) != None or re.search("^布政司$", official) != None:
                    for match in re.finditer(official, line_origin):
                        duplicate = False
                        for i in range(match.start(), match.end()):
                            if line_tags[i] != "O":
                                duplicate = True
                                break
                        if not duplicate:
                            line_tags[match.end() - 1] = "E-ORG"
                            line_tags[match.start()] = "B-ORG"
                            for i in range(match.start() + 1, match.end() - 1):
                                line_tags[i] = "I-ORG"
                        continue
                if re.search("都督府", official) != None and re.search("^都督府$", official) == None:
                    for match in re.finditer(official[:re.search("都督府", official).end()], line_origin):
                        duplicate = False
                        for i in range(match.start(), match.end()):
                            if line_tags[i] != "O":
                                duplicate = True
                                break
                        if not duplicate:
                            line_tags[match.end() - 1] = "E-WEI"
                            line_tags[match.start()] = "B-WEI"
                            for i in range(match.start() + 1, match.end() - 1):
                                line_tags[i] = "I-WEI"
                    official = official[re.search("都督府", official).end():]
                for match in re.finditer(official, line_origin):
                    if 3 < len(official) < 9 and re.search("[衛衞營]", official) != None:
                        if line_tags[match.start() - 1] == "E-LOC":
                            line_tags[match.start() + re.search("[衛衞營]", official).start()] = "E-WEI"
                            curr_pos = match.start() + re.search("[衛衞營]", official).start() - 1
                            while line_tags[curr_pos] != "B-LOC":
                                line_tags[curr_pos] = "I-WEI"
                                curr_pos -= 1
                            line_tags[curr_pos] = "B-WEI"
                        else:
                            duplicate = False
                            for i in range(match.start(), match.end()):
                                if line_tags[i] != "O":
                                    duplicate = True
                                    break
                            if not duplicate:
                                line_tags[match.start() + re.search("[衛衞營]", official).start()] = "E-WEI"
                                curr_pos = match.start() + re.search("[衛衞營]", official).start() - 1
                                while curr_pos > match.start():
                                    line_tags[curr_pos] = "I-WEI"
                                    curr_pos -= 1
                                line_tags[curr_pos] = "B-WEI"
                    if re.search("[司衛衞府營]$", official) == None:
                        OFFICIAL.add(official)
                    duplicate = False
                    for i in range(match.start(), match.end()):
                        if line_tags[i] != "O":
                            duplicate = True
                            break
                    if not duplicate:
                        line_tags[match.end() - 1] = "E-OFF"
                        line_tags[match.start()] = "B-OFF"
                        for i in range(match.start() + 1, match.end() - 1):
                            line_tags[i] = "I-OFF"
                    elif re.search("[衛衞]", official) != None:
                        duplicate = False
                        for i in range(match.start() + re.search("[衛衞]", official).end(), match.end()):
                            if line_tags[i] != "O":
                                duplicate = True
                                break
                        if not duplicate:
                            line_tags[match.end() - 1] = "E-OFF"
                            line_tags[match.start() + re.search("[衛衞]", official).end()] = "B-OFF"
                            for i in range(match.start() + re.search("[衛衞]", official).end() + 1, match.end() - 1):
                                line_tags[i] = "I-OFF"
        
        for match in re.finditer("[一二三四五六七八九十等諸各]+[衛衞]", line_origin):
            if line_tags[match.start()] != "B-LOC" and line_tags[match.start()] != "I-LOC" and line_tags[match.start()] != "E-LOC":
                curr, pivot = match.start(), match.start()
                while curr >= 0 and line_origin[curr] != "，" and line_origin[curr] != "。" and line_origin[curr] != "：":
                    if line_origin[curr] == "、":
                        pivot = curr
                    curr -= 1
                for i in range(pivot, match.start()):
                    line_tags[i] = line_tags[i].replace("LOC", "WEI")
                pivot -= 1
                while line_tags[pivot] != "O":
                    if line_tags[pivot].split("-")[1] == "LOC":
                        line_tags[pivot] = line_tags[pivot].replace("LOC", "WEI")
                    else:
                        break
                    pivot -= 1

        for match in re.finditer("右", line_origin):
            if line_tags[match.start()] == "O":
                if match.start() + 1 < len(line_origin) and line_tags[match.start() + 1] == "B-OFF":
                    if match.start() + 2 < len(line_origin) and line_tags[match.start() + 1] == "O":
                        line_tags[match.start() + 1] = "E-OFF"
                    else:
                        line_tags[match.start() + 1] = "I-OFF"
                    line_tags[match.start()] = "B-OFF"
        for match in re.finditer("左", line_origin):
            if line_tags[match.start()] == "O":
                if match.start() + 1 < len(line_origin) and line_tags[match.start() + 1] == "B-OFF":
                    if match.start() + 2 < len(line_origin) and line_tags[match.start() + 1] == "O":
                        line_tags[match.start() + 1] = "E-OFF"
                    else:
                        line_tags[match.start() + 1] = "I-OFF"
                    line_tags[match.start()] = "B-OFF"
                elif match.start() - 1 >= 0 and line_tags[match.start() - 1] == "E-WEI":
                    line_tags[match.start()] = "E-WEI"
                    line_tags[match.start() - 1] = "I-WEI"
                elif match.start() - 1 >= 0 and line_tags[match.start() - 1] == "B-WEI":
                    line_tags[match.start()] = "E-WEI"
        for match in re.finditer("右", line_origin):
            if line_tags[match.start()] == "O":
                if match.start() - 1 >= 0 and line_tags[match.start() - 1] == "E-WEI":
                    line_tags[match.start()] = "E-WEI"
                    line_tags[match.start() - 1] = "I-WEI"
                elif match.start() - 1 >= 0 and line_tags[match.start() - 1] == "B-WEI":
                    line_tags[match.start()] = "E-WEI"

        if line_predict['PERSON'][0] != "None":
            for person in line_predict['PERSON']:
                if len(person) >= 2 and re.search(person, line_origin) != None:
                    first_time_pos = re.search(person, line_origin).start()
                    for match in re.finditer(person[1:], line_origin):
                        duplicate = False
                        for i in range(match.start(), match.end()):
                            if line_tags[i] != "O":
                                duplicate = True
                                break
                        if not duplicate and match.start() > first_time_pos:
                            line_tags[match.end() - 1] = "E-PER"
                            line_tags[match.start()] = "B-PER"
                            for i in range(match.start() + 1, match.end() - 1):
                                line_tags[i] = "I-PER"
        
        tags.append(line_tags)

    for line_origin, line_predict, line_tags in zip(origin, predict, tags):
        if line_predict['LOCWEIORG'][0] != "None":
            for entity in line_predict['LOCWEIORG']:
                entity, tag = entity.split("-")
                if entity in OFFICIAL or re.search("侯$", entity) != None or re.search("伯$", entity) != None or re.search("殿大學士$", entity) != None or re.search("閣大學士$", entity) != None:
                    for match in re.finditer(entity, line_origin):
                        if line_tags[match.start()].split("-")[0] == "B" and line_tags[match.end() - 1].split("-")[0] == "E":
                            line_tags[match.end() - 1] = "E-OFF"
                            line_tags[match.start()] = "B-OFF"
                            for i in range(match.start() + 1, match.end() - 1):
                                line_tags[i] = "I-OFF"
                else:
                    split_pos = len(entity)
                    for official in OFFICIAL:
                        if len(official) >= 2 and re.search(official + '$', entity) != None:
                            temp_pos = re.search(official + '$', entity).start()
                            if split_pos > temp_pos:
                                split_pos = temp_pos
                    if split_pos != len(entity) and split_pos >= 2:
                        for match in re.finditer(entity, line_origin):
                            if line_tags[match.start()].split("-")[0] == "B" and line_tags[match.end() - 1].split("-")[0] == "E":
                                if tag == "WEI" and re.search("[衛衞司]", entity) == None:
                                    tag = "LOC"
                                line_tags[match.start() + split_pos - 1] = "E-" + tag
                                line_tags[match.start()] = "B-" + tag
                                for i in range(match.start() + 1, match.start() + split_pos - 1):
                                    line_tags[i] = "I-" + tag
                                line_tags[match.end() - 1] = "E-OFF"
                                line_tags[match.start() + split_pos] = "B-OFF"
                                for i in range(match.start() + 1 + split_pos, match.end() - 1):
                                    line_tags[i] = "I-OFF"
            for match in re.finditer("入?[衛衞]", line_origin):
                if line_tags[match.start()] == "O" and (line_tags[match.start() - 1] == "E-LOC" or line_tags[match.start() - 1] == "E-WEI"):
                    line_tags[match.end() - 1] = "E-WEI"
                    curr_pos = match.end() - 2
                    while line_tags[curr_pos].split("-")[0] != "B":
                        line_tags[curr_pos] = "I-WEI"
                        curr_pos -= 1
                    line_tags[curr_pos] = "B-WEI"
            for match in re.finditer("堡", line_origin):
                if line_tags[match.start()] == "E-WEI":
                    curr_pos = match.start()
                    while line_tags[curr_pos].split("-")[0] != "B":
                        line_tags[curr_pos] = line_tags[curr_pos].replace("WEI", "LOC")
                        curr_pos -= 1
                    line_tags[curr_pos] = line_tags[curr_pos].replace("WEI", "LOC")
            for match in re.finditer("按察司", line_origin):
                if (line_tags[match.start()] == "O" or line_tags[match.start()] == "B-ORG") and line_tags[match.start() - 1] == "E-LOC":
                    line_tags[match.start() + 2] = "E-ORG"
                    curr_pos = match.start() + 1
                    while line_tags[curr_pos] != "B-LOC":
                        line_tags[curr_pos] = "I-ORG"
                        curr_pos -= 1
                    line_tags[curr_pos] = "B-ORG"
            for match in re.finditer("[等諸各][衛衞]", line_origin):
                if line_tags[match.start()] == "O" and line_tags[match.start() + 1] == "O" and line_tags[match.start() - 1] == "E-WEI":
                    line_tags[match.start() + 1] = "E-WEI"
                    curr_pos = match.start()
                    while line_tags[curr_pos] != "B-WEI":
                        line_tags[curr_pos] = "I-WEI"
                        curr_pos -= 1
                    line_tags[curr_pos] = "B-WEI"
            for match in re.finditer("署", line_origin):
                if (line_tags[match.start()] == "E-WEI" or line_tags[match.start()] == "O") and line_tags[match.start() + 1] == "B-OFF":
                    if line_tags[match.start()] == "E-WEI":
                        line_tags[match.start() - 1] = "E-WEI"
                    line_tags[match.start()] = "B-OFF"
                    if line_tags[match.start() + 2] != "I-OFF" and line_tags[match.start() + 2] != "E-OFF":
                        line_tags[match.start() + 1] = "E-OFF"
                    else:
                        line_tags[match.start() + 1] = "I-OFF"
            for match in re.finditer("南京", line_origin):
                if line_tags[match.start() + 1] == "E-LOC" and line_tags[match.start() + 2] == "B-ORG":
                    line_tags[match.start()] = "B-ORG"
                    line_tags[match.start() + 1] = "I-ORG"
                    line_tags[match.start() + 2] = "I-ORG"
            for match in re.finditer("行都司", line_origin):
                if line_tags[match.start() - 1] == "E-LOC":
                    line_tags[match.start() + 2] = "E-WEI"
                    curr_pos = match.start() + 1
                    while line_tags[curr_pos] != "B-LOC":
                        line_tags[curr_pos] = "I-WEI"
                        curr_pos -= 1
                    line_tags[curr_pos] = "B-WEI"
            for match in re.finditer("都司", line_origin):
                if line_tags[match.start() - 1] == "E-LOC":
                    line_tags[match.start() + 1] = "E-WEI"
                    curr_pos = match.start()
                    while line_tags[curr_pos] != "B-LOC":
                        line_tags[curr_pos] = "I-WEI"
                        curr_pos -= 1
                    line_tags[curr_pos] = "B-WEI"
            for match in re.finditer("營", line_origin):
                if line_tags[match.start()] == "O" and line_tags[match.start() - 2] == "E-LOC":
                    line_tags[match.start()] = "E-WEI"
                    curr_pos = match.start() - 1
                    while line_tags[curr_pos] != "B-LOC":
                        line_tags[curr_pos] = "I-WEI"
                        curr_pos -= 1
                    line_tags[curr_pos] = "B-WEI"
            for match in re.finditer("道", line_origin):
                if line_tags[match.start()] == "O" and line_tags[match.start() - 1] == "E-LOC":
                    line_tags[match.start()] = "E-LOC"
                    line_tags[match.start() - 1] = "I-LOC"
            for match in re.finditer("大學士", line_origin):
                if line_tags[match.start() - 1] == "E-ORG":
                    line_tags[match.start() + 2] = "E-OFF"
                    curr_pos = match.start() + 1
                    while line_tags[curr_pos] != "B-ORG":
                        line_tags[curr_pos] = "I-OFF"
                        curr_pos -= 1
                    line_tags[curr_pos] = "B-OFF"
            for match in re.finditer("[侯伯]", line_origin):
                if line_tags[match.start() - 1] == "E-LOC":
                    line_tags[match.start()] = "E-OFF"
                    curr_pos = match.start() - 1
                    while line_tags[curr_pos] != "B-LOC":
                        line_tags[curr_pos] = "I-OFF"
                        curr_pos -= 1
                    line_tags[curr_pos] = "B-OFF"
            for match in re.finditer("守禦千戶所", line_origin):
                if line_tags[match.start() - 1] == "E-LOC":
                    line_tags[match.start() + 4] = "E-WEI"
                    curr_pos = match.start() + 3
                    while line_tags[curr_pos] != "B-LOC":
                        line_tags[curr_pos] = "I-WEI"
                        curr_pos -= 1
                    line_tags[curr_pos] = "B-WEI"
            for match in re.finditer("千戶所", line_origin):
                if line_tags[match.start() - 1] == "E-LOC":
                    line_tags[match.start() + 2] = "E-WEI"
                    curr_pos = match.start() + 1
                    while line_tags[curr_pos] != "B-LOC":
                        line_tags[curr_pos] = "I-WEI"
                        curr_pos -= 1
                    line_tags[curr_pos] = "B-WEI"
            for match in re.finditer("[一二三四五六七八九十等諸各]+守禦千戶所", line_origin):
                curr, pivot = match.start(), match.start()
                while curr >= 0 and line_origin[curr] != "，" and line_origin[curr] != "。" and line_origin[curr] != "：":
                    if line_origin[curr] == "、":
                        pivot = curr
                    curr -= 1
                for i in range(pivot, match.start()):
                    line_tags[i] = line_tags[i].replace("LOC", "WEI")
                pivot -= 1
                while line_tags[pivot] != "O":
                    if line_tags[pivot].split("-")[1] == "LOC":
                        line_tags[pivot] = line_tags[pivot].replace("LOC", "WEI")
                    else:
                        break
                    pivot -= 1
            for match in re.finditer("[一二三四五六七八九十等諸各]+千戶所", line_origin):
                curr, pivot = match.start(), match.start()
                while curr >= 0 and line_origin[curr] != "，" and line_origin[curr] != "。" and line_origin[curr] != "：":
                    if line_origin[curr] == "、":
                        pivot = curr
                    curr -= 1
                for i in range(pivot, match.start()):
                    line_tags[i] = line_tags[i].replace("LOC", "WEI")
                pivot -= 1
                while line_tags[pivot] != "O":
                    if line_tags[pivot].split("-")[1] == "LOC":
                        line_tags[pivot] = line_tags[pivot].replace("LOC", "WEI")
                    else:
                        break
                    pivot -= 1

        line_with_span, current_span = "", "O"
        for i in range(len(line_origin)):
            tag = line_tags[i].split("-")
            if tag[0] == "B":
                if current_span != "O":
                    line_with_span += "</" + current_span + ">"
                    current_span = "O"
                line_with_span += "<" + tag[1] + ">" + line_origin[i]
                current_span = tag[1]
            elif tag[0] == "I":
                line_with_span += line_origin[i]
            elif tag[0] == "E":
                line_with_span += line_origin[i] + "</" + tag[1] + ">"
                current_span = "O"
            else:
                if current_span != "O":
                    line_with_span += "</" + current_span + ">"
                    current_span = "O"
                line_with_span += line_origin[i]
        predict_with_span.append(line_with_span)

    for line_with_span in predict_with_span:
        fo.write(line_with_span + "\n")
