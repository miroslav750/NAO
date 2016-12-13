# -*- coding: utf-8 -*-
# nastavenie kodovania pre diakritiku

# importy modulov
from bottle import run, route, request
from naoqi import ALProxy
import ramena, nohy, drep, biceps, ramena2, tlaknaramena, tlaky, zakopavanie,stranka

# zakladna cesta ktora vrati web stranku
@route('/')
def web():
    return stranka.web

# cesta pre vykonanie cvicenia
@route('/cvic', method='GET')
def cvic():
    # funkcia pre postavenie robota do vzpriamenej polohy
    def stand():
        postureProxy = ALProxy("ALRobotPosture", IP, PORT)
        postureProxy.goToPosture("Stand", 1.0)

    # funkcia pre nastavenie robota do polohy ked lezi
    def lahnni():
        postureProxy = ALProxy("ALRobotPosture", IP, PORT)
        postureProxy.goToPosture("LyingBack", 1.0)

    # funkcia pre nastavenie robota do polohy ked lezi na bruchu
    def lahnni_brucho():
        postureProxy = ALProxy("ALRobotPosture", IP, PORT)
        postureProxy.goToPosture("LyingBelly", 1.0)

    # funkcia pre fotenie, nastaveni sa tu rozlisenie, miesto ulozenia, format a nazov
    def take_photo():
        try:
            photoCaptureProxy = ALProxy("ALPhotoCapture", IP, PORT)
        except Exception, e:
            print "Error when creating ALPhotoCapture proxy:"
            print str(e)
            exit(1)
        photoCaptureProxy.setResolution(2)
        photoCaptureProxy.setPictureFormat("jpg")
        photoCaptureProxy.takePicture("/home/nao/recordings/cameras/", "image")
        print "OK photo taken"

    # pomocne premenne
    cviky = []
    history = "<br>"
    settings = request.query.decode()

    # for cyklus ktorý prejde URL z ktorej ziska PORT,IP,MENO a zoznam zvolenych cvikov
    for item in settings:
        if item == "NAME":
            NAME = str(request.query[item])
        if item == "IP":
            IP = str(request.query[item])
        if item == "PORT":
            PORT = int(request.query[item])
        if item.startswith('cvik'):
            cviky.append(request.query[item])

    # nastavenia pre text to speech
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    tts.setParameter("doubleVoice", 1)
    tts.setParameter("doubleVoiceLevel", 0.5)
    tts.setParameter("doubleVoiceTimeShift", 0.1)
    tts.setParameter("pitchShift", 1.1)

    # for cyklus ktorý vykonáva cvičenie
    for cvik in cviky:
        if cvik == "ramena":
            history += "- ramena <br>"  # ulozi nazov cviku do historie ktora sa zobrazi po cviceni
            stand() # robot do vzpriamenej polohy
            tts.say("and now Shoulders")    # robot povie co ide vykonavat
            motion = ALProxy("ALMotion", IP, PORT)
            for _ in range(3):  # vykonanie cviku 3-krat
                motion.angleInterpolation(ramena.names, ramena.keys, ramena.times, True)
            stand() # po ukonceni ostane robot stat
        if cvik == "nohy":
            history += "- nohy <br>"
            lahnni()
            tts.say("and now legs")
            motion = ALProxy("ALMotion", IP, PORT)
            motion.angleInterpolation(nohy.names, nohy.keys, nohy.times, True)
            stand()
        if cvik == "drep":
            history += "- drepy <br>"
            stand()
            tts.say("and now squats")
            motion = ALProxy("ALMotion", IP, PORT)
            motion.angleInterpolation(drep.names, drep.keys, drep.times, True)
            stand()
        if cvik == "biceps":
            history += "- biceps <br>"
            stand()
            tts.say("and now biceps")
            motion = ALProxy("ALMotion", IP, PORT)
            motion.angleInterpolation(biceps.names, biceps.keys, biceps.times, True)
            stand()
        if cvik == "ramena2":
            history += "- rozpazovanie <br>"
            stand()
            tts.say("and now Shoulders")
            motion = ALProxy("ALMotion", IP, PORT)
            motion.angleInterpolation(ramena2.names, ramena2.keys, ramena2.times, True)
            stand()
        if cvik == "tlaknaramena":
            history += "- Tlaky na ramena <br>"
            stand()
            tts.say("and now shoulders")
            motion = ALProxy("ALMotion", IP, PORT)
            motion.angleInterpolation(tlaknaramena.names, tlaknaramena.keys, tlaknaramena.times, True)
            stand()
        if cvik == "tlaky":
            history += "- Tlaky <br>"
            lahnni()
            tts.say("and now bench press")
            motion = ALProxy("ALMotion", IP, PORT)
            motion.angleInterpolation(tlaky.names, tlaky.keys, tlaky.times, True)
            stand()
        if cvik == "zakopavanie":
            history += "- Zakopavanie <br>"
            lahnni_brucho()
            tts.say("and now Legs")
            motion = ALProxy("ALMotion", IP, PORT)
            motion.angleInterpolation(zakopavanie.names, zakopavanie.keys, zakopavanie.times, True)
            stand()





    # po docviceni robot navrhne vytvorenie selfie a povie ako na to
    tts.say("Now let's take a photo, touch myhead to take picture")
    memProxy = ALProxy("ALMemory", IP, PORT)
    # caka sa na stalecenie hlavy robota a vytvorenie fotky
    while (True):
        if (memProxy.getData("Device/SubDeviceList/Head/Touch/Middle/Sensor/Value")):
            take_photo()
            tts.say("OKAY PHOTO IS TAKEN, bye bye")
            return stranka.result.format(name=NAME, history=history)




run(host='localhost', port=8080, debug=True, reloader=True)
