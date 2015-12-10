import sys
from scipy import stats

COMPT = "Compatibility with other devices"
PRICE = "Price"
SECUR = "Security"
O_SRC = "Whether Open Source"
MNFCT = "Manufacturer"
SETUP = "How easy it is to use/setup."
RECOM = "Recommendations from peers"
RELIA = "Reliability/Quality"
OTHER = "Other"


TOTAL_SEC = 0
TOTAL_NOT = 0
SEC_SCORE = 0
NOT_SCORE = 0
N_S1 = 0
N_S2 = 0
N_S3 = 0
SEC1 = 0 
SEC2 = 0
SEC3 = 0

sec_rating = []
not_rating = []

def convert_csv_to_list(filename):
	''' Takes in a string filename to a csv, returns a list of lists'''
	f = open(filename, 'r')

	entries = []

	for line in f.readlines()[1:]:
		try:
			entry = line.split(',')[:-1]
			entry.append(int(line.split(',')[-1]))
			entries.append(entry)
		except:
			continue

	return entries


def populate_choice_dicts(entries):
	first_choices = make_empty_choice_dict();
	secon_choices = make_empty_choice_dict();
	third_choices = make_empty_choice_dict();
	overall_chocies = make_empty_choice_dict();

	def iterate_dict(choice_dict, choice):
		try:
			choice_dict[choice] += 1
		except KeyError:
			if is_reliability(choice):
				choice_dict[RELIA] += 1
			else:
				if choice != '':
					choice_dict[OTHER] += 1


	for entry in entries:
		iterate_dict(first_choices, entry[1])
		iterate_dict(secon_choices, entry[2])
		iterate_dict(third_choices, entry[3])

		iterate_dict(overall_chocies, entry[1])
		iterate_dict(overall_chocies, entry[2])
		iterate_dict(overall_chocies, entry[3])

		get_averages(entry)
		make_lists(entry)

	do_t_tests();

	print
	print "Average for those who put Security:     " + str(float(SEC_SCORE)/TOTAL_SEC)
	print "Average for those who put Security 1st: " + str(float(SEC1)/N_S1)
	print "Average for those who put Security 2nd: " + str(float(SEC2)/N_S2)
	print "Average for those who put Security 3rd: " + str(float(SEC3)/N_S3)
	print "Average for those who did not put Security:" + str(float(NOT_SCORE)/TOTAL_NOT)

	print

	print first_choices
	print secon_choices
	print third_choices
	print overall_chocies

def do_t_tests():
	two_sample = stats.ttest_ind(sec_rating, not_rating)

	print "The t-statistic is %.3f and the p-value is %.3f." % two_sample

	# assuming unequal population variances
	two_sample_diff_var = stats.ttest_ind(sec_rating, not_rating)

	print "If we assume unequal variances than the t-statistic is %.3f and the p-value is %.3f." % two_sample_diff_var

def make_lists(entry):
	global sec_rating
	global not_rating
	if SECUR in entry:
		sec_rating.append(entry[-1])
	else:
		not_rating.append(entry[-1])

def get_averages(entry):
	global TOTAL_SEC
	global SEC_SCORE
	global TOTAL_NOT
	global NOT_SCORE
	global SEC1
	global N_S1
	global SEC2, N_S2
	global SEC3, N_S3

	if SECUR in entry:
		TOTAL_SEC += 1
		SEC_SCORE += entry[-1]
		if SECUR == entry[1]:
			SEC1 += entry[-1]
			N_S1 += 1
		elif SECUR == entry[2]:
			SEC2 += entry[-1]
			N_S2 += 1
		elif SECUR == entry[3]:
			SEC3 += entry[-1]
			N_S3 += 1
	else:
		TOTAL_NOT += 1
		NOT_SCORE += entry[-1]

def is_reliability(c):
	c = c.lower()

	if "reliability" in c:
		return True
	elif "quality" in c:
		return True
	else:
		return False

def make_empty_choice_dict():
	rval = {}
	rval[COMPT] = 0
	rval[PRICE] = 0
	rval[SECUR] = 0
	rval[O_SRC] = 0
	rval[MNFCT] = 0
	rval[SETUP] = 0
	rval[RECOM] = 0
	rval[RELIA] = 0
	rval[OTHER] = 0

	return rval




entries = convert_csv_to_list("data2.csv")
populate_choice_dicts(entries)