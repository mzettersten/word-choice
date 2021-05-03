import random

#Pilot Version

######################
# language variables #
######################
#IOT test this script, set solo_run to true.
solo_run = False

input_word_list= ['pim','dak','vorg','yeen','grah','skod','gled',
					'veek','blit','peka','sarp','minada','hoon',
					'clate','noobda','gorm','frabda','mog']

subSize = 8 
# set the size of the language lexicon (from above)

learning_block_count = 4
# for experiment 2.4, we are fixing the number of times a participant does the pairwise learning blocks. This is applied to the pairLearning, and to the new, non-verbal learning which precedes it.

proportion_hf_vocab = 0.5 
#how much of the vocab is designated to hf. note that setting this to anything other than .5 changes the number of training trials.

hf_to_lf_ratio = 4 

#################
# exp variables #
#################

angle_offset = 15 # how far off an ordinary clock
test_length = 20

######
# write vars

#filename="cbal_pilot"
#cbal_Header=['block', 'trial','target','angle','left','right','freq'] #later, cols are appended by words included


#############
# functions #
#############

def list_subsetter(input_word_list,subSize):
	random.shuffle(input_word_list)
	output_list=input_word_list[0:subSize]
	
	return output_list

def convert_ratio(vocabulary_list,proportion_hf_vocab):
	#strictly ordered split of the list
	hf_size=int(len(vocabulary_list)*proportion_hf_vocab) 
	hf_list=vocabulary_list[0:hf_size]
	lf_list=vocabulary_list[hf_size:]
	
	return [hf_list,lf_list]

	
def frequency_maker(list_pair,hf_to_lf_ratio,order=1):

	# Allows the frequency distribution to be counterbalanced by item
	part_one, part_two = (0, 1) if order == 1 else (1, 0)

	local_list=[]
	local_list.extend(list_pair[part_one]*hf_to_lf_ratio)
	local_list.extend(list_pair[part_two])
	
	return local_list

def randoCleaner(list,distance=1):
	# This has not been tested. If works, probably only if/when distance == 1
	# Takes a list and makes sure that neighboring items of x distance are not identical, moves to the end if they are.
	# Repeats until not true for the list.
	cleaned = False

	while not cleaned:
		clean_test = 0
		for i,j in enumerate(list):
			for d in range(distance):
				if list[i]==list[i+d]:
					list.append(pop.list(i))
				else:
					clean_test += 1
		if clean_test==len(list):
			cleaned = True

					
def pairTest(dict_word_directions,word_frequency_list,learn_type = "verbal",genFromScratch=False):
	# genFromScratch was meant to autopopulate the pairtests, but this got complicated, so we hardcoded the pairTests externally (see runtime), and this var is set to False
	# we have two learning trials possible. Default is 'verbal' which generates pairwise words.
	# nonverbal generates pairwise angles.
	if learn_type == "verbal":
		learn_trial = "pairLearn"
	else:
		learn_trial = "nonvLearn"
	if not genFromScratch:
		random.shuffle(word_frequency_list)
		learning_trials=[]
		ct=0
		for each in word_frequency_list:
			ct+=1
			correct_word=each[0]
			foil=each[1]
			if random.randint(1,2)==1:
				left_word,right_word=(correct_word,foil)
			else:
				right_word,left_word=(correct_word,foil)	
			direction=dict_word_directions[correct_word]
			
			if learn_type =="nonverbal":
				left_word = dict_word_directions[correct_word]
				right_word = dict_word_directions[foil]
			learning_trials.append(("learn",learn_trial,ct, correct_word,direction,left_word,right_word))
			
	else:
		# We stopped development/testing on this one.(e.g. nonv trials aren't developed here.)
		foil_dict = {}
		word_set=set(word_frequency_list)

		for word in word_set:
			foil_dict[word]=[]
			for item in word_frequency_list:
				if not item==word:
					foil_dict[word].append(item)
			random.shuffle(foil_dict[word])
		
		learning_trials=[]
		ct=0
		for word in word_frequency_list:
			ct+=1
			foil=foil_dict[word].pop()
			if random.randint(1,2)==1:
				left_word,right_word=(word,foil)
			else:
				right_word,left_word=(word,foil)
			correct_word=word
			direction=dict_word_directions[word]
			
			learning_trials.append(("learn",learn_trial,ct, correct_word,direction,left_word,right_word))
	
	return learning_trials
	
def areaSpecificDegreeGen(pos_degree_increments,separated_lists,
							dict_word_directions,multiple=1,
							offset=0,ratio=1,full_rando=False): #size of distribution, target or offset regions, use/not use lf/hf ratio.
	fullset_randValues=[]

	def rangeDivisor(): #sets ranges into offset half-ranges or not.
		if full_rando:
			range_divisor=2
		else:
			range_divisor=4
		half_range=pos_degree_increments/range_divisor
		return half_range
		
	half_range=rangeDivisor()
	offsetter= (offset*pos_degree_increments/2)

	def regionsMaker(shortlist,ratio_1=1):
		randValues=[]
		for repitition in range(multiple):
			for n in range(ratio_1):
				for i in shortlist:
					centerValue=dict_word_directions[i]-offsetter
					if centerValue<0:
						centerValue=centerValue+360
					lowerBound=centerValue-half_range #math to calculate lower bound of targets
					upperBound=centerValue+half_range #math to calculate upper bound of targets
					randGenValue = random.randint(lowerBound,upperBound)
					randValues.append(randGenValue)
		return randValues

	fullset_randValues.extend(regionsMaker(separated_lists[0],ratio))
	fullset_randValues.extend(regionsMaker(separated_lists[1]))
	random.shuffle(fullset_randValues)
	return fullset_randValues

def evalScore(test_direction,word,dict_word_directions,pos_degree_increments):
	score=min(abs(test_direction - dict_word_directions[word]),abs(dict_word_directions[word] - test_direction))
	if score>180:
		score=360-score
	if score > pos_degree_increments:
		return 0
	else:
		return pos_degree_increments - score
	# return dict_word_directions[word]

def testBlockScores(directions_evaluated,block_label,trialType_label,dict_word_directions,sorted_dict_list,pos_degree_increments,info,wrows):
	score_dict={}
	for i,test_direction in enumerate(directions_evaluated):

		for word in dict_word_directions.keys():
			score_dict[word]= evalScore(test_direction, word,dict_word_directions,pos_degree_increments)
		if type(block_label)==list:
		    row=[block_label[i],trialType_label,i+1,'',test_direction,'','','']
		else:   
		    row=[block_label,trialType_label,i+1,'',test_direction,'','','']
		print score_dict
		for each_score in sorted(score_dict.keys()):
		    score = score_dict[each_score]
		    row.append(score_dict[each_score])
		#added: info on specific items
		nearbyCounter=0
		for each_score in sorted(score_dict.keys()):
		    score = score_dict[each_score]
		    if score > 0:
		        nearbyCounter+=1
		        row.append(each_score)
		        row.append(dict_word_directions[each_score])
		        row.append([item for item in sorted_dict_list if item[1][0] == each_score][0][1][1])
		        
		if nearbyCounter<2:
		    row = row + ['NA','NA','NA']

		        
		#feedback params
		row = row + [1,'partial']
 		
 		#add subject info
  		row = info + row
		
		wrows.append(row)
	print score_dict

					
def writeBlock(rows, filename, header=[], ext='.txt', method='a', delim='\t',initBuffer=0,endBuffer=0):
	f = open(filename+ext, method)
	lineCount=0
	
	def buffer(size):
		for i in range(size):
			f.write('\n')
		
	if len(header)>0:
		for col in header:
			f.write(str(col))
			f.write(delim)
		f.write('\n')
		
	for row in rows:
	
		buffer(initBuffer)
		
		for col in row:
			f.write(str(col))
			f.write(delim)
		f.write('\n')
		
		buffer(endBuffer)
		
	f.close()		

################
# Runtime Init #

def generateTrials(runTimeVars,runTimeVarsOrder):
    
	cbal_Header=['block','trialType', 'trial','target','angle','left','right','freq'] #later, cols are appended by words included

	wrows=[] #for write to file

	#add runtime info
	info=[]
	for curRuntimeVar in runTimeVarsOrder:
		info.append(runTimeVars[curRuntimeVar])
		
	#set seed
	random.seed(int(runTimeVars['seed']))

	print int(runTimeVars['seed'])

	########################
	# Make Learning Distro #
	########################
	
	# We input list of possible words (20) and size of vocabulary we want (8).
	subset_of_full_list = list_subsetter(input_word_list,subSize)
	
	# Give it our 8 words, and an hf:lf vocab ratio (1:1); it returns two lists of four words.
	separated_lists = convert_ratio(subset_of_full_list,proportion_hf_vocab)
	
	# runtime counterbalance var to invert label-to-frequency assignment.
	if int(runTimeVars['labelAssign'])==1:
	    pass
	elif int(runTimeVars['labelAssign'])==2:
	    separated_lists=separated_lists[::-1]
	    

	print "\n\nHF list:"
	print separated_lists[0]
	print "\nLF list:"
	print separated_lists[1]


	# make two separate counterbalanced versions
	list_with_frequencies = frequency_maker(separated_lists,hf_to_lf_ratio,order=1)
	list_with_frequencies_reversed = frequency_maker(separated_lists,hf_to_lf_ratio,order=2)


	cbalFrequencies = [list_with_frequencies,list_with_frequencies_reversed]
	cbalOrdered = []
	for cbalVersion in cbalFrequencies:
		random.shuffle(cbalVersion)
		cbalOrdered.append(cbalVersion)
		#	cbalOrdered.append(randoCleaner(cbalVersion))
	
	#####################
	# Degrees for words #
	#####################

	pos_degree_increments = 360 / subSize # 6

	if not subSize==8 and proportion_hf_vocab==.5:
		print "Warning: experiment was designed for subsize 8, proportion .5"

	alternating_items = [[],[]] #template for two, hf/lf counterbalanced mappings of the same clock

	for i in range(len(separated_lists[0])/2):
		alternating_items[0].append((separated_lists[0][0+2*i],'hf'))
		alternating_items[0].append((separated_lists[0][1+2*i],'hf'))
		alternating_items[0].append((separated_lists[1][0+2*i],'lf'))
		alternating_items[0].append((separated_lists[1][1+2*i],'lf'))
		
		alternating_items[1].append((separated_lists[1][0+2*i],'lf'))
		alternating_items[1].append((separated_lists[1][1+2*i],'lf'))
		alternating_items[1].append((separated_lists[0][0+2*i],'hf'))
		alternating_items[1].append((separated_lists[0][1+2*i],'hf'))
		
		
	# print "\n\nalternating items list 1 and then 2"
	print alternating_items[0]
	print alternating_items[1]

	dict_word_directions={}
	sorted_dict_list = []
	alternating_items_index=((int(runTimeVars['angleAssign'])-1)+(int(runTimeVars['labelAssign'])-1))%2

	for i,word in enumerate(alternating_items[alternating_items_index]):
		value = ((i+1) *pos_degree_increments + angle_offset) % 360
		dict_word_directions[word[0]]= value
		sorted_dict_list.append((value,word))

	print sorted(sorted_dict_list)



	###################
	# Non-verbal Trls #
	###################
	# For participants to do the exact counterbalance of learning trials,
	# See "Learning Trials" for details on this counterbalance. 

	#lf word trials (separated_lists[1]) are assigned to hf non-verbal trials
	w_d=separated_lists[1][0]
	w_a=separated_lists[1][1]
	w_b=separated_lists[1][2]
	w_c=separated_lists[1][3]

	#hf word trials (separated_lists[0]) are assigned to lf non-verbal trials
	w_e=separated_lists[0][0]
	w_f=separated_lists[0][1]
	w_g=separated_lists[0][2]
	w_h=separated_lists[0][3]

	trial_template=[
	(w_a, w_b),
	(w_a, w_c),
	(w_a, w_d),
	(w_a, w_e),
	(w_b, w_a),
	(w_b, w_c),
	(w_b, w_d),
	(w_b, w_f),
	(w_c, w_a),
	(w_c, w_b),
	(w_c, w_d),
	(w_c, w_g),
	(w_d, w_a),
	(w_d, w_b),
	(w_d, w_c),
	(w_d, w_h),
	(w_e, w_a),
	(w_f, w_b),
	(w_g, w_c),
	(w_h, w_d)]

	random.shuffle(trial_template)

	# learningTrials = pairTest(cbalOrdered[0])
	learningTrials = pairTest(dict_word_directions,trial_template,learn_type = "nonverbal",genFromScratch=False)

	print "nverbal pair info: "
	print trial_template[0]
	# print learningTrials[0]

	for row in learningTrials:
		print row
		# print info
		row = info + list(row) + ['NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA']
		wrows.append(row)
	
	#######################
	# Write initial naming block##
	#######################
	
	#write block
	ct=0
	header_add=[]
	for line in sorted(sorted_dict_list):
		ct+=1
		block, word, angle, word_freq = ("init",line[1][0],line[0],line[1][1])
		row = [block,"name",ct, word, angle,'NA','NA',word_freq,'NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA']
		row = info + row
		wrows.append(row)
		header_add.append(word)
		# header_add.append(dict_word_directions[word])
		print word

	cbal_Header.extend(sorted(header_add))
	print cbal_Header
	
	###################
	# Learning Trials #
	###################

	##HARDCODED LEARNING TRIALS#
	# Rather than getting the rando cleaner to work, we're using a hardcoded set of counterbalanced, HF/LF target and alternative words. pairTest takes these and shuffles L/R setting, and prepares relevant details for runtime, (e.g. correct answer).

	#hf trials
	w_d=separated_lists[0][0]
	w_a=separated_lists[0][1]
	w_b=separated_lists[0][2]
	w_c=separated_lists[0][3]

	#lf trials
	w_e=separated_lists[1][0]
	w_f=separated_lists[1][1]
	w_g=separated_lists[1][2]
	w_h=separated_lists[1][3]

	# I think this is redundant...
	trial_template=[
	(w_a, w_b),
	(w_a, w_c),
	(w_a, w_d),
	(w_a, w_e),
	(w_b, w_a),
	(w_b, w_c),
	(w_b, w_d),
	(w_b, w_f),
	(w_c, w_a),
	(w_c, w_b),
	(w_c, w_d),
	(w_c, w_g),
	(w_d, w_a),
	(w_d, w_b),
	(w_d, w_c),
	(w_d, w_h),
	(w_e, w_a),
	(w_f, w_b),
	(w_g, w_c),
	(w_h, w_d)]

	random.shuffle(trial_template)


	# learningTrials = pairTest(cbalOrdered[0])
	learningTrials = pairTest(dict_word_directions,trial_template,learn_type = "verbal",genFromScratch=False)

	print "trial pair info: "
	print trial_template[0]
	print learningTrials[0]

	for row in learningTrials:
		print row
		# print info
		row = info + list(row) + ['NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA']
		wrows.append(row)


	#####################
	# Learning pre-test #	
	#####################

	# Random sample from init block

	#############	
	#TEST TRIALS#
	#############
	cbal_Header.extend(['nearbyLabel1','nearbyAngle1','nearbyFreq1','nearbyLabel2','nearbyAngle2','nearbyFreq2','updateScore','feedback'])
	#Test trial A uses zones around target words, sampled according to word frequency distribution.
	#Test trial B uses zones between target words sampled randomly.
	separated_lists[0] #hf items
	separated_lists[1] #lf items
	pos_degree_increments #space between items. /4 = +/- value. /2 = zones. 
	dict_word_directions
    # value = ((i+1) *pos_degree_increments + angle_offset) % 360

		
    ################
    # Test Trial A #
    ################
	multiple=3
	offset=0
	ratio=hf_to_lf_ratio #if hf_to_lf_ratio is 4, this is the equivalent multiple of 5
	test_trial_gen_A=areaSpecificDegreeGen(pos_degree_increments,separated_lists,dict_word_directions,multiple,offset,ratio)
	
    # testBlockScores(test_trial_gen_A,'test_a','test',dict_word_directions,sorted_dict_list,pos_degree_increments,info,wrows)	

	#NEW
	block_A_items = test_trial_gen_A[0:20]
	testBlockScores(block_A_items,'clear','test',dict_word_directions,sorted_dict_list,pos_degree_increments,info,wrows)	#for exp2.2, modified to only take first 20 items.
	#END NEW#
	
	
    ################
    # Test Trial B #
    ################
	multiple=8
	offset=1
	ratio=1 #multiple of 2
	test_trial_gen_B=areaSpecificDegreeGen(pos_degree_increments,separated_lists,dict_word_directions,multiple,offset,ratio)
	
    # testBlockScores(test_trial_gen_B,'test_b','test',dict_word_directions,sorted_dict_list,pos_degree_increments,info,wrows)

	#NEW#
	#2017.06.21 We need to interleave the items for wc2.2
	remaining_A_items = test_trial_gen_A[20:]
	list_size_difference = len(test_trial_gen_B)-len(test_trial_gen_A)

	interleaved_items=[]

	while len(test_trial_gen_B)>list_size_difference:
		a = (test_trial_gen_B.pop(),'ambig')
		b = (test_trial_gen_B.pop(),'ambig')
		c = (test_trial_gen_B.pop(),'ambig')
		d = (remaining_A_items.pop(),'clear2')
		e = (remaining_A_items.pop(),'clear2')
		
		tmp=[a,b,c,d,e]
		random.shuffle(tmp)
		interleaved_items.extend(tmp)
		
	for test_trial_gen_B_item in test_trial_gen_B:
	   interleaved_items.append((test_trial_gen_B_item,'ambig'))  
	   
	print(interleaved_items) 
	 
	#testBlockScores(test_trial_gen_B,'test_b','test',dict_word_directions,sorted_dict_list,pos_degree_increments,info,wrows)
	interleaved_item_list =[]
	trial_name_list=[]
	for (interleaved_item,trial_name) in interleaved_items:
	    interleaved_item_list.append(interleaved_item)
	    trial_name_list.append(trial_name)
	    
	    
	testBlockScores(interleaved_item_list,trial_name_list,'test',dict_word_directions,sorted_dict_list,pos_degree_increments,info,wrows)

	#END NEW#

    
    ################
    # final eval blk #
    ################
    
	#integrated test
	testBlockScores(dict_word_directions.values(),'test_x','test',dict_word_directions,sorted_dict_list,pos_degree_increments,info,wrows)
	


    ################
    # final eval blk #
    ################
    
	#write block
	ct=0
	header_add=[]
	random.shuffle(sorted_dict_list)
	for line in sorted_dict_list:
		ct+=1
		block, word, angle, word_freq = ("name_check",line[1][0],line[0],line[1][1])
		row = [block,"finalName",ct, word, angle,'NA','NA',word_freq,'NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA']
		row = info + row
		wrows.append(row)
		header_add.append(word)
		print word


	#Set header
	header = runTimeVarsOrder
	header.extend(cbal_Header) 	
	print header
	#####
	# Write block
	writeBlock(wrows, 'trials/'+runTimeVars['subjCode']+'_trials', header=header, ext='.txt', method='w', delim='\t')

	#return subset_of_full_list
	return header_add