import requests,os,time
from main import result


def generate(gen,sub_gen,at):
  count=0
  chk=None
  while True:
    link1="https://mozart.hulu.com/v1.h2o/shows?exclude_hulu_content=1&genre="+str(gen.lower())+"&sort=popular_all_time&_language=en&_region=us&items_per_page=32&position="+str(count)+"&_user_pgid=8195&_content_pgid=29635&_device_id=1&region=us&locale=en&language=en&require_ssl=1&access_token="+at+"&isHttps=true"
    link2="https://mozart.hulu.com/v1.h2o/shows?exclude_hulu_content=1&genre="+str(gen.lower())+"~"+str(sub_gen.lower())+"&sort=popular_all_time&_language=en&_region=us&items_per_page=32&position="+str(count)+"&_user_pgid=8195&_content_pgid=29635&_device_id=1&region=us&locale=en&language=en&require_ssl=1&access_token="+at+"&isHttps=true"
    if sub_gen=="":
      r1 = requests.get(link1)
    else:
      r1 = requests.get(link2)
    #print(link1)
    response1=r1.json()
    try:
      chk1=response1["data"][-1]["show"]['id']
    except:
      break
    if chk1==chk:
      break
    else:
      chk=chk1
    print("Genre: "+gen)
    print("Sub Gen: "+sub_gen)
    print("For :"+str(count))
    for i in response1["data"]:
      try:
        result(int(i["show"]['id']),gen,sub_gen,at)
      except:
        pass
    try:
      time.sleep(sys.argv[1])
    except:
      pass
    count+=1
    

at="5TCe7zLTgYY9QKML/VQM0P675/E-U/VKKghIRP2su3bwCyPYOQ--vInOvP3WYcUMn9S6kWdwAFB8FY/j4/YK/Ovtg4OTlnt7kVOb4ZlD9PeKvKUig11pRAWeneJX4RrcyrW4YjlfkSoWpKAqVHqjIelFslR0fYdowZjDz1/FCDMtcn0bCuv26Fv28xDL53h8UOzazz9R7ReqbtYAUU7lJE_AZhsUyqz0yODksyCyP2l1E/DxrYRcCKkj_LVV2L1CnV/qiaMud2bviHy6gUCv5U6o3Le5i43DLdEQOg9weX3aiQxFf_jCzriAXSlb6diq0A7tibiZEQ--"
all_genre="https://mozart.hulu.com/v1.h2o/shows/genres?sort=name&_language=en&_region=us&items_per_page=32&position=0&_user_pgid=8195&_content_pgid=29635&_device_id=1&region=us&locale=en&language=en&require_ssl=1&access_token="+at+"&isHttps=true"
r = requests.get(all_genre)
response=r.json()
e=response['data']
for i in e:
  gen=i['genre']['name']
  generate(gen,"",at)
  sub_gen=i['genre']['subgenres']
  for k in sub_gen:
    try:
      generate(gen,k,at)
    except:
      pass
  print('----')