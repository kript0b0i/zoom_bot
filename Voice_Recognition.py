import speech_recognition as sr
import Webhook

# listener.dynamic_energy_threshold = True
# listener.energy_threshold=40000
# listener.pause_threshold = 0.8
# 40000
# print(sr.Microphone.list_microphone_names())
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

#  KeyWord = ["turn on your camera", "turn on your camera Luis"]
#             text =Voice_Recognition.getAudio()
#             for phrase in KeyWord:
#                 if phrase in text:
#                     print('')
#                     print('Zoom bot: turning your camera on')


"""

If speech_recognition is not working, make sure you  install pyaudio
If you are using Mac I'm not sure if pyaudio is going to work

IF YOU GET AN ERROR INSTALLING THE REQUIREMENTS LET ME KNOW

#WINDOWS ONLY
pip install pipwin
pipwin install pyaudio

"""
#return audio as text
#use microphone
def getAudio():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source, duration=0.2)
        print('listening...')
        audio = listener.listen(source, phrase_time_limit=5)
        said=''
        try:
            said = listener.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: "+str((e)))
    return said.lower()

    
#test
def answerAttendace():
    listener = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source, duration=0.2)
                print('waiting for professor calling your name...')
                voice = listener.listen(source, phrase_time_limit=5)
                Gettext = listener.recognize_google(voice)#change language  language='es-US'
                Gettext = Gettext.lower()
                print("converting voice to text: " + Gettext)
                if (Gettext.find("Luis") != -1 or Gettext.find("lewis") != -1 or Gettext.find("louis") != -1 or Gettext.find("Mendoza") != -1):
                    Webhook.Attendance(Gettext)
                    break
        except:
            print('no sound detected...trying again')

        