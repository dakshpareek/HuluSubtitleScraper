import requests,json,re,os,sys
from bs4 import BeautifulSoup
import urllib.request
import json
from pathlib import Path

def make_srt(cid,vid,chk=False):
  #getting smi file link
  #print(vid)
  smiLink = ""
  xmlLinkTemplate = "http://www.hulu.com/captions.xml?content_id="
  xmlLink = xmlLinkTemplate + str(cid)
  xmlRequest = requests.get(xmlLink)
  smiSoup = BeautifulSoup(xmlRequest.text, "lxml")
  li = smiSoup.find("transcripts")
  listOfLanguages = li.findChildren()
  try:
    smiLink = smiSoup.find(listOfLanguages[0].name).string
    #print(smiLink)

    #getting vtt link
    vttLink = ""
    replaceDict = {"captions": "captions_webvtt", "smi": "vtt"}

    for keys in replaceDict:
      smiLink = smiLink.replace(keys, replaceDict[keys])
    vttLink = smiLink
    #print(vttLink)


    #creating vtt file
    requestObjectv = requests.get(vttLink)
    subsFileHandler = open(str(vid) + ".vtt", "w",encoding='utf-8')
    subsFileHandler.write(requestObjectv.text)
    subsFileHandler.close()


    f = open(str(vid) + ".vtt", "r",encoding='utf-8')
    fh = open(str(vid) + ".srt", "w",encoding='utf-8')

    count = 1

    # Removing WEBVTT Header line.
    for line in f.readlines():
        if line[:6] == 'WEBVTT':
            continue
        # Substituting '.' with ',' in the time-stamps
        line = re.sub(r'(:\d+)\.(\d+)', r'\1,\2', line)
        # Printing the header number in each line. This is required for the
        # SRT format.
        if line == '\n':
            fh.write("\n" + str(count) + "\n")
            count += 1
        else:
            fh.write(line.strip() + "\n")

    f.close()
    fh.close()
    os.remove(str(vid) + ".vtt")
    if not os.path.exists("movie-data"):
      os.makedirs("movie-data")
    if chk==True:
      mkstr="movie-data/"+str(vid)
    else:
      mkstr="tv-data/"+str(vid)
    os.rename(str(vid) + ".srt", mkstr + ".srt")
    return 1
    #print("SRT")
  except Exception as e:
    print("No Sub")
    return 0

def result(sid,gen,sub_gen,at):
  url="https://mozart.hulu.com/v1.h2o/shows/"+str(sid)+"/episodes?free_only=0&include_nonbrowseable=1&show_id=35077&sort=seasons_and_release&video_type=episode&_language=en&_region=us&items_per_page=32&position=0&_user_pgid=8195&_content_pgid=29635&_device_id=1&region=us&locale=en&language=en&require_ssl=1&access_token="+at+"&isHttps=true"
  r = requests.get(url)
  response=r.json()
  episodes=response['data']
  try:
    print("Series:-->  "+episodes[0]['video']['show']['name'])
  except:
    pass
  for i in episodes:
    #print(i)
    j={'data':[]}
    vid=i['video']['id']
    if not os.path.exists("tv-data"):
      os.makedirs("tv-data")
    if Path("tv-data/"+str(vid) + ".srt").is_file():
      print("Skipping--> "+i['video']['title'])
    else:
      if Path("tv-data/"+str(vid) + ".nosub").is_file():
        print("NoSUB Found")
      else:
        j['data'].append({'video-id':vid})
        cid=i['video']['content_id']
        duration=float(i['video']['duration'])/60
        j['data'].append({'series':episodes[0]['video']['show']['name']})
        j['data'].append({'title':i['video']['title']})
        j['data'].append({'duration':str(round(duration,2)) + ' min' })
        j['data'].append({'released_at':i['video']['original_premiere_date'].split('T')[0]})
        j['data'].append({'genre':gen})
        j['data'].append({'sub-genre':sub_gen})
        ckk=make_srt(cid,vid)
        if ckk==1:
          urllib.request.urlretrieve(i['video']['thumbnail_url'], str(vid)+".jpg")
          os.rename(str(vid)+".jpg", "tv-data/"+str(vid)+".jpg")
          with open(str(vid)+'.json', 'w') as outfile:
              json.dump(j, outfile)
          os.rename(str(vid)+'.json', "tv-data/"+str(vid)+'.json')
          print("   "+i['video']['title'])
        else:
          fh = open(str(vid)+".nosub","w")
          fh.close()
          os.rename(str(vid) + ".nosub", "tv-data/"+str(vid) + ".nosub")   
    print("------")