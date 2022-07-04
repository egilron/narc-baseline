# -*- coding: utf-8 -*-

# Lilja Øvrelid

import re
import sys

from sys import argv
from collections import defaultdict

file = argv[1]


# Functions for accessing the conll data fields
# Input: a list of fields for a token
#****************************************************************************#
def get_id(fields):
    """
    return the token id
    """
    return int(fields[0])


def get_form(fields):
    """
    return the word form
    """
    return fields[1]

def get_lemma(fields):
    """
    return the lemma
    """
    return fields[2]

def get_cpos(fields):
    """
    return the cpos
    """
    return fields[3]

# return the fine grained part of speech
def get_pos(fields):
    """
    return the pos
    """
    return fields[4]

def get_feats(fields):
    """
    return the feats
    """
    return fields[5]

def get_head(fields):
    """
    return the head
    """
    return int(fields[6])

# return the dependency relation
def get_deprel(fields):
    return fields[7]

# return a line of token data in a sentence, given a token id
def get_data(id, sentence):
    return sentence[id-1]

#NP = Nominal heads + all dependents of a nominal head forms a NP
#Nominal = 
# * subst, 
# * pron (pers, not expletive: deprel FSUBJ, FOBJ), 
# * det poss
# * adj (nominal deprel: SUBJ/OBJ/PUTFYLL)


def get_NP(s,graph,token):
    token_id = get_id(token)
    visited = None
    deps = dfs(graph, token_id, s, visited)
    filtered = filter_deps(s,sorted(deps))

    #uncomment this to output NP forms
    # forms = []
    # for dep in filtered:
    #    deprel = get_deprel(s[dep-1])
    #    form = get_form(s[dep-1])
    #    forms.append(form)
    # return forms

    return filtered


def get_NP_nokoord(s,graph,token):
    token_id = get_id(token)
    visited = None
    deps = dfs_nokoord(graph, token_id, s, visited)
    filtered = filter_deps(s,sorted(deps))
    #uncomment this to output NP forms
    # forms = []
    # for dep in filtered:
    #     deprel = get_deprel(s[dep-1])
    #     form = get_form(s[dep-1])
    #     forms.append(form)
    
    # return forms

    return filtered





def filter_deps(s,deps):
    first = deps[0]
    firstdep = get_deprel(s[first-1])
    if firstdep == "KONJ":
        deps.pop(0)
    elif firstdep == "FLAT" and len(deps) == 1:
        deps.pop(0)
    elif firstdep == "APP" and len(deps) == 1:
        deps.pop(0)
    return deps


def is_nominal(token,s):
    pos = get_pos(token)
    feats = get_feats(token)
    dep = get_deprel(token)

    r = re.compile('.*pers.*')
    pers = r.match(feats)
    r2 = re.compile('.*poss')
    poss = r2.match(feats)
    
    if pos == "subst":
        return True
    elif pos == "pron":
       if pers:
            if dep == "FSUBJ" or dep == "FOBJ":
                return False
            else:
                return True
    elif pos == "det" and poss:
        return True
    elif pos == "adj" and is_nominal_dep(dep):
        return True
    elif pos == "adj" and dep == "KOORD":
        head = get_head(token)
        headdep = get_deprel(s[head-1])
        if is_nominal_dep(headdep):
            return True
    else:
        return False


def is_nominal_dep(dep):
    if dep == "SUBJ" or dep == "OBJ" or dep == "PUTFYLL":
        return True
    else:
        return False



def has_dep_label(deprel,deps):
    labels = []
    if deps:
        labels = map(get_deprel,deps)
        if deprel in labels:
            return True
        else:
            return False
    else:
        return False


def dependents(sentence, head):
    current_id = 1
    dependents = []

    while current_id <= len(sentence):
        if head != current_id:
            current_fields = sentence[current_id-1]
            current_head_id = get_head(current_fields)

            if head == current_head_id:
                dependents.append(current_fields)

        current_id = current_id+1

    return dependents




def make_digraph(sent):
    Gr = {}

    # for each word in the sentence
    for token_data in sent:
        word = get_form(token_data)
        word_id = get_id(token_data)

        # add the id for the word, if not already present.
        if word_id not in Gr:
            Gr[word_id] = set()

        # find the head-info for the current token
        head = get_head(token_data)
        head_data = get_data(head, sent)
        head_id = get_id(head_data)

        if head_id not in Gr:
            Gr[head_id] = set()

        # add the path from the head to the dependent
        Gr[head_id].add(word_id)

    return Gr


def dfs(graph, start, sentence, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for next in graph[start] - visited:
        nextdata = sentence[next - 1]
        nextrel = get_deprel(nextdata)

        dfs(graph, next, sentence, visited)
# koordinering følges ikke, vi vil ikke ha en markable for hele koordineringen
#        if nextrel == "KOORD":
#            return visited
#        else:
#  dfs(graph, next, sentence, visited)

#    print(visited)
    return visited

def dfs_nokoord(graph, start, sentence, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for next in graph[start] - visited:
        nextdata = sentence[next - 1]
        nextrel = get_deprel(nextdata)

        if nextrel == "KOORD":
#            return visited
            next
        else:
            dfs(graph, next, sentence, visited)


    return visited




#######################
# Main processing loop
# Read a conll file

def process(file):
    global tokencounts, sentencecounts, poscounts, depcounts, wordcounts, verbcounts
    # List of lists. Each element is a list of data for a token in the sentence
    sentence = []

    file_data = open(file, 'r')
        # read a line with token info from the file
        # split this string into its 10 elements as a list
    for line in file_data:
        if not line.startswith("#"):

            if line != '\n':
            # Extract token data, add the token data to the sentence.
                fields = line.split('\t')
                sentence.append(fields)

            # Blank line reached, finished reading a sentence.
            else:
                graph = make_digraph(sentence)
                for token in sentence:
                    if is_nominal(token,sentence):
                        tokenid = get_id(token)
                        deps = dependents(sentence, tokenid)
                        np = get_NP(sentence,graph,token)
                        print(np)
                        if has_dep_label("KOORD",deps):
                            np = get_NP_nokoord(sentence,graph,token)
                            print(np)
                        
                        
                sentence = []

    file_data.close()
    



def format_word(t):
    fields = []
    fields.append(str(get_id(t)))
    fields.append(get_form(t))
    fields.append(get_lemma(t))
    fields.append(get_cpos(t))
    fields.append(get_pos(t))
    fields.append(get_feats(t))
    fields.append(str(get_head(t)))
    fields.append(get_deprel(t))
    fields.append("_")
    fields.append("_")
#    print fields
    return fields
    
    
    

def print_conll(s):
    for token_data in s:
        print("\t".join(format_word(token_data)))
    print


def get_relfreq(freq,total):
    rel = freq / total
    return(rel)

f = open(file)

process(file)


# text = f.read()
f.close()


