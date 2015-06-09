import logging
logging.basicConfig(filename='sample2.log',level=logging.DEBUG,filemode='w',disable_existing_loggers=False)

import os
import json
import requests
import eyed3

apiurl="http://api.gaana.com/index.php?type=search&subtype=search_song&key="
start_dir='E:\RahulHP\The Playground\Tagger\Data'
final_dir='E:\RahulHP\The Playground\Tagger\Done'

def get_json_response(url,search_string):
	requesturl=url+search_string
	jsonresponse=requests.get(requesturl)
	data=json.loads(jsonresponse.content)
	return data

def extract_song_data(songdata):
	tracktitle=songdata["tracks"][0]["track_title"].encode('utf-8')

	album= songdata["tracks"][0]["album_title"].encode('utf-8')
	singercount=0
	singerstr=""
	for i in songdata["tracks"][0]["artist"]:
		singercount=singercount+1
		if singercount==1:
			singerstr=singerstr+str(i["name"])
		else:
			singerstr=singerstr+' ,'+str(i["name"])
	return tracktitle,album,singerstr.encode('utf-8')

def write_to_mp3(start_dir,filename,tracktitle,album,singerstr):
	audiofile=eyed3.load(start_dir+'\\'+filename)
	audiofile.tag.artist = singerstr.decode('utf-8','ignore')
	audiofile.tag.album_artist = unicode("","utf-8")
	audiofile.tag.album = album.decode('utf-8','ignore')
	audiofile.tag.title = tracktitle.decode('utf-8','ignore').strip('\n')
	audiofile.tag.track_num = None, None
	audiofile.tag.save()

def file_ops(start_dir,songfile,final_dir,tracktitle,album):
	new_filename="{0} - {1}.mp3".format(tracktitle.strip('\n'),album)
	os.rename(start_dir+'\\'+songfile,final_dir+'\\'+new_filename)

def cleaner(actual_filename):
	replacer = ['0','1','2','3','4','5','6','7','8','9','[',']','(',')','=','&','songs','pk','www']
	new=actual_filename
	for word in replacer:
		new=new.replace(word,'')
	return new.strip()

def tagger():
	for songfile in os.listdir(start_dir):
		try:
			print songfile
			logging.info('%s' % (songfile))
			file_type=songfile.split('.')[-1]
			if file_type != 'mp3':
				logging.info('\t%s is not an mp3 file.' % (songfile))
				continue
			actual_name=songfile.split('.')[0]
			clean_name=cleaner(actual_name)
			if '-' in str(clean_name): ## Assuming file name is type "Album - Song.mp3"
				songname=str(clean_name).split('-')[-1].strip()
			else:
				songname=str(clean_name)
			logging.info('\tTrack Name - %s' % (songname))
			
			songdata = get_json_response(apiurl,songname)
			if songdata["count"]==0:
				logging.info('\t%s with track name %s not found.' % (songfile,songname))
				continue

			logging.debug('\tExtracting data')
			tracktitle,album,singerstr = extract_song_data(songdata)
			logging.debug('\tWriting data to mp3')
			write_to_mp3(start_dir,songfile,tracktitle,album,singerstr)
			logging.debug('\tMoving File')
			file_ops(start_dir,songfile,final_dir,str(tracktitle),str(album))
			logging.info('\tFile %s completed.' % (songfile))
		except Exception as e:
			logging.info('\tSong %s failed: %s' % (songfile,str(e)))

tagger()