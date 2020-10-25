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


    # ##########################################################################################

    @rltk.cached_property
    def title_first_2_letters(self):
        # ######################################################################################
        # ** STUDENT CODE. Task 2.1 (part 1)
        # TODO: Implement title_first_2_letters.
        #       Your code should return the first 2 letters of the record title if it isn't blank,
        #       otherwise return the string '###'. Return type is string.
        #       Your implementation should be inside this ####### block
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


    # ##########################################################################################

    @rltk.cached_property
    def title_first_2_letters(self):
        # ######################################################################################
        # ** STUDENT CODE. Task 2.1 (part 2)
        # TODO: Implement title_first_2_letters.
        #       Your code should return the first 2 letters of the record title if it isn't blank,
        #       otherwise return the string '###'. Return type is string.
        #       Your implementation should be inside this ####### block
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
    return 0
    # ##################################################
    
def imdb_afi__release_time_similarity(r_imdb, r_afi):
    ''' Similiary function for movie release time '''
    # ##################################################
    # ** STUDENT CODE. Task 1.1 (part 2)
    # TODO: Implement the similrity function between the two record release times, given the two records
    #       Your code should return a similarty value between 0 to 1 (where 1 means they "certainly" match)
    #       Your implementation should be inside this ####### block
    return 0
    # ##################################################
    
def imdb_afi__genre_similarity(r_imdb, r_afi):
    ''' Similiary function for movie genre '''
    # ##################################################
    # ** STUDENT CODE. Task 1.1 (part 3)
    # TODO: Implement the similrity function between the two record genres, given the two records
    #       Your code should return a similarty value between 0 to 1 (where 1 means they "certainly" match)
    #       Your implementation should be inside this ####### block
    return 0
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
    return True, 0
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
    # ##################################################


def create_hash_blocks(dataset_1: rltk.Dataset, dataset_2: rltk.Dataset) -> rltk.block:
    ''' Create and return rltk hash blocks '''
    # ##################################################
    # ** STUDENT CODE. Task 2.2 (part 1)
    # TODO: Implement create_hash_blocks.
    #       Your code should implement a hash blocking method using rltk.HashBlockGenerator().
    #       The hashing property should be the attribute 'title_first_2_letters'.
    #       Your implementation should be inside this ####### block
    return None
    # ##################################################


def create_token_blocks(dataset_1: rltk.Dataset, dataset_2: rltk.Dataset) -> rltk.block:
    ''' Create and return rltk token blocks '''
    # ##################################################
    # ** STUDENT CODE. Task 2.2 (part 2)
    # TODO: Implement create_token_blocks.
    #       Your code should implement a bi-gram token blocking method using rltk.TokenBlockGenerator().
    #       You can use rltk.NGramTokenizer() to generate ngrams (where n=2).
    #       Your implementation should be inside this ####### block
    return None
    # ##################################################


if __name__ == '__main__':
    main()