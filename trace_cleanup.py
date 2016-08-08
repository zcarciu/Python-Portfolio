import csv
import re
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
from datetime import datetime


def main():

	continue




def get_all_paths_from_trace():

	for data_file in os.listdir(sys.argv[1]):	

		trace_or_ping, send_host, rec_host, _date, _time = \
			get_info_from_filename(data_file)
		
		new_filename = "%s_TO_%s.csv" % (send_host, rec_host)

		path = []	

		with open(os.path.join(sys.argv[1], data_file), 'r') as f:
			for i in f.readlines()[1:]:
				regex = re.compile("\(\d+\.\d+\.\d+\.\d+\)")
				abc = "$".join(regex.findall(i))
				if len(abc) == 0: abc = "*"
				path.append(abc)

		hops = len(path)
		path = "#".join(path)
		row = [_date, _time, hops, path]
		headers = ["date", "time", "hops", "path"]

		with open(os.path.join("trace_path_data", new_filename), "a+") as f:
			csv_writer = csv.writer(f)
			if os.path.getsize(f.name) == 0: csv_writer.writerow(headers)
			csv_writer.writerow(row)

	

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
	


def find_between(s, first, last):
	try:
		start = s.index(first) + len(first)		
		end = s.index(last, start)
		return s[start:end]
	except ValueError:
		return ""


if __name__ == '__main__':
	main()
