import requests,os,time
from main import make_srt
from pathlib import Path
import urllib.request
import json

def generate(gen,sub_gen,at):
  count=0
  chk=None
  while True:
    link1="https://mozart.hulu.com/v1.h2o/movies/films?exclude_hulu_content=1&genre="+str(gen.lower())+"&sort=popular_all_time&_language=en&_region=us&items_per_page=32&position="+str(count)+"&_user_pgid=8195&_content_pgid=29635&_device_id=1&region=us&locale=en&language=en&require_ssl=1&access_token="+at+"&isHttps=true"
    link2="https://mozart.hulu.com/v1.h2o/movies/films?exclude_hulu_content=1&genre="+str(gen.lower())+"~"+str(sub_gen.lower())+"&sort=popular_all_time&_language=en&_region=us&items_per_page=32&position="+str(count)+"&_user_pgid=8195&_content_pgid=29635&_device_id=1&region=us&locale=en&language=en&require_ssl=1&access_token="+at+"&isHttps=true"
    if sub_gen=="":
      r1 = requests.get(link1)
    else:
      r1 = requests.get(link2)
    #print(link1)
    response1=r1.json()
    #print(response1["data"])
    #break
    try:
      chk1=response1["data"][-1]["video"]['id']
    except:
      break
    if chk1==chk:
      break
    else:
      chk=chk1
    for i in response1["data"]:
      vid=(int(i["video"]['id']))
      if Path("movie-data/"+str(vid) + ".jpg").is_file():
        print("Skipping--> "+i["video"]['title'])
      else:
        if Path("movie-data/"+str(vid) + ".nosub").is_file():
          print("NoSUB Found")
        else:
          j={'data':[]}
          print(i["video"]['title'])
          cid=i["video"]['content_id']
          duration=float(i["video"]['duration'])/60
          #print(i["video"]['released_at'])
          #print(i["video"]['thumbnail_url'])
          j['data'].append({'video-id':vid})
          j['data'].append({'title':i['video']['title']})
          j['data'].append({'duration':str(round(duration,2)) + ' min' })
          j['data'].append({'released_at':i['video']['original_premiere_date'].split('T')[0]})
          j['data'].append({'genre':gen})
          j['data'].append({'sub-genre':sub_gen})
          ckk=make_srt(cid,vid,True)
          if ckk==1:
            urllib.request.urlretrieve(i['video']['thumbnail_url'], str(vid)+".jpg")
            try:
              os.rename(str(vid)+".jpg", "movie-data/"+str(vid)+".jpg")
            except:
              pass
            with open(str(vid)+'.json', 'w') as outfile:
              json.dump(j, outfile)
            os.rename(str(vid)+'.json', "movie-data/"+str(vid)+'.json')
          else:
            fh = open(str(vid)+".nosub","w")
            fh.close()
            os.rename(str(vid) + ".nosub", "movie-data/"+str(vid) + ".nosub")
          print("-*-*-*-")
      #break
    try:
      time.sleep(sys.argv[1])
    except:
      pass
    count+=1
    #break
    

at="5TCe7zLTgYY9QKML/VQM0P675/E-U/VKKghIRP2su3bwCyPYOQ--vInOvP3WYcUMn9S6kWdwAFB8FY/j4/YK/Ovtg4OTlnt7kVOb4ZlD9PeKvKUig11pRAWeneJX4RrcyrW4YjlfkSoWpKAqVHqjIelFslR0fYdowZjDz1/FCDMtcn0bCuv26Fv28xDL53h8UOzazz9R7ReqbtYAUU7lJE_AZhsUyqz0yODksyCyP2l1E/DxrYRcCKkj_LVV2L1CnV/qiaMud2bviHy6gUCv5U6o3Le5i43DLdEQOg9weX3aiQxFf_jCzriAXSlb6diq0A7tibiZEQ--" 
all_genre="https://mozart.hulu.com/v1.h2o/movies/genres?sort=name&_language=en&_region=us&items_per_page=32&position=0&_user_pgid=8195&_content_pgid=29635&_device_id=1&region=us&locale=en&language=en&require_ssl=1&access_token="+at+"&isHttps=true"
#print(all_genre)
r = requests.get(all_genre)
response=r.json()
e=response['data']
for i in e:
  try:
    gen=i['genre']['name']
    generate(gen,"",at)
    sub_gen=i['genre']['subgenres']
  except Exception as e:
    #print(e)
    pass
  for k in sub_gen:
    try:
      generate(gen,k,at)
    except:
      pass
  print('----')
