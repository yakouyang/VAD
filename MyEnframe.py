import numpy as np
import math

def enframe(signal,frameLen,frameStep):
	'''
	signal:origin wav
	frameLen:every frame length
	frameStep:every frame step
	'''
	sLen=len(signal)
	frameLen=int(round(frameLen))
	frameStep=int(round(frameStep))
	if sLen<=frameLen:
		numFrames=1
	else:
		numFrames=1+int(math.ceil((1.0*sLen-frameLen)/frameStep))#ceil return a int that not less than input
	
	padLen=int((numFrames-1)*frameStep+frameLen)
	zeros=np.zeros((padLen-sLen,))
	padsignal=np.concatenate((signal,zeros))
	
	indices=np.tile(np.arange(0,frameLen),(numFrames,1))+np.tile(np.arange(0,numFrames*frameStep,frameStep),(frameLen,1)).T#T is Transpose
	frames=padsignal[indices]

	return frames