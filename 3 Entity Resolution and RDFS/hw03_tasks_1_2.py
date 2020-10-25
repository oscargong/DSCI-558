from pathlib import Path
from typing import *
from re import sub as re_sub
import sys
import json
import rltk
import student_libs
# You can call your imports via the 'student_libs' module if needed

global g_tokenizer
g_tokenizer = rltk.CrfTokenizer()

class IMDBRecord(rltk.Record):
    ''' Record entry class for each of our IMDB records '''
    def __init__(self, raw_object):
        super().__init__(raw_object)
        self.name = ''

    @rltk.cached_property
    def id(self):
        return self.raw_object['url']

    @rltk.cached_property
    def name_string(self):
        return self.raw_object['name']

    @rltk.cached_property
    def name_tokens(self):
        global g_tokenizer
        return set(g_tokenizer.tokenize(self.name_string))

    # ##########################################################################################
    # ** STUDENT CODE. You may add methods to this record for Task 1.1 inside this ####### block
    @rltk.cached_property
    def year(self):
        return self.raw_object.get('year', None)

    @rltk.cached_property
    def genre(self):
        return self.raw_object.get('genre', None)
    # ##########################################################################################

    @rltk.cached_property
    def title_first_2_letters(self):
        # ######################################################################################
        # ** STUDENT CODE. Task 2.1 (part 1)
        # TODO: Implement title_first_2_letters.
        #       Your code should return the first 2 letters of the record title if it isn't blank,
        #       otherwise return the string '###'. Return type is string.
        #       Your implementation should be inside this ####### block
        name_string = self.raw_object['name']
        if len(name_string)>=2:
            return name_string[0:2]
        else:
            return '##'        
        # ######################################################################################

class AFIRecord(rltk.Record):
    ''' Record entry class for each of our AFI records '''
    def __init__(self, raw_object):
        super().__init__(raw_object)
        self.name = ''

    @rltk.cached_property
    def id(self):
        return self.raw_object['url']

    @rltk.cached_property
    def title_string(self):
        return self.raw_object['title']

    @rltk.cached_property
    def title_tokens(self):
        global g_tokenizer
        return set(g_tokenizer.tokenize(self.title_string))

    # ##########################################################################################
    # ** STUDENT CODE. You may add methods to this record for Task 1.1 inside this ####### block
    @rltk.cached_property
    def release_date(self):
        return self.raw_object.get('release_date', None)

    @rltk.cached_property
    def genre(self):
        return self.raw_object.get('genre', None)
    # ##########################################################################################

    @rltk.cached_property
    def title_first_2_letters(self):
        # ######################################################################################
        # ** STUDENT CODE. Task 2.1 (part 2)
        # TODO: Implement title_first_2_letters.
        #       Your code should return the first 2 letters of the record title if it isn't blank,
        #       otherwise return the string '###'. Return type is string.
        #       Your implementation should be inside this ####### block
        title_string = self.raw_object['title']

        if len(title_string)>=2:
            return title_string[0:2]
        else:
            return '##'
        # ######################################################################################


def create_dataset(input_file: str, rcrd_class: rltk.Record) -> rltk.Dataset:
    ''' Create rltk dataset from a given jl file '''
    assert Path(input_file).suffix == ".jl"
    return rltk.Dataset(reader=rltk.JsonLinesReader(input_file), record_class=rcrd_class, adapter=rltk.MemoryKeyValueAdapter())


def get_ground_truth(input_file: str, ds1: rltk.Dataset, ds2: rltk.Dataset) -> rltk.GroundTruth:
    ''' Read the grouth truth from the given input file '''
    devset_file_handle = open(input_file, "r")
    devset_data = json.load(devset_file_handle)
    gt = rltk.GroundTruth()
    for item in devset_data:
        if None != item['afi_movie']:
            r_imdb = ds1.get_record(item['imdb_movie'])
            r_afi  = ds2.get_record(item['afi_movie']) 
            gt.add_positive(r_imdb.raw_object['url'], r_afi.raw_object['url'])
    return gt

def imdb_afi__title_similarity(r_imdb, r_afi):
    ''' Similiary function for movie title '''
    # ##################################################
    # ** STUDENT CODE. Task 1.1 (part 1)
    # TODO: Implement the similrity function between the two record titles, given the two records
    #       Your code should return a similarty value between 0 to 1 (where 1 means they "certainly" match)
    #       Your implementation should be inside this ####### block
    imdb_name = r_imdb.name_string.strip().lower()
    afi_title = r_afi.title_string.strip().lower()
    similarity = 1 - student_libs.metric_lcs(imdb_name.lower(), afi_title.lower())

    if imdb_name[-1].isnumeric() or afi_title[-1].isnumeric():
        return similarity * 0.8
    elif len(imdb_name)<=4 and len(afi_title) <=4:
        return similarity * 0.8
    else:
        return similarity
    # ##################################################
    
def imdb_afi__release_time_similarity(r_imdb, r_afi):
    ''' Similiary function for movie release time '''
    # ##################################################
    # ** STUDENT CODE. Task 1.1 (part 2)
    # TODO: Implement the similrity function between the two record release times, given the two records
    #       Your code should return a similarty value between 0 to 1 (where 1 means they "certainly" match)
    #       Your implementation should be inside this ####### block

    # afi
    release_date = r_afi.release_date
    if release_date == None:
        afi_year = None
    elif student_libs.re.match(r"\d{1,2}[, ]\w{3,9}[, ]{1,2}\d{4}", release_date):
        #         afi_year = datetime.strptime(release_date,'%d %b, %Y').strftime("%Y")
        afi_year = release_date[-4:]
    elif student_libs.re.match(r"\d\d/\d\d/\d\d\d\d", release_date):
        afi_year = release_date[-4:]
    elif student_libs.re.match(r"\w{3,9}[, ]{1,2}\d{4}", release_date):
        afi_year = release_date[-4:]
    elif student_libs.re.match(r"\d{4}", release_date):
        afi_year = release_date
    else:
        raise AttributeError("AFI entry release_date format unknown")

    # imdb
    imdb_year = r_imdb.year

    if imdb_year == None or afi_year == None:
        return None
    elif int(imdb_year) == int(afi_year):
        return 1
    elif abs(int(imdb_year) - int(afi_year)) <=1:
        return 0.5
    else:
        return 0
    # ##################################################
    
def imdb_afi__genre_similarity(r_imdb, r_afi):
    ''' Similiary function for movie genre '''
    # ##################################################
    # ** STUDENT CODE. Task 1.1 (part 3)
    # TODO: Implement the similrity function between the two record genres, given the two records
    #       Your code should return a similarty value between 0 to 1 (where 1 means they "certainly" match)
    #       Your implementation should be inside this ####### block
    # imdb:afi
    attribute_dict = {
        'Drama': 'Drama',
        'History': None,
        'Horror':'Horror',
        'Sci-Fi':'Science fiction',
        'Film-Noir':'Film noir',
        'Western':'Western',
        'Music':'Musical',
        'Mystery':'Mystery',
        'Crime':'Drama',
        'Adventure': 'Adventure',
        'Family': None,
        'Fantasy':'Fantasy',
        'Romance':'Romance',
        'War':'Drama',
        'Thriller':'Horror',
        'Action':'',
        'Biography':'Biography',
        'Comedy':'Comedy',
        'Musical':'Musical',
        'Sport':None,
        'Animation':None,
        'Documentary':'Documentary'
    }
    afi_genre = r_afi.genre
    imdb_genre = r_imdb.genre

    if afi_genre == None or imdb_genre == None:
        return None
    else:
        afi_list = [item.strip() for item in afi_genre.split(',')]
        imdb_list = [item.strip() for item in imdb_genre.split(',')]

        for imdb in imdb_list:
            if attribute_dict[imdb] == None:
                continue
            for afi in afi_list:
                if attribute_dict[imdb].lower() in afi.lower():
                    return 1
        return 0 # not matcched
    # ##################################################

def rule_based_method(r_imdb, r_afi):
    ''' IMDB-AFI Record Linkage scoring function '''
    # ##################################################
    # ** STUDENT CODE. Task 1.2 (part 1)
    # TODO: Implement the overall similrity measure function between the two given records
    #       Your code should return two values: boolean if they match or not, float to determine confidence (0 to 1)
    #       Your implementation should be inside this ####### block
    score_title = imdb_afi__title_similarity(r_imdb, r_afi)
    score_rtime = imdb_afi__release_time_similarity(r_imdb, r_afi)
    score_genre = imdb_afi__genre_similarity(r_imdb, r_afi)

    flag = "Normal"
    if score_rtime == None or score_genre == None:
        weighted_score = score_title
        flag = 'None  '
    else:
        weighted_score = 0.6 * score_title + 0.2 * score_rtime + 0.2 * score_genre

    match = True if weighted_score >= 0.66 else False

    # if weighted_score >= 0.66:
    #     print(flag, "  ",r_imdb.name_string,'\t=>\t', r_afi.title_string)
    
    return match, weighted_score
    # ##################################################

def main():
    # here's how you can construct the the datasets from the given files (as seen in the notebook)
    ds1_file = "./imdb.jl"
    ds2_file = "./afi.jl"
    ds_imdb = create_dataset(ds1_file, IMDBRecord)
    ds_afi = create_dataset(ds2_file, AFIRecord)
    # here's how you can get the gruond truth if you need it (as seen in the notebook)
    gt_file   = "./imdb_afi_el.dev.json"
    gt = get_ground_truth(gt_file, ds_imdb, ds_afi)
    # ##################################################
    # ** STUDENT CODE. Task 1.2 (part 2) --> this code should run as part of main()
    # TODO: Export your linkage prediction from the IMDB dataset (imdb.jl) to the AFI dataset (afi.jl) into to an output file
    #       The output file should be name `Firstname_Lastname_hw03_imdb_afi_el.json` and should be also submitted
    #       Your implementation should be inside this ####### block
    
    pairs = rltk.get_record_pairs(ds_imdb, ds_afi)


    matched_list = []
    imdb_flag = ds_imdb.head(1)
    for r_imdb in ds_imdb:
        flag = False
        for r_afi in ds_afi:
            match,_ = rule_based_method(r_imdb, r_afi)
            if match:
                flag = True
                export = {
                    "imdb_movie": r_imdb.id,
                    "afi_movie": r_afi.id
                }
                matched_list.append(export)
                continue
        if not flag:
            export = {
                        "imdb_movie": r_imdb.id,
                        "afi_movie": None
                    }
            matched_list.append(export)



    # for r_imdb, r_afi in pairs:
    #     if r_imdb != imdb_flag:
    #         imdb_flag = r_imdb
    #         export = {
    #                 "imdb_movie": r_imdb.id,
    #                 "afi_movie": None
    #             }
    #         matched_list.append(export)
    #     else:
    #         match,_ = rule_based_method(r_imdb, r_afi)
    #         if match:
    #             # print(r_imdb.name_string,'\t|\t',r_afi.title_string)
    #             export = {
    #                 "imdb_movie": r_imdb.id,
    #                 "afi_movie": r_afi.id
    #             }
    #             matched_list.append(export)
    
    with open('Ziheng_Gong_hw03_imdb_afi_el.json','w') as f:
        json.dump(matched_list,f)
    
    
    # ##################################################


def create_hash_blocks(dataset_1: rltk.Dataset, dataset_2: rltk.Dataset) -> rltk.block:
    ''' Create and return rltk hash blocks '''
    # ##################################################
    # ** STUDENT CODE. Task 2.2 (part 1)
    # TODO: Implement create_hash_blocks.
    #       Your code should implement a hash blocking method using rltk.HashBlockGenerator().
    #       The hashing property should be the attribute 'title_first_2_letters'.
    #       Your implementation should be inside this ####### block
    bg = rltk.HashBlockGenerator()
    block = bg.generate(
        bg.block(dataset_1,property_='title_first_2_letters'),
        bg.block(dataset_2,property_='title_first_2_letters')
    )

    return block
    # ##################################################


def create_token_blocks(dataset_1: rltk.Dataset, dataset_2: rltk.Dataset) -> rltk.block:
    ''' Create and return rltk token blocks '''
    # ##################################################
    # ** STUDENT CODE. Task 2.2 (part 2)
    # TODO: Implement create_token_blocks.
    #       Your code should implement a bi-gram token blocking method using rltk.TokenBlockGenerator().
    #       You can use rltk.NGramTokenizer() to generate ngrams (where n=2).
    #       Your implementation should be inside this ####### block
    bg = rltk.TokenBlockGenerator()
    tokenizer = rltk.NGramTokenizer()

    block = bg.generate(
        bg.block(
            dataset_1, 
            property_='name_string',
            function_= lambda x: tokenizer.basic(x.name_string,2)
            ),
        bg.block(
            dataset_2, 
            property_='title_string',
            function_= lambda x:tokenizer.basic(x.title_string,2)
            )
    )
    return block
    # ##################################################


if __name__ == '__main__':
    main()