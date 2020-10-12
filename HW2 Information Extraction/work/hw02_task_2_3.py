import re, sys
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
    # input_file = sys.argv[1]
    nlp = spacy.load('en_core_web_md')
    # nlp = spacy.load('en_core_web_sm')
    print("model loaded")

    export_file_path = "./Ziheng_Gong_hw02_cast.jl"

    text = """
    "Johnny Depp is perhaps one of the most versatile actors of his day and age in Hollywood.
    
    He was born John Christopher Depp II in Owensboro, Kentucky, on June 9, 1963, to Betty Sue (Wells), who worked as a waitress, and John Christopher Depp, a civil engineer.
    
    Depp was raised in Florida. He dropped out of school when he was 15, and fronted a series of music-garage bands, including one named 'The Kids'. When he married Lori Anne Allison (Lori A. Depp) he took a job as a ballpoint-pen salesman to support himself and his wife. A visit to Los Angeles, California, with his wife, however, happened to be a blessing in disguise, when he met up with actor Nicolas Cage, who advised him to turn to acting, which culminated in Depp's film debut in the low-budget horror film, A Nightmare on Elm Street (1984), where he played a teenager who falls prey to dream-stalking demon Freddy Krueger.
    
    In 1987 he shot to stardom when he replaced Jeff Yagher in the role of undercover cop Tommy Hanson in the popular TV series 21 Jump Street (1987).
    
    In 1990, after numerous roles in teen-oriented films, his first of a handful of great collaborations with director Tim Burton came about when Depp played the title role in Edward Scissorhands (1990). Following the film's success, Depp carved a niche for himself as a serious, somewhat dark, idiosyncratic performer, consistently selecting roles that surprised critics and audiences alike. He continued to gain critical acclaim and increasing popularity by appearing in many features before re-joining with Burton in the lead role of Ed Wood (1994). In 1997 he played an undercover FBI agent in the fact-based film Donnie Brasco (1997), opposite Al Pacino; in 1998 he appeared in Fear and Loathing in Las Vegas (1998), directed by Terry Gilliam; and then, in 1999, he appeared in the sci-fi/horror film The Astronaut's Wife (1999). The same year he teamed up again with Burton in Sleepy Hollow (1999), brilliantly portraying Ichabod Crane.
    
    Depp has played many characters in his career, including another fact-based one, Insp. Fred Abberline in From Hell (2001). He stole the show from screen greats such as Antonio Banderas in the finale to Robert Rodriguez's "mariachi" trilogy, Once Upon a Time in Mexico (2003). In that same year he starred in the marvelous family blockbuster Pirates of the Caribbean: The Curse of the Black Pearl (2003), playing a character that only the likes of Depp could pull off: the charming, conniving and roguish Capt. Jack Sparrow. The film's enormous success has opened several doors for his career and included an Oscar nomination. He appeared as the central character in the Stephen King-based movie, Secret Window (2004); as the kind-hearted novelist James Barrie in the factually-based Finding Neverland (2004), where he co-starred with Kate Winslet; and Rochester in the British film, The Libertine (2004). Depp collaborated again with Burton in a screen adaptation of Roald Dahl's novel, Charlie and the Chocolate Factory (2005), and later in Alice in Wonderland (2010) and Dark Shadows (2012).
    
    Off-screen, Depp has dated several female celebrities, and has been engaged to Sherilyn Fenn, Jennifer Grey, Winona Ryder and Kate Moss. He was married to Lori Anne Allison in 1983, but divorced her in 1985. Depp has two children with French singer/actress Vanessa Paradis: Lily-Rose Melody, born in 1999 and Jack, born in 2002. He married actress/producer Amber Heard in 2015.
    "
    
    """

    print("parent lexical",parent_lexical(text))
    print("parent syntactic",parent_syntactic(text))

    print("education_lexical",education_lexical(text))
    print("education_syntactic",education_syntactic(text))

    print("spouse lexical",spouse_lexical(text))
    print("spouse syntactic",spouse_syntactic(text))

    print("debut lexical",debut_lexical(text))
    print("debut syntactic",debut_syntactic(text))

    print("starin lexical",starin_lexical(text))
    print("starin syntactic",starin_syntactic(text))
    export_dict = dict()
    export_dict['parent'] = parent_syntactic(text)
    export_dict['education'] = education_syntactic(text)
    export_dict['debuted_in'] = debut_syntactic(text)
    export_dict['starred_in'] = starin_syntactic(text)
    export_dict['spouse'] = spouse_syntactic(text)

    with open(export_file_path,"w+") as f:
        f.write(str(export_dict))
        f.write('\n')

