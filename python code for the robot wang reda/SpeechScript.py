from datetime import date
import speech_recognition as sr
from random import *
import requests
import UserWrittenModules.MultiprocessingFunctions as multi
#check_words = ["hello radar","hello Radhika","hi radar","hello Radha","hey Radhika","hey radar","heda","Irada","Prada"]
check_words = ["hey assist","hello assist","hi assist"]
initial_response = ["hello man!,whats going on","hey!,what do want to know from me","namaskar, how can i help you","hoi,how can i be a help to you?"]
print("[INFO] |COMMUNICATION FEATURE IS ENABLED FOR 'WANG REDA'.")

count = 0
suslink=0
symdat=['','','','']
magret=[]
cco = 0
url = "https://reda.niran.dev/remote_sql.php?"

def arbit():
    print("\n*** Arbit Info ***")
    print("Col value: ",cco)
    print("Suspect Data: ")
    for x in range(len(symdat)):
        print (symdat[x] +", ")
    print("****************\n")
"""
while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        recognisedtext = str(r.recognize_google(audio))
        if recognisedtext not in check_words:
            print("[INFO] |REDA DO NOT RESPONDS AS SHE THINKS YOU SAID : "+recognisedtext)
        if recognisedtext in check_words:
            print("[REDA WAKES UP]")
            multi.MakeAwareness(initial_response[randint(0, 3)])
            print("[IF YOU DONT SPEAK >> REDA SLEEPS]")
            count = 0
            while True:
                R = sr.Recognizer()
                with sr.Microphone() as source:
                    R.adjust_for_ambient_noise(source)
                    print("[SPEAK]")
                    audio = R.listen(source)
                try:
                    recognisedtext = str(R.recognize_google(audio))
                    print("[YOUR RESPONSE] >> " + recognisedtext)
                    dialogflowresult = multi.DialogflowSocket(recognisedtext)
                    print("[REDA'S  REPLY] >> " + dialogflowresult)
                    multi.TextToSpeech(dialogflowresult)
                    count = 0
                except sr.UnknownValueError:
                    count+=1
                    if count > 2:
                        print("[REDA SLEEPS]")
                        break
                except sr.RequestError as e:
                    print("Could not process because of the reason : {0}".format(e))
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print("Could not process because of the reason : {0}".format(e))
"""
print("[INFO] |SAY 'HELLO ASSIST' TO WAKE REDA")
r = sr.Recognizer()
while True:

    print("[INFO] |SPEAK TO WAKEUP REDA")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("---")
        recognisedtext = str(r.recognize_google(audio))
        if recognisedtext not in check_words:
            print("[INFO] |REDA DO NOT RESPONDS AS SHE THINKS YOU SAID : " + recognisedtext)
        if recognisedtext in check_words:
            print("[REDA WAKES UP]")
            multi.MakeAwareness(initial_response[randint(0, 3)])
            print("[IF YOU DONT SPEAK >> REDA SLEEPS]")
            m = 0
            while True:
                R = sr.Recognizer()
                with sr.Microphone() as source:
                    R.adjust_for_ambient_noise(source)
                    print("SPEAK")
                    audio = R.listen(source)
                try:
                    print("---")
                    recognisedtext = str(R.recognize_google(audio))
                    print("[YOUR RESPONSE] >> " + recognisedtext)
                    magret = multi.DialogflowSocket(recognisedtext)
                    replyy = magret[0]
                    pscintentt = magret[2]

                    if (suslink == 1):
                        if (pscintentt == "Suspect - getname"):
                            arbit()
                            symdat[0] = recognisedtext
                            print("Name Taken")
                            cco += 1

                        elif (pscintentt == "Suspect - getaddress"):
                            arbit()
                            symdat[1] = recognisedtext
                            print("Address Taken")
                            cco += 1
                        elif (pscintentt == "Suspect - getage"):
                            arbit()
                            symdat[2] = recognisedtext
                            print("Age Taken")
                            cco += 1
                        elif (pscintentt == "Suspect - getsymptom"):
                            arbit()
                            symdat[3] = recognisedtext
                            print("Symptom Taken")
                            cco += 1
                        else:
                            arbit()
                            if (cco == 4):

                                date1 = str(date.today())
                                man = str(symdat[0])
                                adu = str(symdat[1])
                                agg = str(symdat[2])
                                simp = str(symdat[3])
                                data = {'suspected_name': man,
                                        'address': adu,
                                        'symptoms': simp,
                                        'suspected_age': agg,
                                        'reported_date': date1}
                                # urllib.request.urlopen('https://reda.niran.dev/remote_sql.php?suspected_name='+'papamaria '+man+'&address='+adu+'&symptoms='+simp+'&suspected_age='+agg+'&reported_date='+date1)
                                r = requests.post('https://reda.niran.dev/remote_sql.php?suspected_name='+man+'&address='+adu+'&symptoms='+simp+'&suspected_age='+agg+'&reported_date='+date1,verify=False)
                                print (r.text)
                                #uneurl = str(
                                #    'https://reda.niran.dev/remote_sql.php?suspected_name=' + man + '&address=' + adu + '&symptoms=' + simp + '&suspected_age=' + agg + '&reported_date=' + date1)
                                #finur = quote(uneurl, safe=':,/,?,=,&,-,_')
                                # finur.replace(" ","%20")
                                

                                suslink = 0
                                cco = 0
                            else:
                                print("Some error. Suspect data entry sequence terminated")
                                suslink = 0
                                cco = 0

                    print("[REDA'S  REPLY] >> " + magret[0])
                    print("\n\n**** Stat ****\n")
                    print("Query was: " + magret[1])
                    print("Intent was: " + magret[2])
                    print("Intent Confidence was: " + magret[3])
                    print(" Action was: " + magret[4])
                    multi.TextToSpeech(replyy)

                    if (pscintentt == "Suspect - yes"):
                        suslink = 1
                        cco = 0
                        print("\n~~~~*********COVID SQL data collection mode has started*********~~~~")

                    count = 0
                except sr.UnknownValueError:
                    count += 1
                    print("Speak something")
                    if count > 3:
                        print("[REDA SLEEPS]")
                        break
                except sr.RequestError as e:
                    print("Could not process because of the reason : {0}".format(e))
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print("Could not process because of the reason : {0}".format(e))


