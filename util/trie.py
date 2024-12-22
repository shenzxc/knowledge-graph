# -*- coding: UTF-8 -*-

import pickle
import os
import json
from tqdm import tqdm
import sys
sys.path.append('..')
from loguru import logger as log
from util import get_terms_from_json, pmc_data_iterator
sys.setrecursionlimit(30000)

punctuation = {'_', '~', '(', '^', '+', '"', '#', '%', ':', '?', '`', '>', '$', '@', '*', '[', ']', '!', '&', ',',
               '{', ';', '.', '|', '}', "'", '<', '\\', '=', ')', '/'}


class TrieNode:
    def __init__(self):
        self.table = dict()
        self.phrase_end = False
        self.phrase = None

    def __len__(self):
        return len(self.table)


class TrieMatchResult:
    def __init__(self, begin, end, phrase):
        self.begin = begin
        self.end = end
        self.phrase = phrase

    def __str__(self):
        return json.dumps({
            "begin": self.begin,
            "end": self.end,
            "phrase": self.phrase,
        })

    def __repr__(self):
        return json.dumps({
            "begin": self.begin,
            "end": self.end,
            "phrase": self.phrase,
        })


class Trie:
    def __init__(self, terms_pkl_file_path, trie_pkl_file_path):
        self.root = TrieNode()
        self.terms_pkl_file_path = terms_pkl_file_path
        self.trie_pkl_file_path = trie_pkl_file_path

    def insert_phrase(self, phrase):
        node = self.root

        for ch in phrase:
            if ch not in node.table:
                node.table[ch] = TrieNode()
            node = node.table[ch]

        node.phrase_end = True
        node.phrase = phrase

    # if text[start:] has a prefix in this trie
    # return the end position of this match
    # else return -1
    def search(self, text, start=0):
        node = self.root

        tmp_result = (-1, None)
        for i in range(start, len(text)):
            if text[i] not in node.table:
                break
            node = node.table[text[i]]
            if node.phrase_end:
                if i == len(text) - 1 or text[i + 1].isspace() or text[i + 1] in punctuation:
                    tmp_result = i + 1, node.phrase
        return tmp_result

    """建Trie树"""

    def build(self):
        f = open(self.terms_pkl_file_path, "rb")
        all_terms = pickle.load(f)
        f.close()
        for term in tqdm(all_terms):
            self.insert_phrase(term)
        self.save()

    def save(self):
        log.info("saving")
        f = open(self.trie_pkl_file_path, "wb")
        pickle.dump(self.root, f)
        f.close()

    def load(self):
        log.info("loading")
        f = open(self.trie_pkl_file_path, "rb")
        self.root = pickle.load(f)
        f.close()

    """匹配文本"""

    def match(self, text):
        result_list = []
        i = 0
        while i < len(text):
            #if (i == 0 or text[i - 1].isspace()) and text[i].isalnum():
            if (i == 0 or text[i - 1].isspace() or text[i-1]=='(') and text[i].isalnum():
                res = self.search(text, i)
                if res[0] > 0:
                    result_item = vars(TrieMatchResult(i, res[0], res[1]))
                    result_list.append(result_item)
                    i = res[0]
                else:
                    i += 1
            else:
                i += 1
        return result_list


def gen_terms_pkl(terms_pkl_path, cleanterms_path):
    all_terms = get_terms_from_json(cleanterms_path)
    
    with open(terms_pkl_path, 'wb') as writer:
        pickle.dump(all_terms, writer)
        log.info("生成术语字典成功")


def build_trie_tree(terms_pkl_path, trie_pkl_path):
    trie = Trie(terms_pkl_path, trie_pkl_path)
    trie.build()
    log.info("构件字典树完成")
    return trie


def match_and_tagging(trie, text_path, output_path):
    cnt = 0
    with open(output_path, 'w', encoding="utf-8") as writer:
        for text in pmc_data_iterator(text_path):
            text = text.lower() # 统一为小写匹配
            matches = trie.match(text) 
            if len(matches) == 0:
                continue
            
            cnt += 1
            writer.write(json.dumps(dict(text=text, entities=matches), ensure_ascii=False) + "\n")
            if cnt % 10000 == 0:
                log.info("进度：%d" % cnt)


if __name__ == "__main__":

    terms_path = "../result/clean/cleaned_gpt_terms.json"
    text_path = "../data/pmc_data/random_pmc_oa_2000w.txt"
    output_path = "../data/matched_entities_result.json"
    terms_pkl_path = "./terms.pkl"
    trie_pkl_path = "./trie.pkl"
    

    log.info("try to gen terms pkl ...")
    gen_terms_pkl(terms_pkl_path, terms_path)

    log.info("try to build trie tree ...")
    trie = build_trie_tree(terms_pkl_path, trie_pkl_path)

    log.info("match text ...")
    match_and_tagging(trie, text_path, output_path)
