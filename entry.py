import requests,time,pygame,json
from datetime import datetime
now = datetime.now()
print("starting time: ",now.strftime("%H:%M:%S"))
pygame.init()
pygame.mixer.music.load("sound_dingdong.wav")
counter = 0
def get_data():
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict"
    params={"district_id":583,"date":"27-05-2021"}
    headers = {
        'user-agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }
    response = requests.get(url=url,params=params,headers=headers)
    data = response.json()
    global counter
    with open('count.txt', 'a') as outfile:
        outfile.write(str(counter)+" ")
    counter+=1
    return data

status = 1 
#1=still slot not found 2=slot found 3=slots closed

while True:
    data = get_data()
    if('sessions' not in data):
        time.sleep(3)
        continue
    if len(data['sessions'])==0:
        time.sleep(3)
        continue
    if(status==1):
        now = datetime.now()
        status=2
        print("********************************************************************")
        print("****************** Found the first slot time ***********************")
        print("*********************** "+now.strftime("%H:%M:%S")+" ***********************************")
        print("********************************************************************")
        with open('first_slot_data.txt', 'a') as outfile:
            outfile.write("slots opening time: "+now.strftime("%H:%M:%S")+"\n")
            json.dump(data, outfile)
        time.sleep(3)
        pygame.mixer.music.play(0)
        while pygame.mixer.music.get_busy():
            dummy = 1
        continue
    if(status==2):
        now = datetime.now()
        with open('extra_log.txt','a') as outfile:
            outfile.write("\n*****************************time: "+now.strftime("%H:%M:%S")+"************************************\n")
            json.dump(data, outfile)
    pygame.mixer.music.play(0)
    while pygame.mixer.music.get_busy():
        dummy = 1
    time.sleep(3)