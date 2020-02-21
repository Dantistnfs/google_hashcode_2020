"""
Written by dantistnfs for google hash code 2020
"""
import os
import itertools
from collections import Counter
from tqdm import tqdm
import numpy as np

def consume_str(arr):
    string = [int(x) for x in arr[0].split(' ')]
    arr.pop(0)
    return string

def consume_library(arr):
    lib_par = [int(x) for x in arr[0].split(' ')]
    arr.pop(0)
    lib_books = [int(x) for x in arr[0].split(' ')]
    arr.pop(0)
    return lib_par, lib_books

def calculate_max_score_lib(lib, books, book_scores, days_for_scan):
    avalible_days = days_for_scan - lib[1]
    lib_speed = lib[2]
    avalible_books_score = [book_scores[x] for x in books]
    arr = np.array([books, avalible_books_score]).T
    arr = arr[arr[:,1].argsort()[::-1]]
    num_to_scan = avalible_days*lib_speed
    if num_to_scan > len(arr):
        num_to_scan = len(arr) - 1
    selected_books = arr[0:num_to_scan]
    return selected_books.sum(axis=0)[1], selected_books[:,0]

def process_lib_file(f):
    # READING FILE
    print("Started processing: {}".format(f))
    f = open("./inputs/{}".format(i_file),'r').read()
    f = f.split("\n")
    while f[-1] == '':
        f.pop()
    s_par = consume_str(f)
    books_num = s_par[0]
    libraries_num = s_par[1]
    days_avalible = s_par[2]
    book_scores = consume_str(f)
    libs = []
    books = []
    enumer = 0
    while len(f) > 0:
        lib_o = consume_library(f)
        lib_o_0 = lib_o[0]
        lib_o_0.append(enumer)
        libs.append(lib_o_0)
        books.append(lib_o[1])
        enumer += 1

    total_books_count = list(itertools.chain.from_iterable(books))
    counted = Counter(total_books_count)
    num_of_unique = 0
    for value in counted.values():
        if value == 1:
            num_of_unique += 1
    
    print("Percent Unique: {}".format(num_of_unique/books_num*100))


    output_file = []
    # CALCULATING CYCLE
    
    prev_max = 1000000000000
    while (days_avalible > 0) and libs:
        print("Days for scan: {}".format(days_avalible))
        max_scores = []
        selected_books = []

        # COMPUTE BEST BOOKS FOR EACH LIBRARY
        for i in range(0,len(libs)):
            s = calculate_max_score_lib(libs[i], books[i], book_scores, days_avalible)
            max_scores.append(s[0]/(libs[i][1]**2))
            selected_books.append(s[1])
            if max_scores[-1] >= prev_max:
                break

        max_score = max(max_scores)
        prev_max = max_score
        best_lib = max_scores.index(max_score)
        best_books = books[best_lib]
        print("Best lib found: {}, it's score {}".format(best_lib, max_score))

        # ASSUME IT's BEST WAS REALLY THE BEST
        # update days_avalible
        days_avalible -= libs[best_lib][1]
        best_lib_id = libs[best_lib][3]
        libs.pop(best_lib)
        books.pop(best_lib)

        # EXCLUDE BOOKS SCANNED BY BEST LIB FROM GLOBAL NEEDED BOOK LIST
        for i in range(0,len(best_books)):
            book_scores[best_books[i]] = 0
            
        output_file.append("{} {}".format(best_lib_id, len(best_books)))
        output_file.append(" ".join([str(x) for x in best_books]))

    output_file.insert(0,str(len(output_file)//2))
    output_file = '\n'.join(output_file)
    text_file = open("./outputs/{}".format(i_file), "w")
    text_file.write(output_file)
    text_file.close()
    return 0


input_files = os.listdir("./inputs")
input_files.sort()

for i_file in input_files:
    process_lib_file(i_file)
