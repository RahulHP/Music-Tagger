import os
import csv
import json
import requests
from pprint import pprint
import eyed3
logfile=open('logfile.csv','a')
logwriter=csv.writer(logfile)
notdone=open('notdone.txt','a')
homedir="G:\My Songs"
apiurl="http://s.staging.api.gaana.com/index.php?type=search&subtype=search_song&key="

for song in os.listdir(homedir):
	print song
	try:
		jsonurl=apiurl+str(song).split('.')[0]
		#print jsonurl
		response=requests.get(jsonurl)
		#print response
		#f=open(jsonurl)
		data=json.loads(response.content)
		if data["count"]==0:
			logwriter.writerow([str(song).split('.')[0]])
			notdone.write(str(song)+'\n')
			#print str(song).split('.')[0]
			continue
		tracktitle=data["tracks"][0]["track_title"]
		album= data["tracks"][0]["album_title"]
		singer=[]
		singerstr=""
		#print data["tracks"][0]["artist"]
		singercount=0
		for i in data["tracks"][0]["artist"]:
			singercount=singercount+1
			singer.append(i["name"])
			if singercount!=1:
				singerstr=singerstr+' ,'+str(i["name"])
				continue
			singerstr=singerstr+str(i["name"])
		
		#print singerstr


		audiofile=eyed3.load(homedir+'\\'+song)
		audiofile.tag.artist = singerstr.decode('utf-8','ignore')
		audiofile.tag.album_artist = unicode("","utf-8")
		audiofile.tag.album = album.decode('utf-8','ignore')
		audiofile.tag.title = tracktitle.decode('utf-8','ignore')
		audiofile.tag.track_num = None, None
		audiofile.tag.save()

		new_filename="{0} - {1}.mp3".format(audiofile.tag.title,audiofile.tag.album)

		logwriter.writerow([str(song).split('.')[0],tracktitle,album,singer,new_filename])
		print new_filename
		try:
			os.rename(homedir+'\\'+song,homedir+'\\'+'Done\\'+new_filename)
		except:
			continue
	except:
		continue


