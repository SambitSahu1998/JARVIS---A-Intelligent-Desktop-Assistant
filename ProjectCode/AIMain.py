import random
import json
import torch
import datetime
from Brain import NeuralNet
from NeuralNetwork import bag_of_words, tokenize

device = torch.device('cude'if torch.cuda.is_available() else 'cpu')
with open("intents.json","r") as json_data:
    intents = json.load(json_data)

FILE = "TrainData.pth"
data=torch.load(FILE)

input_size=data["input_size"]
hidden_size=data["hidden_size"]
output_size=data["output_size"]
all_words=data["all_words"]
tags=data["tags"]
model_state=data["model_state"]


model=NeuralNet(input_size,hidden_size,output_size).to(device)
model.load_state_dict(model_state)
model.eval()

Name="AI BOT"

from Listen import Listen
from Speak import Say
from Task import NonInputExecution,InputExecution

def Main():
    
    sentence = Listen()
    query=sentence
    if sentence == "quit jarvis":
        Say("Alright sir, going offline. It was nice working with you")
        exit()

    sentence=tokenize(sentence)
    X=bag_of_words(sentence,all_words)
    X=X.reshape(1,X.shape[0])
    X=torch.from_numpy(X).to(device)

    output=model(X)

    _ , predicted=torch.max(output,dim=1)

    tag = tags[predicted.item()]

    probs=torch.softmax(output,dim=1)
    prob=probs[0][predicted.item()]

    if prob.item()>0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                reply=random.choice(intent["responses"])
                
                if "time" in reply:
                    NonInputExecution(reply)
    
                elif "date" in reply:
                    NonInputExecution(reply)
                
                elif "day" in reply:
                    NonInputExecution(reply)

                elif "wikipedia" in reply:
                    InputExecution(reply,sentence)

                elif "hide" in reply:
                    InputExecution(reply,sentence)
                
                elif "visible" in reply:
                    InputExecution(reply,sentence)

                elif "ip" in reply:
                    InputExecution(reply,sentence)

                elif "system" in reply:
                    InputExecution(reply,sentence)

                elif "locationc" in reply:
                    InputExecution(reply,sentence)  
                
                elif "swindow" in reply:
                    InputExecution(reply,sentence) 
                    
                elif "news" in reply:
                    InputExecution(reply,sentence) 

                elif "findplace" in reply:
                    InputExecution(reply,query) 

                elif "open" in reply:
                    InputExecution(reply,query)

                elif "video" in reply:
                    InputExecution(reply,query)

                elif "apps" in reply:
                    InputExecution(reply,query)

                elif "tscreenshot" in reply:
                    InputExecution(reply,query)
                
                elif "cscreenshot" in reply:
                    InputExecution(reply,query)

                elif "cnotepad" in reply:
                    InputExecution(reply,query)

                elif "mnotepad" in reply:
                    InputExecution(reply,query)

                elif "weather" in reply:
                    InputExecution(reply,query)

                elif "volup" in reply:
                    InputExecution(reply,query)

                elif "voldn" in reply:
                    InputExecution(reply,query)

                elif "volmt" in reply:
                    InputExecution(reply,query)

                elif "phonecall" in reply:
                    InputExecution(reply,query)

                else:
                    Say(reply)


def Startup():
    Say("Initializing Jarvis")
    Say("Starting all systems applications")
    Say("Installing and checking all drivers")
    Say("Caliberating and examining all the core processors")
    Say("Checking the internet connection")
    Say("Wait a moment sir")
    Say("All drivers are up and running")
    Say("All systems have been activated")
    Say("Now I am online")


def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        Say("Good Morning")
    elif hour>12 and hour<18:
        Say("Good afternoon")
    else:
        Say("Good evening")
    time = datetime.datetime.now().strftime("%H:%M:%S")
    Say(f"Currently it is {time}")
    Say("I am Jarvis. Online and ready sir. Please tell me how may I help you")





#Startup()
#Wish()

while True:
    Main()







