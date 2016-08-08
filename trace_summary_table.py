from collections import defaultdict
import pandas as pd
import numpy as np
import os
import sys


input_folder = sys.argv[1]
##output_folder = sys.argv[2]
def main():
	
	for filename in os.listdir(input_folder):
		the_file = os.path.join(input_folder, filename)
		df = pd.read_csv(the_file)
		print "############################"
		print filename
		print "Mean: " + str(np.average(df.n_hops))
		print "Sd: " + str(np.std(df.n_hops))
		print "Min: " + str(np.amin(df.n_hops))
		print "Max: " + str(np.amax(df.n_hops))
		print "Flutters per path: " + str(np.average(df.flutters))
		print "Amount of no responses per path: " + str(np.average(df.amt_of_no_resp))


if __name__ == '__main__':
	main()
