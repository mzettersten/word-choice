#!/usr/bin/env python
from psychopy import core, visual, prefs, event
import random, sys
from useful_functions import *
from generateTrials import *
import webbrowser as web
import socket
import datetime
from baseDefsPsychoPy import *
from stimPresPsychoPy import *
#import pyaudio
import wave
#workaround for dropdown box
#import pyglet
#pyglet.options['shadow_window'] = False


class Exp:
	def __init__(self):
	           
		self.surveyURL = 'https://uwmadison.co1.qualtrics.com/SE/?SID=SV_bvapa6sSEHDmdsF'
		self.get_runtime_vars()
		
		if self.runTimeVars['windowSize']=="test":
		    self.win = visual.Window([800,800],color='grey', units='pix',screen=1)
		else:
		    self.win = visual.Window(fullscr=True,color='grey', units='pix')
		
		self.myMouse = event.Mouse()
		self.myMouse.setVisible(0)
		self.pics =  loadFiles('stimuli/pics','.png','image', win=self.win)
		self.sounds =  loadFiles('stimuli/sounds','.wav','sound', win=self.win)
		#self.background = self.pics['grass_background'][0]
		self.background = newRect(self.win, size=[1920,1200],pos=[0,0], color="lightgrey")
		self.background.size=[1920,1200]
		
		self.clockFrame = visual.Circle(win=self.win,radius=150, lineColor="black", lineWidth=5, fillColor="white")
		self.clockHand = visual.ShapeStim(win=self.win,vertices=((-142, 0), (0, 10),(0,-10)),lineColor="black",lineWidth=2,fillColor="black")
		self.clockCenter = visual.Circle(win=self.win,radius=10, lineColor="black", lineWidth=5, fillColor="black")
		#self.arrow = visual.ShapeStim(self.experiment.win,lineWidth=1.0, lineColor="black",  fillColor="black", vertices=((-150, 0), (-125, 20), (-125, -20)))
		
		#for text box
		self.textBoxOuter=newRect(self.win, size=[210,60],pos=(0,-300), color="black")
                self.textBoxInner=newRect(self.win, size=[200,50],pos=(0,-300), color="white")
                
                self.instructions = """
		Thank you for your participation. In order to complete today's task, you're going to play a game. You've been asked to be a guide for a squad of Elves looking to find buried treasure. Their compass navigator has gone missing and there's not much time before winter makes the hunt impossible. In exchange for your navigating, they'll give you a cut of their prize.
		
		Here's the situation. The worker elves only know Elvish. It's your job to learn to read the compass as quickly and accurately as possible, and use what you know to guide the Elves to treasure. First you'll learn how to give directions. Just as soon as you pass basic navigating it's off to hunt for treasure. Good luck!                
                """
		self.nvlearnInstructions = "The Elves use 8 principal directions to navigate. First, to get you familiar with the directions of the compass and to see whether you can quickly judge the main compass directions, we will do a short memory test. On each trial, you will see a direction flash briefly on the screen. Your job is then to move the hand of the compass to the direction you just saw, by scrolling the wheel on top of the mouse. Try to respond as quickly and as accurately as you can. The compass face will flash green if you were correct and red if you were incorrect."
		self.exposureInstructions = "The Elves use 8 principal directions to navigate. You will use those directions to help them find the treasure. You're about to see the names for each direction, and practice giving directions by typing in the name of the direction."
		self.learningInstructions =  "Let's check in to see how much Elvish you've learned. You will see a direction and two potential words for that direction. Type the word that you think is correct. We'll go back to practicing Elvish if you haven't learned all the words yet."
                
                self.startPrompt=visual.TextStim(self.win,text="Press space bar to begin the hunt.", wrapWidth=1200, height=30,pos=[0,-200],color='black',bold=True)
                self.textPrompt=visual.TextStim(self.win,text="Quick, which direction is the treasure?", wrapWidth=1200, height=30,pos=[0,-200],color='black',bold=True)
                self.textPrompt2=visual.TextStim(self.win,text="Press enter once you have typed the direction in the text box.", wrapWidth=1200, height=30,pos=[0,-240],color='black',bold=True)
                self.audioPrompt=visual.TextStim(self.win, text="Quick, which direction is the treasure? Press the space bar when finished.", wrapWidth=1200, height=30,pos=[0,-200],color='black',bold=True)
                self.audioPromptEnd=visual.TextStim(self.win, text="Finished recording.", wrapWidth=1200, height=30,pos=[0,-200],color='black',bold=True)
                self.audioPromptFeedback=visual.TextStim(self.win, text="", wrapWidth=1200, height=30,pos=[0,-200],color='black',bold=True)
                
                self.learnPrompt = visual.TextStim(self.win,text="", wrapWidth=1200, height=30,pos=[0,-200],color='black',bold=True)
                self.learnResponseInfo = visual.TextStim(self.win,text="Type in the name for the direction and press enter.", wrapWidth=1200, height=30,pos=[0,-240],color='black',bold=True)
                self.labelFeedbackText = visual.TextStim(self.win,text="", wrapWidth=1200, height=30,pos=[0,-350],color='black',bold=True)
                
                self.textPromptAngleMem=visual.TextStim(self.win,text="Remember the angle orientation.\n Left-click on the mouse to see the next angle.", wrapWidth=1200, height=30,pos=[0,-200],color='black',bold=True)
                self.textPromptAngleAdjust=visual.TextStim(self.win,text="Adjust the angle to the first orientation you just saw using the mouse wheel.", wrapWidth=1200, height=30,pos=[0,-200],color='black',bold=True)
                self.textPromptAngleAdjust2=visual.TextStim(self.win,text="Left-click on the mouse when finished.", wrapWidth=1200, height=30,pos=[0,-240],color='black',bold=True)
                
                self.pos={'left': [-200,-300], 'right': [200,-300]}
                self.learningPrompt = visual.TextStim(self.win,text="What is the correct name for this direction?", wrapWidth=1200, height=30,pos=[0,-200],color='black',bold=True)
                self.learningResponseInfo = visual.TextStim(self.win,text="Use the left and right arrow keys to respond.", wrapWidth=1200, height=30,pos=[0,-240],color='black',bold=True)
                self.learningTextLeft = visual.TextStim(self.win, text="", wrapWidth=1200, height=40,pos = self.pos["left"],color='black',bold=True)
                self.learningTextRight = visual.TextStim(self.win, text="", wrapWidth=1200, height=40,pos = self.pos["right"],color='black',bold=True)
                self.learningBoxOuterLeft=newRect(self.win, size=[210,60],pos=self.pos['left'], color="black")
                self.learningBoxInnerLeft=newRect(self.win, size=[200,50],pos=self.pos['left'], color="white")
                self.learningBoxOuterRight=newRect(self.win, size=[210,60],pos=self.pos['right'], color="black")
                self.learningBoxInnerRight=newRect(self.win, size=[200,50],pos=self.pos['right'], color="white")
                
                self.recordPic = visual.ImageStim(self.win,'stimuli/pics/record.png', pos=[0,-300], size=[200,200])
                self.stopPic = visual.ImageStim(self.win,'stimuli/pics/stop.png', pos=[0,-300])
                
                self.treasurePic = visual.ImageStim(self.win, 'stimuli/pics/treasure.png',pos=[340,300],size=[50,50])
                self.treasurePicFeedback = visual.ImageStim(self.win, 'stimuli/pics/treasure.png',pos=[380,0],size=[50,50])
                
                self.elfFeedback = visual.ImageStim(self.win, 'stimuli/pics/elf.png',pos=[340,125],size=[90,180])
                
                self.score=visual.TextStim(self.win,text="0", wrapWidth=1200, height=60,pos=[300,300],alignHoriz='right',color='red',bold=True)
                self.feedbackText = visual.TextStim(self.win,text="+0", wrapWidth=1200, height=60,pos=[340,0],alignHoriz='right',color='red',bold=True)
                self.feedback2Text = visual.TextStim(self.win,text="", wrapWidth=400, height=30,pos=[200,-100],alignHoriz='left',color='black',bold=True)
                self.feedbackLabel = visual.TextStim(self.win,text="", wrapWidth=1200, height=30,pos=[0,-200],color='black',bold=True)
                self.incorrLabelFeedback = visual.TextStim(self.win,text="That is not a valid word.", wrapWidth=1200, height=30,pos=[0,-240],color='black',bold=True)
                
                #self.labelList = ["gled","yeen","peka","pim","dak","grah","sarp","noobda"]
                
                self.textBoxEntry = visual.TextStim(self.win, text='', wrapWidth=150,height = 30, bold=True, color="black",alignHoriz="left",alignVert="top",pos=(-50,-285))
                
                self.learningResponses = ['left','right']
                
                self.ITI = 0.5
                self.learnTimeoutTime = 7.0
                self.timeoutTime = 5.0
                
                self.postStartDelay=.5
                self.postEndDelay=.25
                self.audioTimeoutTime = 10.0
                self.audioEndTime = 1.0
                
                self.angleViewTime = 0.5
                
                self.namingScore = 10
                self.numberOfNames = 8
                self.maxNameBlocks = 11
                
                self.fixedLearnLen="yes"
                self.numLearnBlocks = 5
                self.numNvlearnBlocks = 5
                
                self.feedbackTime = 4.0
                self.feedback2Time = 5.0
                self.numLongFeedbackTrials = 5
                self.learnFeedbackTime = 1.0
                self.angleAdjustFeedbackTime = 1.0
                
                self.numFeedbackBlocks=8
                
                self.breakAfter = 40

		
	def get_runtime_vars(self):
		while True:
			runTimeVarsOrder = ['subjCode','seed', 'angleAssign','labelAssign','condition','room','date_time', 'block','windowSize']
			self.runTimeVars = getRunTimeVars(
												{'subjCode':'clock_101', 'seed':10, \
												'condition': 'test', \
												'angleAssign': 1, \
												'labelAssign': 1, \
												#'angleAssign': [1,2], \
												'room': socket.gethostname().upper(),\
												'date_time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),\
												'block': 0,\
												'windowSize': "full"},\
												runTimeVarsOrder,'wc2_4_v1')
			self.outputFile = openOutputFile('data/'+self.runTimeVars['subjCode'],'wc2_4_v1')
			if self.outputFile:
				break
		
		try:
			print 'generating trials...'
			self.labelList=generateTrials(self.runTimeVars,runTimeVarsOrder)
			print self.labelList
		except:
			sys.exit('Something went wrong with trial generation')

		(self.header,self.trialInfo) = importTrialsWithHeader('trials/'+self.runTimeVars['subjCode']+'_trials.txt')
		#(self.header,self.trialInfo) = importTrialsWithHeader('testTrialListDemo.csv',separator=",")
		#(self.learnHeader,self.learnTrialInfo) = importTrialsWithHeader('learnTrialList_demo.csv',separator=",")
		self.trialInfo = evaluateLists(self.trialInfo)
		
		#group into different learning trial types
		self.nvlearnInfo=[]
		self.nameInfo=[]
		self.learnInfo=[]
		self.testInfo=[]
		self.finalNameInfo=[]
		for curTrial in self.trialInfo:
		    if curTrial['trialType']=="nonvLearn":
		        self.nvlearnInfo.append(curTrial)
		    elif curTrial['trialType']=="name":
		        self.nameInfo.append(curTrial)
		    elif curTrial['trialType']=="pairLearn": 
		        self.learnInfo.append(curTrial)
		    elif curTrial['trialType']=="test": 
		        self.testInfo.append(curTrial)
		    elif curTrial['trialType']=="finalName": 
		        self.finalNameInfo.append(curTrial)
		        
		
		#self.learnTrialInfo = evaluateLists(self.learnTrialInfo)
		printHeader(self.header+['trialType','trialNumber','response','label','isRight', 'rt', 'score','numWheelTurnsUp','numWheelTurnsDown'])
		self.surveyURL += '&subjCode=%s' % (self.runTimeVars['subjCode'])
        
        def runLearningTrial2AFC(self,trialType,trialNumber,curTrial,totalScore):
            
		curTrial['header']=self.header
		
		#reset clock hand
		self.clockHand.ori = int(curTrial['angle'])
		
		#set label choices
		self.learningTextLeft.text = curTrial['left']
		self.learningTextRight.text = curTrial['right']
		
		#draw clock & options
		setAndPresentStimulus(self.win,[self.background,self.clockFrame,self.clockCenter,self.clockHand,self.learningBoxOuterLeft,self.learningBoxInnerLeft,self.learningBoxOuterRight,self.learningBoxInnerRight,self.learningTextLeft,self.learningTextRight,self.learningPrompt,self.learningResponseInfo])
		
		#get keyboard response
		[resp,RT] = getKeyboardResponse(self.learningResponses,duration=0)   
		RT = RT *1000
		label = curTrial[resp]
		
		#check if correct
		isRight = int(curTrial['target'] == label)
		
                    
		#write runtime and indep variables to 
		responses=[curTrial[_] for _ in curTrial['header']]

		#write dep variables
		responses.extend(
			[trialType,
			trialNumber,
			resp,
			label,
			isRight,
			RT,totalScore])
		writeToFile(self.outputFile,responses,separator='\t', sync=True,writeNewLine=True)
		
		#feedback
		if isRight ==1 :
		    feedbackColor = "green"
		    totalScore+=1
		else:
		    feedbackColor = "red"
		    
		if resp == "left":
		    self.learningBoxInnerLeft.color = feedbackColor
		else:
		    self.learningBoxInnerRight.color = feedbackColor
		
		#draw clock with feedback on response
		setAndPresentStimulus(self.win,[self.background,self.clockFrame,self.clockCenter,self.clockHand,self.learningBoxOuterLeft,self.learningBoxInnerLeft,self.learningBoxOuterRight,self.learningBoxInnerRight,self.learningTextLeft,self.learningTextRight,self.learningPrompt,self.learningResponseInfo])
		core.wait(self.learnFeedbackTime)  
		
		#flip screen
		setAndPresentStimulus(self.win,[self.background,self.clockFrame,self.clockCenter])
		core.wait(self.ITI)
		self.learningBoxInnerLeft.color = "white"
		self.learningBoxInnerRight.color = "white"
		
		return totalScore
	
	def runLearningTrial(self,trialType,trialNumber,curTrial,totalScore, labelFeedback = 0, feedback = True):
            
		curTrial['header']=self.header
		
		#reset clock hand
		self.clockHand.ori = int(curTrial['angle'])
		
		#set label choices
		if trialType == "name" and labelFeedback ==0:
		  self.learnPrompt.text = 'This direction is called ' + curTrial['target'] 
		elif trialType == "name" and labelFeedback ==1:
		  self.learnPrompt.text = 'What is this direction called?'  
		elif trialType == "pairLearn":
		  self.learnPrompt.text = curTrial['left'] + " or " + curTrial['right'] + '?'
		elif trialType == "finalName":
		  self.learnPrompt.text = 'What is this direction called?'  
		
		#base stimulus array
		baseStims = [self.background,self.clockFrame,self.clockCenter,self.clockHand,self.learnPrompt,self.learnResponseInfo]
		
		#enter text response
		timer = core.Clock()
		label = self.enterText(baseStims,0)
		RT = timer.getTime()*1000
		
		#check if correct
		isRight = int(curTrial['target'] == label)
		
                    
		#write runtime and indep variables to 
		responses=[curTrial[_] for _ in curTrial['header']]
		
		resp="NA"

		#write dep variables
		responses.extend(
			[trialType,
			trialNumber,
			resp,
			label,
			isRight,
			RT,totalScore])
		writeToFile(self.outputFile,responses,separator='\t', sync=True,writeNewLine=True)
		
		if feedback:
		  #feedback
		  if isRight ==1 :
		      feedbackColor = "green"
		      totalScore+=1
		      feedbackSound = "bleep"
		  else:
		      feedbackColor = "red"
		      feedbackSound = "buzz"
		      
		  self.textBoxInner.color = feedbackColor
		  self.textBoxEntry.text = label
		
		  #draw clock with feedback on response
		  stimArray = [self.background,self.clockFrame,self.clockCenter,self.clockHand,self.learnPrompt,self.learnResponseInfo,self.textBoxOuter,self.textBoxInner,self.textBoxEntry]
		  if labelFeedback == 1 and isRight ==0:
		      self.labelFeedbackText.text="The correct label is " + curTrial['target']
		      stimArray = stimArray + [self.labelFeedbackText]
		  setAndPresentStimulus(self.win,stimArray)
		
		  #play feedback sound
		  playAndWait(self.sounds[feedbackSound])
		  core.wait(self.learnFeedbackTime)  
		
		#flip screen
		setAndPresentStimulus(self.win,[self.background,self.clockFrame,self.clockCenter])
		core.wait(self.ITI)
		self.textBoxInner.color = "white"
		self.textBoxEntry.text = ""
		
		return totalScore
	
	
	def angleAdjustTrial(self,trialType,trialNumber,curTrial,snapLag=1,snapDist=45,feedback=True):
	    		
	    	curTrial['header']=self.header
		
		#reset clock hand
		self.clockHand.ori = int(curTrial['angle'])
		
		#setAndPresentStimulus(self.win,[self.background,self.clockFrame,self.clockCenter,self.textPromptAngleMem])
                setAndPresentStimulus(self.win,[self.background,self.clockFrame,self.clockCenter])
		
		#while self.myMouse.getPressed()[0]==0:
		#    core.wait(0.01)
		
		#draw clock & options
		setAndPresentStimulus(self.win,[self.background,self.clockFrame,self.clockCenter,self.clockHand])
                core.wait(self.angleViewTime)
                
                #flip screen
		setAndPresentStimulus(self.win,[self.background,self.clockFrame,self.clockCenter])
		
		#reset clockHand
		self.clockHand.ori = int(curTrial['right'])
		core.wait(0.5)
		setAndPresentStimulus(self.win,[self.background,self.clockFrame,self.clockCenter,self.clockHand,self.textPromptAngleAdjust,self.textPromptAngleAdjust2])
                
		
		numWheelTurnsDown=numWheelTurnsUp=0
		responded=False
		startingOri=int(curTrial['right'])
		oriCounter = 0
	
		timer = core.Clock()
		while not responded:
			while self.myMouse.getPressed()[0]==0:
			     
			    
				setAndPresentStimulus(self.win,[self.background,self.clockFrame,self.clockCenter,self.clockHand,self.textPromptAngleAdjust,self.textPromptAngleAdjust2])
				wheelRel = self.myMouse.getWheelRel()[1]
				
				if wheelRel>0.0:
				    numWheelTurnsDown+=1
				    oriCounter-=1
				    curOri=(startingOri+snapDist*floor(oriCounter/snapLag)) % 360
				    self.clockHand.ori = curOri
				elif wheelRel<0.0:
				    numWheelTurnsUp+=1
				    oriCounter+=1
				    curOri=(startingOri+snapDist*floor(oriCounter/snapLag)) % 360
				    self.clockHand.ori = curOri

				if self.myMouse.getPressed()[0]==1 and (numWheelTurnsUp>0 or numWheelTurnsDown>0):
					RT = timer.getTime()*1000
					responded=True
					
		#write runtime and indep variables to 
		responses=[curTrial[_] for _ in curTrial['header']]
		
		isRight=0
		if curOri == int(curTrial['angle']):
		    isRight=1
		    
		distance=min(abs(curOri-int(curTrial['angle'])), 360-abs(curOri-int(curTrial['angle'])))
	
		#write dep variables
		responses.extend(
			[trialType,
			trialNumber,
			curOri,
			'NA',
			isRight,
			RT,distance,numWheelTurnsUp,numWheelTurnsDown])
			
		writeToFile(self.outputFile,responses,separator='\t', sync=True,writeNewLine=True)
		
		if feedback:
		  #feedback
		  if isRight ==1 :
		      feedbackColor = "green"
		      feedbackSound = "bleep"
		  else:
		      feedbackColor = "red"
		      feedbackSound = "buzz"
		      
		  self.clockFrame.fillColor = feedbackColor
		
		  #draw clock with feedback on response
		  setAndPresentStimulus(self.win,[self.background,self.clockFrame,self.clockCenter,self.clockHand])
		  
		  #play feedback sound
		  playAndWait(self.sounds[feedbackSound])

		  core.wait(self.angleAdjustFeedbackTime) 
		  
		  #reset color
		  self.clockFrame.fillColor = "white"
		
		
		setAndPresentStimulus(self.win,[self.background,self.clockFrame,self.clockCenter])
		core.wait(self.ITI)


	def runTestTrial(self,trialType,trialNumber,curTrial,updateScore,updateEveryXTrials,totalScore,runningScore, feedback,feedback2="none"):
	        
	        setAndPresentStimulus(self.win,[self.background,self.score,self.treasurePic,self.clockFrame,self.clockCenter,self.startPrompt])
	       
	        event.waitKeys(keyList=['space'])
	       
		curTrial['header']=self.header
		
		#reset clock hand
		self.clockHand.ori = int(curTrial['angle'])
		
		#base stimulus array
		baseStims = [self.background,self.score,self.treasurePic,self.clockFrame,self.clockCenter,self.clockHand]
		
		promptStims = baseStims+[self.textPrompt, self.textPrompt2]
		
		#draw clock
		setAndPresentStimulus(self.win,promptStims)
		
		if trialType == "test":
		    #responded=False
		    timer = core.Clock()
		    label = self.enterText(promptStims,1,self.timeoutTime)
		    RT = timer.getTime()*1000
		elif trialType == "name":
		    timer = core.Clock()
		    label = self.enterText(promptStims,1,self.learnTimeoutTime)
		    RT = timer.getTime()*1000
		    
		#while not responded:
		#    if self.myMouse.getPressed()[0]==1 and (numWheelTurnsUp>0 or numWheelTurnsDown>0):
		#			RT = timer.getTime()*1000
		#			responded=True
                if trialType == "recordName":
                    RT = self.recordIt(self.runTimeVars['subjCode']+"_"+str(trialNumber)+"_"+curTrial['label'],baseStims,chunk=1024)
                    label = "NA"
                    core.wait(self.audioEndTime)
                    
                isRight='NA'
                if trialType == "name":
                    isRight=0
                    if label == curTrial['target']:
                        isRight = 1
                    
                curScore = 0
                if trialType == "name":
                    if label == curTrial['target']:
                        curScore = self.namingScore
                if trialType == "test":   
                    if label in self.labelList:
                        curScore = int(curTrial[label])
                curScore = int(round(curScore * (1 + (self.timeoutTime * 1000 - RT)/ (self.timeoutTime*1000)),0))
                totalScore += curScore
                runningScore += curScore
                    
                    
                    
		#write runtime and indep variables
		responses=[curTrial[_] for _ in curTrial['header']]
		
		resp = 'NA'
		
		#write dep variables
		responses.extend(
			[trialType,
			trialNumber,
			resp,
			label,
			isRight,
			RT,curScore])
		writeToFile(self.outputFile,responses,separator='\t', sync=True,writeNewLine=True)
		
		#feedback
		if feedback=="yes":
		    #update feedback text
		    self.feedbackText.text="+" + str(curScore)
		    self.feedbackLabel.text = "You entered: " + label
		    if not (label in self.labelList):
		        setAndPresentStimulus(self.win,baseStims+[self.feedbackText,self.feedbackLabel,self.incorrLabelFeedback,self.treasurePicFeedback,self.elfFeedback])
		    else:
		        setAndPresentStimulus(self.win,baseStims+[self.feedbackText,self.feedbackLabel,self.treasurePicFeedback,self.elfFeedback])
		    core.wait(self.feedbackTime)
		    
		elif feedback=="partial":
		    self.feedbackLabel.text = "You entered: " + label
		    if not (label in self.labelList):
		        setAndPresentStimulus(self.win,baseStims+[self.feedbackLabel,self.incorrLabelFeedback])
		    else:
		        setAndPresentStimulus(self.win,baseStims+[self.feedbackLabel])
		    core.wait(self.feedbackTime)
		    
		if feedback2=="cumulative":
		    #update feedback text
		    self.feedbackText.text="+" + str(runningScore)
		    self.feedback2Text.text="You helped the elves collect " + str(runningScore) + " treasure coins on your last " + str(self.numFeedbackBlocks)+ " hunts combined."
		    setAndPresentStimulus(self.win,baseStims+[self.feedbackText,self.feedback2Text,self.treasurePicFeedback,self.elfFeedback])
		    core.wait(self.feedback2Time)
		    
		
		endTrialStims = [self.background, self.clockFrame,self.clockCenter,self.score,self.treasurePic]
		self.textBoxEntry.text = ""
		
		if int(updateScore)==1 and trialNumber % updateEveryXTrials==0:
		    self.score.text = str(totalScore)
		
		setAndPresentStimulus(self.win,endTrialStims)
		core.wait(self.ITI)
		
		return [curScore,totalScore,runningScore]

	def showInstructions(self,instructions):
		visual.TextStim(win=self.win,text=instructions,color="white",height=30,wrapWidth=1200).draw()
		self.win.flip()
		event.waitKeys(keyList=['z'])

	def showText(self, text):
		visual.TextStim(win=self.win,text=text,color="white",height=30).draw()
		self.win.flip()
		event.waitKeys(keyList=['enter','return'])
		
	def enterText(self,stimulusArray,timeoutTrue,timeoutTime=0):
	    
	    #text
	    text = self.textBoxEntry
        
	    #present text box
            setAndPresentStimulus(self.win,stimulusArray+[self.textBoxOuter,self.textBoxInner])

            chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','1','2','3','4','5','6','7','8','9']
            
            # Loop until return is pressed
            endTrial = False
            
            timer = core.Clock()
            startTime = timer.getTime()

            while not endTrial:
                #check timeout time
                if timeoutTrue==1:
                    if timer.getTime()-startTime>timeoutTime:
                        endTrial=True
                        break
                        print 'timeout'
                        
                #get responses since last clear
                keyResponses = event.getKeys()
                #if keyResponses != []:
                #   print keyResponses
                
                for keyResponse in keyResponses:
                    #if keyResponses != []:
                    #    print keyResponse[0]
                    if keyResponse:
                        #print keyResponse
                        if keyResponse == 'comma':
                            text.setText(text.text + ',')
                         
                        if keyResponse == 'period':
                            text.setText(text.text + '.')
                        
                        #  If backspace, delete last character
                        if keyResponse == 'backspace':
                            text.setText(text.text[:-1])
                        
                        # If return, end trial
                        elif keyResponse == 'return':
                            endTrial = True
                        
                        # Insert space
                        elif keyResponse == 'space':
                            text.setText(text.text + ' ')

                        # Else if a letter, append to text:
                        elif keyResponse in chars:
                            text.setText(text.text + keyResponse[0])

                    # Display updated text
                    setAndPresentStimulus(self.win,stimulusArray+[self.textBoxOuter,self.textBoxInner,text])
                
                #print text.text
                # If "quit" is entered into the text field, exits the experiment 
                if text.text == "quit":
                        self.win.close()
                        core.quit()

                #event.clearEvents()
            
            return text.text
            
        def getFileReady(self,name):
	   p = pyaudio.PyAudio()
	   stream = p.open(format = pyaudio.paInt16,
		channels = 1,
		#rate = 16000,
		rate = 44100,
		input = True, 
		frames_per_buffer = 1024)
	   wf = wave.open('sounds/'+name+'.wav', 'wb')
	   wf.setnchannels(1)
	   wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
	   #wf.setframerate(16000)
	   wf.setframerate(44100)
	   return (p,stream,wf)
	   
	def recordIt(self,whatToRecord,stimulusArray,chunk=1024):
	    
	    soundStream = []
	    recordingTimer = core.Clock()
	    #event.waitKeys(keyList=['space']) #wait for spacebar, then start recording 
	    print 'starting to record'
	    (p,stream,wf)=self.getFileReady(whatToRecord)
	    print 'file ready'
	    recordingTimer.reset()
	    alreadyDrawn=responded=False
	    
	    setAndPresentStimulus(self.win,stimulusArray+[self.audioPrompt])

	    
	    while True: #recording
	
		if not alreadyDrawn and recordingTimer.getTime()>self.postStartDelay:
		    
			setAndPresentStimulus(self.win,stimulusArray+[self.audioPrompt,self.recordPic])

			alreadyDrawn=True

		data = stream.read(chunk)
		soundStream.append(data)
		if event.getKeys(keyList=['space']):
		    RT = recordingTimer.getTime()*1000
		    recordingTimer.reset()
		    responded=True
		    print 'spacebar pressed'
		elif self.audioTimeoutTime>0 and recordingTimer.getTime()>self.audioTimeoutTime:
		    responded=True
		    RT = recordingTimer.getTime()*1000
		    recordingTimer.reset()
		
		if responded and recordingTimer.getTime()>self.postEndDelay: #stop recording postEndDelay after spacebar press or timeout
                        print 'terminating recording'
			stream.close()
			p.terminate()
			setAndPresentStimulus(self.win,stimulusArray+[self.audioPromptEnd,self.stopPic])
			break
	    # write data to WAVE file
	    print 'saving data'
	    data = ''.join(soundStream)
	    wf.writeframes(data)
	    wf.close()

	    setAndPresentStimulus(self.win,stimulusArray+[self.audioPromptEnd,self.stopPic])
	       
	    return RT
	    
        def shuffleBlock(self,trialList, seed, numShuffles=10):
            random.seed(int(seed))
            for i in range(numShuffles):
                random.shuffle(trialList)
            return trialList

#non-verbal trials block
def nvlearn_trials_block(exp):
    
    exp.showText(exp.nvlearnInstructions+"\n\n"+"Press enter to proceed.")
    nvlearnTrialCounter = 0
    nvlearnBlock=0
    while nvlearnBlock < exp.numNvlearnBlocks:
        for curTrial in exp.nvlearnInfo:
            nvlearnTrialCounter += 1
            exp.angleAdjustTrial(curTrial['trialType'], nvlearnTrialCounter, curTrial)
        nvlearnBlock+=1
        exp.shuffleBlock(exp.nvlearnInfo, exp.runTimeVars['seed'])
    return nvlearnTrialCounter

#naming trials block


def naming_trials_block(exp):
    
    exp.showText(exp.exposureInstructions+"\n\n"+"Press enter to proceed.")
    nameTrialCounter = 0
    for curTrial in exp.nameInfo:
        learnScore=0
        while learnScore == 0:
            nameTrialCounter += 1
            learnScore = exp.runLearningTrial(curTrial['trialType'], nameTrialCounter, curTrial,learnScore)
    return nameTrialCounter
    
#learning trials
def learning_trials_block(exp):
	       
	exp.showText(exp.learningInstructions+"\n\n"+"Press enter to proceed.")
	
	#complete learning and naming trials until participants succeed at all 8 names in the test run.
	learnNameLoop = True
	totalLearnScore=0
	learnTrialCounter = 0
	while learnNameLoop:
	   #learning trials
	   repeat = True
	   learnScore = 0
	   while repeat:
	       for curTrial in exp.learnInfo:
	           learnTrialCounter+=1
	           #learnScore = exp.runLearningTrial2AFC(curTrial['trialType'], learnTrialCounter, curTrial,learnScore)
	           learnScore = exp.runLearningTrial(curTrial['trialType'],learnTrialCounter, curTrial,learnScore)
	           print learnTrialCounter
	       print learnScore
	       #shuffle learning trials
	       exp.shuffleBlock(exp.learnInfo, exp.runTimeVars['seed'])
	       if learnScore > 15:
	           repeat = False
	           break
	       else:
	           exp.showText("You got " + str(learnScore) + " out of 20 trials correct. Let's see if you can do better on the next try. Press enter to continue.")
	           
	       learnScore = 0
	        
	        
	   #naming trial test run block
	   exp.showText("Time for a test hunt with a group of elves to see how you're doing. Type the right direction as quick as you can. The faster your directions, the more points you will score. If you do well enough, you will go off on a real hunt. If it looks like you need more practice, we'll go back.\n\nPress enter to proceed")	
	
	   #naming trials
	   #shuffle naming trials
	   nameTrialCounter = 0
	   exp.shuffleBlock(trialList=exp.nameInfo, seed=int(exp.runTimeVars['seed']))
	   learnCounter = 0
	   for curTrial in exp.nameInfo:
	       nameTrialCounter += 1
	       [curLearnScore, totalLearnScore,totalLearnScore] = exp.runTestTrial(curTrial['trialType'], nameTrialCounter, curTrial,1,1, totalLearnScore,totalLearnScore, "yes")
	       if curLearnScore > 0:
	           learnCounter+=1
	   if learnCounter >= exp.numberOfNames or nameTrialCounter>= (exp.numberOfNames*exp.maxNameBlocks):
	       print "finished"
	       learnNameLoop = False
	       break
	   else:
	       print "repeat"
	       exp.showText("You got " + str(learnCounter) + " out of 8 names correct. Looks like you need a bit more practice before you can go off on a real treasure hunt. Press enter to continue.")
	       learnCounter = 0

	return learnCounter, totalLearnScore  

def learning_trials_block_fixed(exp):
	       
	exp.showText(exp.learningInstructions+"\n\n"+"Press enter to proceed.")
	
	#complete learning and naming trials 
	totalLearnScore=0
	learnTrialCounter = 0
	learnBlock=0
	while learnBlock < exp.numLearnBlocks:
	   #learning trials
	   learnScore = 0
	   for curTrial in exp.learnInfo:
	       learnTrialCounter+=1
	       exp.runLearningTrial(curTrial['trialType'],learnTrialCounter, curTrial,learnScore)
	       print learnTrialCounter
	   #shuffle learning trials
	   exp.shuffleBlock(exp.learnInfo, exp.runTimeVars['seed'])
	        
	        
	   #naming trial test run block
	   exp.showText("Time for a test hunt with a group of elves to see how you're doing. Type the right direction as quick as you can. The faster your directions, the more points you will score. If you do well enough, you will go off on a real hunt. If it looks like you need more practice, we'll go back.\n\nPress enter to proceed")	
	
	   #naming trials
	   #shuffle naming trials
	   nameTrialCounter = 0
	   exp.shuffleBlock(trialList=exp.nameInfo, seed=int(exp.runTimeVars['seed']))
	   learnCounter = 0
	   for curTrial in exp.nameInfo:
	       nameTrialCounter += 1
	       [curLearnScore, totalLearnScore,totalLearnScore] = exp.runTestTrial(curTrial['trialType'], nameTrialCounter, curTrial,1,1, totalLearnScore,totalLearnScore, "yes")
	       if curLearnScore > 0:
	           learnCounter+=1
	   
	   learnBlock+=1
	   if learnBlock < exp.numLearnBlocks:
	       exp.showText("Good job. You got " + str(learnCounter) + " out of 8 names correct. Let's get a bit more practice before you can go off on a real treasure hunt. Press enter to continue.")

	return learnCounter, totalLearnScore  



#testing trials block

def testing_trials_block(exp, learnCounter = 8, totalLearnScore = 0):
	#complete learning phase and proceed to testing trials
	exp.showText("You got " + str(learnCounter) + " out of 8 names correct. Great job! You are ready to go off on a real treasure hunt. Unlike practice hunts, treasures can be anywhere. Every " + str(exp.numFeedbackBlocks)+ " hunts, the elves will let you know how much treasure you helped collect. Just remember the basics, trust your compass and provide guidance as quickly and accurately as possible. Good luck! Press enter to continue.")
	trialCounter=0
	totalScore = totalLearnScore
	runningScore=0
	for curTrial in exp.testInfo:
	    trialCounter+=1
	    if trialCounter > exp.numLongFeedbackTrials:
	        exp.feedbackTime = 2.0
	    #feedback every numFeedbackBlocks number of trials
	    if trialCounter % exp.numFeedbackBlocks==0:
	        #exp.showText("Great job! You helped the elves collect " + str(runningScore) + " treasure coins on your last " + str(exp.numFeedbackBlocks)+ " hunts combined. You've helped the elves collect " + str(totalScore) + " treasure coins overall. Press enter to continue.")
	        [curScore, totalScore,runningScore] = exp.runTestTrial(curTrial['trialType'], trialCounter, curTrial,curTrial['updateScore'],exp.numFeedbackBlocks,totalScore,runningScore, feedback = curTrial["feedback"],feedback2="cumulative")
	        runningScore=0
	    else:
	        [curScore, totalScore,runningScore] = exp.runTestTrial(curTrial['trialType'], trialCounter, curTrial,curTrial['updateScore'],exp.numFeedbackBlocks,totalScore,runningScore, feedback = curTrial["feedback"])
	    
	        
	    if trialCounter == exp.breakAfter:
	        exp.showText("Take a short break. Please press enter when you are ready to continue.")
	        
	return totalScore

#final name trials block

def final_name_trials_block(exp, totalScore = 0):
        exp.showText("Now we will check to see whether you still know the names of the 8 elvish directions. There is no time pressure. Just try to remember the correct name for each direction. Please press enter when you are ready.")
	finalNameTrialCounter = 0
	for curTrial in exp.finalNameInfo:
	    finalNameTrialCounter += 1
	    exp.runLearningTrial(curTrial['trialType'], finalNameTrialCounter, curTrial,"NA",labelFeedback = 1, feedback = False)
	
	exp.showText("You've reached the end of the experiment. You've helped the elves collect " + str(totalScore) + " treasure coins, great job! The elves thank you for your help. Please press enter to end the experiment.")



		
def runStudy():
    
	exp = Exp()
	exp.showInstructions(exp.instructions)

        #Enables user to jump to specific blocks in the experiment
	#based on value entered in "Block" at start up 
	if (exp.runTimeVars['block'] == 1):
	    
	    #starts from initial naming trials
	    naming_trials_block(exp)
	    if exp.fixedLearnLen == "yes":
	        learnCount, learnScore = learning_trials_block_fixed(exp)
	    else:
	        learnCount, learnScore = learning_trials_block(exp)
	    totalScore = testing_trials_block(exp, learnCount, learnScore)
	    final_name_trials_block(exp,totalScore)
	
	elif (exp.runTimeVars['block'] == 2):
	    
            # Starts from learning block
            learnCount, learnScore = learning_trials_block(exp)
            if exp.fixedLearnLen == "yes":
	        learnCount, learnScore = learning_trials_block_fixed(exp)
	    else:
	        learnCount, learnScore = learning_trials_block(exp)
            final_name_trials_block(exp,totalScore)
            
	elif (exp.runTimeVars['block'] == 3):
	    
	    # Starts from test trials
	    totalScore = testing_trials_block(exp)
	    final_name_trials_block(exp, totalScore)
		
	elif (exp.runTimeVars['block'] == 4):
	    
	    # Starts at the final naming block
	    final_name_trials_block(exp)
	    
	else:
	    
	    # Runs the entire experiment, sharing variables
	    # between each function 
	    nvlearn_trials_block(exp)
	    naming_trials_block(exp)
	    if exp.fixedLearnLen == "yes":
	        learnCount, learnScore = learning_trials_block_fixed(exp)
	    else:
	        learnCount, learnScore = learning_trials_block(exp)
	    totalScore = testing_trials_block(exp, learnCount, learnScore)
	    final_name_trials_block(exp,totalScore)

	web.open(exp.surveyURL)
	exp.win.close()

runStudy()
