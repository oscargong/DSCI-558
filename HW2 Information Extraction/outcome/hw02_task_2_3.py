import re, sys,json
from copy import copy
from collections import namedtuple
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Token
from spacy import displacy


Film = namedtuple('Film',['title','year'])

def resolve_substring(input):
    l = sorted(input, key=len)
    export = []
    for index, item in enumerate(l):
        judge = []
        for sub_item in l[index + 1:]:
            if item not in sub_item:
                judge.append(True)
            else:
                judge.append(False)
        if all(judge):
            export.append(item)
    return export

# extract Person Entity
def person_ent_extract(input):
    if isinstance(input, list):
        if len(input) > 0:
            text = input[0]
        elif len(input) == 0:
            return []
    elif isinstance(input, str):
        text = copy(input)
    else:
        raise Exception("person_ent_extract, input type:", type(input))

    doc = nlp(text)
    matcher = Matcher(nlp.vocab)
    person_pattern = [{'ENT_TYPE': 'PERSON', 'OP': '+'}]
    matcher.add("person_entity", None, person_pattern)
    matches = matcher(doc)
    match_list = sorted([doc[s:e].text for _, s, e in matches], key=len)

    # l = match_list
    # resolve sub string:[j for i, j in enumerate(l) if all(j == k or (j not in k) for k in l[i + 1:])]
    export = resolve_substring(match_list)

    return export

def parent_lexical(text):
    # case 1
    # => father, {father_name} * mother,{mother_name}
    # father_re_pattern = r"(?: [Ff]ather.*?)([A-Z][\"\w \(\)]+)"
    # mother_re_pattern = r"(?: [Mm]other.*?)([A-Z][\"\w \(\)]+)"
    #
    # case1_mother = [match.group(1) for match in re.finditer(mother_re_pattern, text)]
    # case1_father = [match.group(1) for match in re.finditer(father_re_pattern, text)]
    case1_pattern = r"(?:\b[Mm]other|parent|[Ff]ather)\b(?:.*?)([A-Z][\"\w \(\)]+)"
    case1_result = [match.group(1) for match in re.finditer(case1_pattern, text) if len(match.group(1))< 30 ]

    # case 2
    # => {person_name} * born * to {parent_name} * and {parent_name}
    case2_re_pattern = r"born.+?to ([A-Z][\w \(\)]+)\b.+?and ([A-Z][\w \(\)]+)"
    case2_result = []
    for match in re.finditer(case2_re_pattern, text):
        if len(match.group(1))< 30:
            case2_result.append(match.group(1))
        if len(match.group(2)) < 30:
            case2_result.append(match.group(2))

    # case 3
    # => son|daughter * of {parent_name} * {parent_name}
    case3_re_pattern = r"\b(?:son|daughter|child)\b.*?of.*?([A-Z][\w \(\)]+).*?([A-Z][\w \(\)]+)"
    case3_result = []
    for match in re.finditer(case3_re_pattern, text):
        if len(match.group(1))< 30:
            case3_result.append(match.group(1))
        if len(match.group(2)) < 30:
            case3_result.append(match.group(2))

    parent_lexical_result = case1_result + case2_result + case3_result

    return parent_lexical_result



def parent_syntactic(text):
    text = nlp(text)
    sentences = list(text.sents)

    # case 1
    # => father, {father_name} * mother,{mother_name}
    case1_syntactic_result = []
    case1_re_pattern = r"(?:\b[Mm]other|parent|[Ff]ather)\b(?:.*?)([A-Z][\"\w \(\)]+)"

    for sentence in sentences:
        sentence_text = sentence.text
        if re.search(r"\b(father|mother)\b", sentence_text.lower()):
            case1_re_matches = [(match.start(), match.end()) for match in re.finditer(case1_re_pattern, sentence_text)]
            # expand a little bit
            expanded_case1_matches = [
                (start - 5, end + 5) if start - 5 >= 0 else (0, end + 5) for start, end in case1_re_matches
            ]
            for span in expanded_case1_matches:
                s, e = span
                slicy = sentence_text[s:e]
                case1_syntactic_result.extend(person_ent_extract(slicy))


    # case 2
    # => {person_name} * born * to {parent_name} * and {parent_name}
    case2_syntactic_result =[]
    case2_re_pattern = r"born.+?to ([A-Z][\w \(\)]+)\b.+?and ([A-Z][\w \(\)]+)"

    for sentence in sentences:
        sentence_text = sentence.text
        if re.search(r"\bborn.+?to", sentence_text.lower()):
            case2_re_matches = [(match.start(),match.end()) for match in re.finditer(case2_re_pattern, sentence_text)]
            # expand a little bit
            expanded_case2_matches = [
                (start-5,end+8) if start-5>=0 else (0,end+8) for start,end in case2_re_matches
            ]
            for span in expanded_case2_matches:
                s,e = span
                slicy = sentence_text[s:e]
                case2_syntactic_result.extend(person_ent_extract(slicy))


    # case 3
    # => son|daughter * of {parent_name} * {parent_name}
    case3_re_pattern = r"\b(?:son|daughter|child)\b.*?of.*?([A-Z][\w \(\)]+).*?([A-Z][\w \(\)]+)"
    case3_syntactic_result = []
    for sentence in sentences:
        sentence_text = sentence.text
        if re.search(r"\b(son|daughter|child)\b", sentence_text.lower()):
            case3_re_matches = [(match.start(),match.end()) for match in re.finditer(case3_re_pattern, sentence_text)]
            # expand a little bit
            expanded_case3_matches = [
                (start-5,end+8) if start-5>=0 else (0,end+8) for start,end in case3_re_matches
            ]
            for span in expanded_case3_matches:
                s, e = span
                slicy = sentence_text[s:e]
                case3_syntactic_result.extend(person_ent_extract(slicy))

    syntactic_result = case1_syntactic_result + case2_syntactic_result + case3_syntactic_result
    lexical_result = parent_lexical(text.text)

    lexical_result = sorted(lexical_result, key=len)

    combined = []
    for syn in sorted(syntactic_result, key=len):
        judge = []
        for lex in lexical_result:
            if syn in lex:
                if '(' in lex or ')' in lex:
                    combined.append(lex)
                    judge.append(False)
            else:
                judge.append(True)
        if all(judge):
            combined.append(syn)

    return(list(set(combined)))

def spouse_lexical(text):
    spouse_re_pattern = r"(?:married|engagement|wife).*?([A-Z]\w+ *[A-Z]*\w* *[A-Z]*\w*)"
    spouse_re_matches = [match.group(1) for match in re.finditer(spouse_re_pattern,text)]

    return spouse_re_matches

def spouse_syntactic(input):
    text = nlp(input)
    sentences = list(text.sents)

    pattern1 = [
        {"TEXT": {"REGEX": r'married|marry|engagement|engage|wife|husband'}},
        {'IS_ASCII': True, 'OP': '*'},
        {'ENT_TYPE': 'PERSON', 'OP': '+'},
        {'IS_PUNCT': True}
    ]
    spouse_matcher1 = Matcher(nlp.vocab)
    spouse_matcher1.add("spouse", None, pattern1)

    syntactic_matches = []
    for sentence in sentences:
        sentence_text = sentence.text.lower()
        t_nlp = nlp(sentence.text)
        if re.search(r'married|marry|engagement|engage|wife|husband',sentence_text):
            syntactic_matches.extend([t_nlp[s:e].text for _, s, e in spouse_matcher1(t_nlp)])
    syntactic_result = []
    for match in syntactic_matches:
        syntactic_result.extend(person_ent_extract(match))

    return list(set(syntactic_result))


def education_lexical(input):
    pattern1 = r"(School|College|University|Academy) (of) ([A-Z]\w+)"
    pattern2 = r"(?:[A-Z][^\s]*\s?)+ (School|College|University|Academy)"
    pattern1_match = [match.group() for match in re.finditer(pattern1, input)]
    pattern2_match = [match.group() for match in re.finditer(pattern2, input)]

    return pattern1_match + pattern2_match

def education_syntactic(input):
    text = nlp(input)
    sentences = list(text.sents)

    pattern = [{'ENT_TYPE': 'ORG', 'OP': '+'}]
    education_matcher = Matcher(nlp.vocab)
    education_matcher.add("education",None,pattern)
    syntactic_matches = []
    for sentence in sentences:
        t_nlp = nlp(sentence.text)
        if re.search(r'university|college|school|academy|husband', sentence.text.lower()):
            syntactic_matches.append([t_nlp[s:e].text for _, s, e in education_matcher(t_nlp)])
    syntactic_result = []
    for org in syntactic_matches:
        if org != []:
            syntactic_result.append(sorted(org, key=len)[-1])
    syntactic_result = resolve_substring(syntactic_result)
    return list(set(syntactic_result))


def starin_lexical(input):
    re_pattern = r"([A-Z][\w' .:-]{1,25})\((\d{4})\)"
    film_list =[]
    for match in re.finditer(re_pattern, input):
        film_list.append(
            Film(match.group(1),match.group(2))
        )
    film_list = sorted(film_list, key=lambda x: x.year)
    export = [film.title.strip() for film in film_list]
    return export

def starin_syntactic(input):
    """
    identical to starin_lexical
    """
    re_pattern = r"([A-Z\d][\w' .:-]{1,25})\((\d{4})\)"
    film_list =[]
    for match in re.finditer(re_pattern, input):
        film_list.append(
            Film(match.group(1),match.group(2))
        )
    film_list = sorted(film_list, key=lambda x: x.year)
    export = [film.title.strip() for film in film_list]
    return resolve_substring(export)


def debut_lexical(input):
    re_pattern = r"debut.*?([\w '-]+\(\d{4}\))"
    debut_match = []
    for match in re.finditer(re_pattern,input):
        debut_match.append(match.group(1))

    if debut_match:
        debut_match = debut_match[0]
        return starin_syntactic(debut_match)[0]
    else:
        starin_match = starin_syntactic(input)
        if starin_match:
            return starin_match[0]

def debut_syntactic(input):
    re_pattern = r"debut.*?([\w '-]+\(\d{4}\))"
    debut_match = []
    for match in re.finditer(re_pattern,input):
        debut_match.append(match.group(1))
    if debut_match:
        debut_match = debut_match[0]
        return starin_syntactic(debut_match)[0]
    else:
        starin_match = starin_syntactic(input)
        if starin_match:
            return starin_match[0]

if  __name__ == "__main__":
    input_file = sys.argv[1]
    print(" loadeding model")
    nlp = spacy.load('en_core_web_md')
    # nlp = spacy.load('en_core_web_sm')

    export_file_path = "/Users/oscar/Dropbox/1) Schoolwork/DSCI 558 Building Knowledge Graphs/Homework/HW2/submit/Ziheng_Gong_hw02_cast.jl"

    # input_file = '/Users/oscar/Dropbox/1) Schoolwork/DSCI 558 Building Knowledge Graphs/Homework/HW2/submit/Ziheng_Gong_hw02_bios.tsv'

    f_input_file = open(input_file, 'r')
    line_list = f_input_file.read().split('\n')
    f_output = open(export_file_path,"w+")
    count = 0
    for line in line_list:
        print(count)
        url,bio = line.split('\t')
        export_dict = dict()
        export_dict['url'] = url
        try:
            p = parent_syntactic(bio)
        except Exception:
            p =[]
        export_dict['parent'] = p

        try:
            db = debut_syntactic(bio)
        except Exception:
            db = ""
        export_dict['debuted_in'] = db

        try:
            star = starin_syntactic(bio)
        except Exception:
            star = []
        export_dict['starred_in'] = star
        try:
            sp = spouse_syntactic(bio)
        except Exception:
            sp = []
        export_dict['spouse'] = sp

        f_output.write(json.dumps(export_dict))
        f_output.write('\n')

        count += 1

