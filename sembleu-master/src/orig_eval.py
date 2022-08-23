#!/usr/bin/env python3

import os, sys, json, time
from bleu_score import corpus_bleu, sentence_bleu, SmoothingFunction, NgramInst
from amr_graph import AMRGraph

from nmt_english import Translator

def read_amr(path):
    ids = []
    id_dict = {}
    amrs = []
    amr_str = ''
    for line in open(path,'r'):
        if line.startswith('#'):
            if line.startswith('# ::id'):
                id = line.strip().split()[2]
                ids.append(id)
                id_dict[id] = len(ids)-1
            continue
        line = line.strip()
        if line == '':
            if amr_str != '':
                amrs.append(amr_str.strip())
                amr_str = ''
        else:
            amr_str = amr_str + line + ' '

    if amr_str != '':
        amrs.append(amr_str.strip())
        amr_str = ''
    return amrs

def get_amr_ngrams(path, stat_save_path=None):
    data = []
    if stat_save_path:
        f = open(stat_save_path, 'w')
    for line in read_amr(path):
        try:
            amr = AMRGraph(line.strip())
        except AssertionError:
            print(line)
            assert False
        amr.revert_of_edges()
        ngrams = amr.extract_ngrams(3, multi_roots=True) # dict(list(tuple))
        data.append(NgramInst(ngram=ngrams, length=len(amr.edges)))
        if stat_save_path:
            print(len(amr), len(ngrams[1]), len(ngrams[2]), len(ngrams[3]), file=f)
    if stat_save_path:
        f.close()
    return data

def remove_parens(text):
	return text.replace("(","").replace(")","")

# def open_paren_handler(token, file_save_path,translator):
# 	file_save_path.write(' ')
# 	curr_token = token
# 	if curr_token.startswith('('):
# 		print("in while loop")
# 		file_save_path.write('(')
# 		item = curr_token[1:]
# 		with open('line.txt', 'w') as f:
# 			f.write(item)
# 			f.close()
# 			translator.load_sentences('line.txt')
# 			out = translator.translate(source_language="es")
# 			out_text = str(out[0])
# 			if '(' in out_text or '(' in out_text:
# 				out_text = remove_parens(out_text)
# 			if ' ' in out_text:
# 				if out_text.split()[0] == 'to':
# 					out_new = out_text.split()[1]
# 					file_save_path.write(out_new)
# 					file_save_path.write(' ')
# 					continue
# 				else:
# 					out_new = out_text.replace(' ', '-')
# 					file_save_path.write(out_new)
# 					file_save_path.write(' ')
# 					continue
# 			else:
# 				file_save_path.write(out_text)
# 				file_save_path.write(' ')
# 				continue
# 		curr_token = curr_token[1:]
# 	#print("out of while loop")

# def close_paren_handler(token, file_save_path,translator):
# 	curr_token = token
# 	while curr_token.endswith(')'):
# 		print("in while loop")
# 		item = curr_token[:-1]
# 		with open('line.txt', 'w') as f:
# 			f.write(item)
# 			f.close()
# 			translator.load_sentences('line.txt')
# 			out = translator.translate(source_language="es")
# 			out_text = str(out[0])
# 			if '(' in out_text or '(' in out_text:
# 				out_text = remove_parens(out_text)
# 			if ' ' in out_text:
# 				if out_text.split()[0] == 'to':
# 					out_new = out_text.split()[1]
# 					file_save_path.write(out_new)
# 					#file_save_path.write(') ')
# 					continue
# 				else:
# 					out_new = out_text.replace(' ', '-')
# 					file_save_path.write(out_new)
# 					#file_save_path.write(') ')
# 					continue
# 			else:
# 				file_save_path.write(out_text)
# 		file_save_path.write(')')
# 		curr_token = curr_token[:-1]
# 	file_save_path.write(' ')
# 	print("out of while loop")

def truncate(text, end_index=5):
	if len(text) >= end_index:
		if text.startswith('"') and text.endswith('"'):
			new_text = text[0:end_index] + '"'
			return new_text
		else:
			return text[0:end_index]
	else:
		return text


def translate_and_truncate_amr(path):
	translator = Translator()
	#data = []
	with open('translated_amr.txt', 'w') as file_save_path:
		for line in read_amr(path):
			#print(line)
			for item in line.split():
				#print("ITEM")
				#print(item)
				if item == "-":
					file_save_path.write(item)
					file_save_path.write(' ')
					continue
				if item == "/":
					file_save_path.write(item)
					file_save_path.write(' ')
					continue
				if item.startswith(':'):
					file_save_path.write(item)
					file_save_path.write(' ')
					continue
				# if item.startswith('"'):
				# 	file_save_path.write(item)
				# 	file_save_path.write(' ')
				# 	continue
				elif item.startswith('(') or item.endswith(')'):
					#print("begin if statement")
					# -- write number of open parens
					num_open_parens = item.count('(')
					num_close_parens = item.count(')')
					for x in range(num_open_parens):
						file_save_path.write('(')
					# if num_open_parens > 0:
					# 	file_save_path.write(' ')
					# -- write item
					item = remove_parens(item)
					if item == "-" or item == "/" or item.startswith(':'):
						file_save_path.write(item)
					else:
						# HERE
						with open('line.txt', 'w') as f:
							f.write(item)
						f.close()
						translator.load_sentences('line.txt')
						out = translator.translate(source_language="es")
						out_text = str(out[0])
						if '(' in out_text or '(' in out_text:
							out_text = remove_parens(out_text)
							#print("end remove parens")
							if ' ' in out_text:
								if out_text.split()[0] == 'to':
									out_new = out_text.split()[1]
									# TRUNCATING HERE
									out_new = truncate(out_new)
									file_save_path.write(out_new)
									file_save_path.write(' ')
								else:
									out_new = out_text.replace(' ', '-')
									# TRUNCATING HERE
									out_new = truncate(out_new)
									file_save_path.write(out_new)
									file_save_path.write(' ')
						else:
							# TRUNCATING HERE
							out_text = truncate(out_text)
							file_save_path.write(out_text)
							file_save_path.write(' ')
					#file_save_path.write(' ')
					# -- write number of close parens
					for y in range(num_close_parens):
						file_save_path.write(')')
					if num_close_parens > 0:
						file_save_path.write(' ')
					#print("end if statement")
				else:
					#print(item)
					with open('line.txt', 'w') as f:
						f.write(item)
					f.close()
					translator.load_sentences('line.txt')
					out = translator.translate(source_language="es")
					out_text = str(out[0])
					if '(' in out_text or '(' in out_text:
						out_text = remove_parens(out_text)
						#print("end remove parens")
					if ' ' in out_text:
						if out_text.split()[0] == 'to':
							out_new = out_text.split()[1]
							# TRUNCATING HERE
							out_new = truncate(out_new)
							file_save_path.write(out_new)
							file_save_path.write(' ')
							continue
						else:
							out_new = out_text.replace(' ', '-')
							# TRUNCATING HERE
							out_new = truncate(out_new)
							file_save_path.write(out_new)
							file_save_path.write(' ')
							continue
					else:
						# TRUNCATING HERE
						out_text = truncate(out_text)
						file_save_path.write(out_text)
						file_save_path.write(' ')
					#print(str(out[0]))

def truncate_amr(path):
	#translator = Translator()
	#data = []
	with open('truncated_amr.txt', 'w') as file_save_path:
		for line in read_amr(path):
			#print(line)
			for item in line.split():
				#print("ITEM")
				#print(item)
				if item == "-":
					file_save_path.write(item)
					file_save_path.write(' ')
					continue
				if item == "/":
					file_save_path.write(item)
					file_save_path.write(' ')
					continue
				if item.startswith(':'):
					file_save_path.write(item)
					file_save_path.write(' ')
					continue
				# if item.startswith('"'):
				# 	file_save_path.write(item)
				# 	file_save_path.write(' ')
				# 	continue
				elif item.startswith('(') or item.endswith(')'):
					#print("begin if statement")
					# -- write number of open parens
					num_open_parens = item.count('(')
					num_close_parens = item.count(')')
					for x in range(num_open_parens):
						file_save_path.write('(')
					# if num_open_parens > 0:
					# 	file_save_path.write(' ')
					# -- write item
					item = remove_parens(item)
					if item == "-" or item == "/" or item.startswith(':'):
						file_save_path.write(item)
					else:
						# HERE
						# with open('line.txt', 'w') as f:
						# 	f.write(item)
						# f.close()
						# translator.load_sentences('line.txt')
						# out = translator.translate(source_language="es")
						# out_text = str(out[0])
						out_text = item
						if '(' in out_text or '(' in out_text:
							out_text = remove_parens(out_text)
							# print("end remove parens")
							if ' ' in out_text:
								if out_text.split()[0] == 'to':
									out_new = out_text.split()[1]
									# TRUNCATING HERE
									out_new = truncate(out_new)
									file_save_path.write(out_new)
									file_save_path.write(' ')
								else:
									out_new = out_text.replace(' ', '-')
									# TRUNCATING HERE
									out_new = truncate(out_new)
									file_save_path.write(out_new)
									file_save_path.write(' ')
						else:
							out_text = remove_parens(out_text)
							# TRUNCATING HERE
							out_text = truncate(out_text)
							file_save_path.write(out_text)
							file_save_path.write(' ')
					#file_save_path.write(' ')
					# -- write number of close parens
					for y in range(num_close_parens):
						file_save_path.write(')')
					if num_close_parens > 0:
						file_save_path.write(' ')
					#print("end if statement")
				else:
					#print(item)
					# with open('line.txt', 'w') as f:
					# 	f.write(item)
					# f.close()
					# translator.load_sentences('line.txt')
					# out = translator.translate(source_language="es")
					# out_text = str(out[0])
					out_text = item
					if '(' in out_text or '(' in out_text:
						out_text = remove_parens(out_text)
						# print("end remove parens")
					if ' ' in out_text:
						if out_text.split()[0] == 'to':
							out_new = out_text.split()[1]
							# TRUNCATING HERE
							out_new = truncate(out_new)
							file_save_path.write(out_new)
							file_save_path.write(' ')
							continue
						else:
							out_new = out_text.replace(' ', '-')
							# TRUNCATING HERE
							out_new = truncate(out_new)
							file_save_path.write(out_new)
							file_save_path.write(' ')
							continue
					else:
						# TRUNCATING HERE
						out_text = truncate(out_text)
						file_save_path.write(out_text)
						file_save_path.write(' ')
					#print(str(out[0]))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('python this-script ans-file ref-file')
        sys.exit(0)
    print('loading ...')
    #translated_hypo = translate_and_truncate_amr(sys.argv[1])
    #print(translated_hypo)
    #hypothesis = get_amr_ngrams("translated_amr.txt")
    hypothesis = get_amr_ngrams(sys.argv[1])
    print("HYPOTHESIS")
    print(hypothesis)
    #truncated_ref = truncate_amr(sys.argv[2])
    references = [[x] for x in get_amr_ngrams(sys.argv[2])]
    #references = [[x] for x in get_amr_ngrams("truncated_amr.txt")]
    print("REFERENCES")
    print(references)
    smoofunc = getattr(SmoothingFunction(), 'method3')
    print('evaluating ...')
    st = time.time()
    if len(sys.argv) == 4:
        n = int(sys.argv[3])
        weights = (1.0/n, )*n
    else:
        weights = (0.34, 0.33, 0.34)
    print(corpus_bleu(references, hypothesis, weights=weights, smoothing_function=smoofunc, auto_reweigh=True))
    print('time:', time.time()-st, 'secs')
