import os
import csv
homedir="C:\Users\RahulHP\Tagger\Data"
#homedir="G:\My Songs"

#log=open('log.csv','wb')
#writer=csv.writer(log)
replace = ['0','1','2','3','4','5','6','7','8','9','-','[',']','(',')','=','&']


for f in os.listdir(homedir):
	filename=str(f).split('.')[0]
	if str(f).split('.')[-1]=='mp3':
	#print filename.replace('0','')
		new=filename.translate(None,''.join(replace)).strip().title()
	else:
		new=filename
	print filename
	print new
	' '.join(new.split())
	newfilename=homedir+'\\'+new+'.mp3'
	oldfilename=homedir+'\\'+f
	os.rename(oldfilename,newfilename)


