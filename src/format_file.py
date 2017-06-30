import glob
import os

files 		= glob.glob("../output/Financial Data/*.csv")
codeFile	= "../output/StockCodesNYSE.csv"

def detect_empty(file):
	data 		= open(file,'r').read()
	lines		= data.split('\n')
	for line in lines:
		fields	= line.split('|')
		if len(fields)>1:
			return False
	return True

def check_count():
	data 		= open(codeFile,'r').read()
	records		= data.split('\n')
	for record in records:
		code 	= record.split(',')[0]
		files 	= glob.glob("../output/Formatted/temp/"+code+"-*.csv")
		if len(files) == 3:
			for file in files:
				os.remove(file)
		# if len(files)>0 and len(files)<3:
			# print(code)

if __name__ == "__main__":
	# check_count()
	"""
		Uncomment the following code to check and remove empty data files
	"""
	# for file in files:
	# 	if detect_empty(file) == True:
	# 		os.remove(file)
	# 		print(file)
