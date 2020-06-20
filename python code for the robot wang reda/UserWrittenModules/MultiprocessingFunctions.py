import os
import dialogflow
from google.api_core.exceptions import InvalidArgument
import speech_recognition as sr
import pyttsx3
import requests
import cv2
from datetime import date

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'Assets/Dialogflow credentials/reda-catqul-dddb616bf22b.json' # it is there in this folder inside the currrent working directory
DIALOGFLOW_PROJECT_ID = 'reda-catqul'#EDITED
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'

def MakeAwareness(text):
    TextToSpeech(text)

def SpeechToText():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("[I AM LISTENING...]")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        recognisedtext = str(r.recognize_google(audio))
        print("[YOU SAID] " + recognisedtext)
        dialogflowresult = DialogflowSocket(recognisedtext)
        print("[I REPLIED] " + dialogflowresult)
        TextToSpeech(dialogflowresult)
    except sr.UnknownValueError:
        print("NO SPEECH HEARD!")
    except sr.RequestError as e:
        print("Could not process because of the reason : {0}".format(e))

def TextToSpeech(text):
    urilocation = r'Assets/Audio Files/speechCommand.mp3'
    engine = pyttsx3.init()  # object creation
    engine.setProperty('rate', 190)  # setting up new voice rate
    voices = engine.getProperty('voices')  # getting details of current voice
    engine.setProperty('voice', voices[1].id)  # changing index, changes voices. 1 for female
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def DialogflowSocket(queryText):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=queryText, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    #print("***PRINT START***")
    #querytext = response.query_result.query_text
    #print("Query text:", response.query_result.query_text)
    #dectintent = response.query_result.intent.display_name
    #print("Detected intent:", response.query_result.intent.display_name)
    #dectintentc = response.query_result.intent_detection_confidence
    #print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    #print("Fulfillment text:", response.query_result.fulfillment_text)
    #print("***PRINT END***")
    the_data = [str(response.query_result.fulfillment_text), str(response.query_result.query_text), str(response.query_result.intent.display_name), str(response.query_result.intent_detection_confidence), str(response.query_result.action) ]
    return the_data


def upload_image_to_server_and_increment_count(frame,file_name):
    imencoded = cv2.imencode(".jpg", frame)[1]
    # To get the current date and the month name
    today = date.today()
    date_and_month_name = today.strftime("%d %B")
    file = {'image': (file_name, imencoded.tostring(), 'image/jpeg', {'Expires': '0'})}
    response = requests.post("http://localhost:5000/api/report_image/", files=file, timeout=5)
    print("[HTTP STATUS] |"+str(response.status_code)+"  |[response] |"+response.text)
    response = requests.get("http://localhost:5000/api/report_count/?Date="+date_and_month_name+"&Count=1", timeout=5)
    print("[HTTP STATUS] |"+str(response.status_code)+"  |[response] |"+response.text)


'''
#if i use gTTS module then we can use this speaklikerobot else, i cannot use this!.
def SpeakLikeRobot(uri):
    freq, bitSize, channels, buffer, volume = 25000, -16, 2, 2500, 1.0
    pygame.mixer.init(freq, bitSize, channels, buffer)
    pygame.mixer.music.set_volume(volume)
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(uri)
    except pygame.error:
        print("file {} not found! ({})".format(uri, pygame.get_error()))
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(300)
'''
