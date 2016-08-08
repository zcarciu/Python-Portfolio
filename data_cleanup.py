import operator
import numpy as np
import csv
import fnmatch
import os
import sys
import pandas as pd
from datetime import datetime


def main():
	if len(sys.argv) != 2:
		print 'len(sys.argv) = {}'.format(len(sys.argv))
		print "Usage: python data_cleanup.py <data-folder>"
		sys.exit()


	######## folder of raw data! #############
	raw_data_folder = sys.argv[1]
	######## folder of cleaned data! ############
	cleaned_data_folder = os.path.join('.', 'cleaned_data')


	##### make sure file exists and is dir! #######
	if not os.path.exists(raw_data_folder) and os.path.isdir(raw_data_folder):
		print "Not a valid directory!"
		sys.exit(1)


	####### if cleaned_data file doesnt exist, create it! ####	
	if not os.path.isdir(cleaned_data_folder):
		os.mkdir(cleaned_data_folder)


	####### make sure cleaned data folder is empty before analysis!######
	for i in os.listdir(cleaned_data_folder):
		os.remove(os.path.join(cleaned_data_folder, i))

	####### fix naming error ####################
	for i in os.listdir(raw_data_folder):
		if i[i.index('2016-')-1] is ".":
			######### need to turn it into a list 
			######### because strings are immutable
			str_as_list = list(i)
			str_as_list[i.index('2016-')-1] = "_"
			
			######### change it back to a str #####
			new_name = "".join(str_as_list)
			os.rename(os.path.join(raw_data_folder, i),
						 os.path.join(raw_data_folder, new_name))

	

	####### iterate through raw data files ################
	for data_file in os.listdir(raw_data_folder):
			

		##### get type, date, time and hosts from filename #####
		trace_or_ping, send_host, rec_host, _date, _time = \
			get_info_from_filename(data_file)
			
		######################################################
		################  ping files  ########################
		if trace_or_ping == "ping":

			###### will hold all RTTs from current ping ####
			temp_rtt_array = []

			with open(os.path.join(raw_data_folder, data_file), 'r+') as rf:
				for line in rf.readlines():
					a = line.split(' ')	

					###### RTT is in 8th column i.e. a[7] ########
					if len(a) == 9:
						rtt = float(a[7].split('=')[1])
						temp_rtt_array.append(rtt)

			##### get mean and sd of RTTS  ###############
			n = len(temp_rtt_array)
			avg_rtt=0
			if n > 0:
				avg_rtt = sum(temp_rtt_array)/n
				sd_rtt = np.std(temp_rtt_array)


			####### each file will contain a day's worth of data ###
			csv_headers = ['time','from', 'to', 'avg_rtt', 'sd', '# of packets received'] 
	
			filename = "ping_%s.csv" % _date

			with open(os.path.join('cleaned_data', filename), 'a+') as wf:
				csv_writer = csv.writer(wf, delimiter=',')
				if os.path.getsize(wf.name) == 0:
					csv_writer.writerow(csv_headers)
				csv_writer.writerow([_time, send_host, 
										rec_host, avg_rtt, sd_rtt, n]) 


		##########################################################
		################  traceroute files!  #####################
		if trace_or_ping == "trace":
			
			####### declare metrics #########
			n_hops = 0
			one_ast = 0
			two_ast = 0
			three_ast = 0
			all_responded = 0

			#keep record of all unique paths taken 

			with open(os.path.join(raw_data_folder, data_file), 'r+') as rf:
				for line in rf.readlines():

					n_hops += 1

					a = line.split()	
					
					if a.count('*') == 3:
						three_ast += 1

					elif a.count('*') == 2:
						two_ast += 1

					elif a.count('*') == 1:
						one_ast += 1

					elif a.count('*') == 0:
						all_responded += 1

					else:	
						print "AHHHHHHHHHHHH the amount of '*' is not in [0,3] AHHHHHHHHHHHH!"


			####### each file will contain a day's worth of data ###
			csv_headers = ['time','from', 'to', '3 *s', '2 *s', '1 *s', 'all successes', 'n_hops', 'date']

			filename = "trace_%s.csv" % _date

			with open(os.path.join('cleaned_data', filename), 'a+') as wf:
				csv_writer = csv.writer(wf, delimiter=',')
				if os.path.getsize(wf.name) == 0:
					csv_writer.writerow(csv_headers)
				csv_writer.writerow([_time, send_host, rec_host, three_ast, two_ast, one_ast, all_responded, n_hops, _date])


	sort_files()


def get_info_from_filename(filename):
	####### ping or traceroute?!?! ###############
	if "trace" in filename:
		trace_or_ping="trace"
		###### extract hostnames ############
		send_host = find_between(filename, 'trace_stats_', '_')
		pattern_str = "trace_stats_{}_".format(send_host)
		rec_host = find_between(filename, pattern_str, '_2016') 
	elif "ping" in filename:
		trace_or_ping="ping"

		###### extract hostnames ############
		send_host = find_between(filename, 'ping_stats_', '_')
		pattern_str = "ping_stats_{}_".format(send_host)
		rec_host = find_between(filename, pattern_str, '_2016') 
	else:
		print "Uh oh.. filename doesnt contain 'trace' or 'ping' D:"


	date_time = datetime.strptime(filename[-19:], 
									'%Y-%m-%d-%H.%M.%S')
	_date = "%s-%s-%s" % (date_time.year, 
										date_time.month, date_time.day)
	_time = "%02d:%02d:%02d" % (date_time.hour, 
								date_time.minute, date_time.second)

	return (trace_or_ping, send_host, rec_host, _date, _time)
	



#assuming all files in directory are csv
#sorts csv file based on a column
def sort_files(col=0):
	for i in os.listdir(os.path.join(os.getcwd(), 'cleaned_data')):
		reader = csv.reader(open(os.path.join('cleaned_data', i), 'r'), delimiter=",")
		sortedlist=sorted(reader, key=operator.itemgetter(col), 
								reverse=False)
		##### add 'sorted' to sorted files' names ####
		new_file_name = "%s_sorted.csv" % i[0:-4]

		headers=sortedlist.pop()
		

		with open(os.path.join('cleaned_data', new_file_name), 'w+') as f:
			writer = csv.writer(f)
			writer.writerow(headers)
			writer.writerows(sortedlist)

####################
#>>> s = "123123STRINGabcabc"
#>>> print find_between( s, "123", "abc" )
#>>> 123STRING

# taken from 
# http://stackoverflow.com/questions/3368969/find-string-between-two-substrings
def find_between(s, first, last):
	try:
		start = s.index(first) + len(first)		
		end = s.index(last, start)
		return s[start:end]
	except ValueError:
		return ""

if __name__ == '__main__':
	main()
