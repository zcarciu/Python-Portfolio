import os
import sys
import matplotlib.pyplot as plt
import matplotlib
import pylab
import pandas as pd


saved_images_folder = "saved_images"
raw_data_file = "ping_2016-4-2_sorted.csv" 
def main():

	if len(sys.argv) != 2:
		print 'len(sys.argv) = {}'.format(len(sys.argv))
		print "Usage: python data_visualization.py <data-folder>"
		sys.exit()


	if not os.path.exists(saved_images_folder):
		os.mkdir(saved_images_folder)
			
	#pingcsvfile = os.path.join("cleaned_data", raw_data_file)

	#plot_all_days_w_error_bars(sys.argv[1])

	#ping_boxplots_of_one_day(pingcsvfile, save_boxplots=True)
	
	#ping_line_graphs_one_day(pingcsvfile)

	## group summary graphs together
	## group simple graphs together


#expects a folder of sorted csv data
#where date is in filename 
def plot_all_days_w_error_bars(data_folder):
	
	nrows = 3
	ncols = 2
	fig, axes = plt.subplots(nrows, ncols)

	the_data = []

	for data_file in os.listdir(data_folder):
		
		if "ping" in data_file and "sorted" in data_file:
			df = pd.read_csv(os.path.join(data_folder, data_file))
			for i in list(sorted(set(df['from'].tolist()))):
					
		


#not quite finished
#legend in huge in plot
def ping_line_graphs_one_day(ping_csv_file, save_linegraphs=False):

	df = pd.read_csv(ping_csv_file)
	df['time'] = pd.to_datetime(df['time'], format="%H:%M:%S") 
	boxes = []
	times = []
	labs = []

	iterator = 0

	for i in set(df['from'].tolist()):
		boxes.append(df.loc[df['from'] == i]['avg_rtt'])
		times.append(df.loc[df['from'] == i]['time'])
		rec_host = list(df.loc[df['from'] == i]['to'])[0]

		current_label = i + "\nto\n" + rec_host
		plt.plot(times[iterator], boxes[iterator], label = current_label)
		plt.gcf().autofmt_xdate()
	
		iterator += 1

	plt.legend()		
	plt.show()

## if save_boxplots, will save in saved_images_folder 
## will not output plots
### email_boxplots(Me, Brad) ###########
def ping_boxplots_of_one_day(ping_csv_file, save_boxplots=False):

	## make 5 of these 
	## each will have the connection at the top 
	## as the title
	## each box plot will have 


	df = pd.read_csv(ping_csv_file)
	df['time'] = pd.to_datetime(df['time'], format="%H:%M:%S") 
	boxes = []
	times = []
	labs = []

	for i in set(df['from'].tolist()):
		boxes.append(df.loc[df['from'] == i]['avg_rtt'])
		times.append(df.loc[df['from'] == i]['time'])
		rec_host = list(df.loc[df['from'] == i]['to'])[0]
		labs.append(i + "\nto\n" + rec_host)

	plt.boxplot(boxes, labels = labs, vert=False)
	plt.title(ping_csv_file)

	if not save_boxplots:
		plt.show()
	else:
		new_name = ping_csv_file[0:-4] + ".png"
		new_name = new_name[13:]
		img_file = os.path.join(saved_images_folder, new_name)
		plt.savefig(img_file, bbox_inches='tight')

if __name__ == "__main__":
	main()
