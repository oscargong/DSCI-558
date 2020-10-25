from typing import *
import sys
import rltk

from hw03_tasks_1_2 import IMDBRecord, AFIRecord, \
                            create_dataset, get_ground_truth, create_hash_blocks, create_token_blocks

HASH_BLOCKING = 0
TOKN_BLOCKING = 1


def calc_reduction_ratio(dataset_1, dataset_2, block_set, gt_set):
    ''' Calculate and print reduction ratio '''

    pairs = rltk.get_record_pairs(dataset_1, dataset_2, block=block_set)
    
    set_candidates_size = len(list(pairs))
    ds1_size = len(dataset_1.generate_dataframe())
    ds2_size = len(dataset_2.generate_dataframe())

    rr = (1 - float((set_candidates_size)/(ds1_size*ds2_size)))
    print(f'Reduction Ratio    = 1 - ({set_candidates_size}/{ds1_size}*{ds2_size}) = {rr:.06f}')
    return rr


def calc_pairs_completeness(dataset_1, dataset_2, block_set, gt_set):
    ''' Calculate and print Pairs Completeness '''

    gt_dict = dict()
    cand_matches = 0

    for id_r1, id_r2, label in gt_set:
        if label:
            gt_dict[id_r1] = id_r2
    gt_matches = len(gt_dict)

    for key, r1_id, r2_id in block_set.pairwise(dataset_1, dataset_2):
        if r1_id in gt_dict and gt_dict[r1_id] == r2_id:
            cand_matches += 1
            del gt_dict[r1_id]

    pc = float(cand_matches)/gt_matches
    print(f'Pairs Completeness = {cand_matches}/{gt_matches} = {pc:.06f}')
    return pc


def evaluate_blocking(ds1_file: str, ds2_file: str, gt_file: str, blk_type: int):
    ''' Evaluate and print the reduction-ratio and pairs-completeness
        of the data, based on the given ground truth file '''

    dataset_1: rltk.Dataset = create_dataset(ds1_file, IMDBRecord)
    dataset_2: rltk.Dataset = create_dataset(ds2_file, AFIRecord)

    gt_set = get_ground_truth(gt_file, dataset_1, dataset_2)

    if HASH_BLOCKING == blk_type:
        blocks = create_hash_blocks(dataset_1, dataset_2)
    else:
        blocks = create_token_blocks(dataset_1, dataset_2)

    calc_reduction_ratio(dataset_1, dataset_2, blocks, gt_set)
    calc_pairs_completeness(dataset_1, dataset_2, blocks, gt_set)


def main():

    if len(sys.argv) < 2:
        print("Error: missing blocking type!")
        exit(1)

    if sys.argv[1] == 'hash':
        blocking_type = HASH_BLOCKING
    elif sys.argv[1] == 'token':
        blocking_type = TOKN_BLOCKING
    else:
        print("Error: blocking type should be 'hash' or 'token'!")
        exit(1)

    # define filenames
    ds1_file = "./imdb.jl"
    ds2_file = "./afi.jl"
    gt_file   = "./imdb_afi_el.dev.json"

    # evaluate
    evaluate_blocking(ds1_file, ds2_file, gt_file, blocking_type)


if __name__ == '__main__':
    main()