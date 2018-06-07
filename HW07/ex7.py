import utils
import numpy as np
from math import log10

def single_pmi(term_prob, term_prob_class, use_log=True):
    
    if not use_log:
        if term_prob_class == 0:
            return -float('Inf')
        return log10(term_prob_class / float(term_prob))
    else:
        return term_prob_class - term_prob

def compute_single_category_pmi(pmi_list):
    return max(pmi_list)

def ex4_1():

    # read data
    stop_words = utils.tokenize_text_file("Materials/stopwords.txt")
    train_bio = utils.tokenize_text_file("Materials/train/Biology.txt", stopwords=stop_words)
    train_chem = utils.tokenize_text_file("Materials/train/Chemistry.txt", stopwords=stop_words)
    train_phys = utils.tokenize_text_file("Materials/train/Physics.txt", stopwords=stop_words)

    # preprocess data
    train_bio = utils.lemma_stemming(train_bio) 
    train_chem = utils.lemma_stemming(train_chem)
    train_phys = utils.lemma_stemming(train_phys)

    train_all = train_bio + train_chem + train_phys

    # compute probabilities

    # probabilities of all occurring words in all texts
    p_t = utils.get_probabilities(train_all, train_all, get_log_prob=True)

    # conditional probabilities of all terms depending on class
    p_t_bio = utils.get_probabilities(train_all, train_bio, get_log_prob=True)
    p_t_chem = utils.get_probabilities(train_all, train_chem, get_log_prob=True)
    p_t_phys = utils.get_probabilities(train_all, train_phys, get_log_prob=True)
   

    bio_pmis = []
    chem_pmis = []
    phys_pmis = []

    all_pmis = [bio_pmis, chem_pmis, phys_pmis]

    # compute pmi values

    for term in set(train_all):

        pmi_bio = single_pmi(p_t[term], p_t_bio[term], use_log=True)
        pmi_chem = single_pmi(p_t[term], p_t_chem[term], use_log=True)
        pmi_phys = single_pmi(p_t[term], p_t_phys[term], use_log=True)

        max_index = np.argmax((pmi_bio, pmi_chem, pmi_phys))

        all_pmis[max_index].append((term, max(pmi_bio, pmi_chem, pmi_phys)))

    return all_pmis

if __name__ == "__main__":
    res_lists = ex4_1()
    categories = ["bio", "chem", "phys"]

    for cat_index, pmi_list in enumerate(res_lists):

        print("CATEGORY: {}".format(categories[cat_index]))

        # sort after pmis
        sorted_list = sorted(pmi_list, key=lambda x: x[1], reverse=True)

        for i in range(10):
            term_val = sorted_list[i]
            print("Term: {} - PMI: {}".format(term_val[0], term_val[1])) 
    

