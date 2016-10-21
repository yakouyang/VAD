import numpy as np
from scipy.io import wavfile
import scipy.signal
from MyEnframe import enframe
import matplotlib.pyplot as plt

def vad(x,fs):
	x=np.double(x)/max(abs(x))
	
	FrameLen=int(round(fs*0.025))	#25ms
	FrameInc=int(round(fs*0.01))	#10ms
	
	amp1=10
	amp2=2
	zcr1=10
	zcr2=5
	
	maxsilence=8	#8*10ms(frameInc)=80ms
	minlen=15	#15*10ms(frameInc)=150ms
	status=0
	count=0
	silence=0
	
	#calculate the zero-crossing rate(ZCR)
	tmp1=enframe(x[:len(x)],FrameLen,FrameInc)
	tmp2=enframe(x[1:len(x)-1],FrameLen,FrameInc)
	signs=tmp1*tmp2<0
	diffs =(tmp1-tmp2)>0.02
	zcr =np.sum(signs*diffs,1)
	
	#calculate the short-time energy
	amp=np.sum(abs(enframe(scipy.signal.lfilter([1.0,-0.9375], 1,x),FrameLen,FrameInc)),1)
	
	#adjust the limit of energy
	amp1=min(amp1,max(amp)/4)
	amp2=min(amp2,max(amp)/8)
	
	#detect begin point
	x1=0
	x2=0
	for n in range(len(zcr)):
		goto=0;
		# 0 = silent 1=perhaps begin
		if status==0 or status==1:
			#certainly get into voice segment
			if amp[n]>amp1:
				x1=max(n-count-1,1)
				status=2
				silence=0
				count+=1
			#perhaps in voice segment
			elif amp[n]>amp2 or zcr[n]>zcr2:
				status=1
				count+=1
			#silent segment
			else:
				status=0
				count=0
		#2=voice segment
		elif status==2:
			#still in voice segment
			if amp[n]>amp2 or zcr[n]>zcr2:
				count+=1
			#voice segment in closing
			else:
				silence+=1
				#silent segment not reach the limit,still in voice segment
				if silence<maxsilence:
					count+=1
				#voice segment is considered as noise for it's length too short
				elif count<minlen:
					status=0
					silence=0
					count=0
				#voice segment over
				else:
					status=3
		elif status==3:
			break
	count-=silence/2
	x2=x1+count-1
	
	#if you want to see the result ,get the 
	'''
	plt.subplot(311)
	plt.plot(x)
	plt.axis([1,len(x),-1,1])
	plt.ylabel('Speech')
	plt.plot([x1*FrameInc,x1*FrameInc],[-1,1],'r')
	plt.plot([x2*FrameInc,x2*FrameInc],[-1,1],'r')
	plt.subplot(312)
	plt.plot(amp)
	plt.axis([1,len(amp),0,max(amp)])
	plt.ylabel('Energy')
	plt.plot([x1,x1],[min(amp),max(amp)],'r')
	plt.plot([x2,x2],[min(amp),max(amp)],'r')
	plt.subplot(313)
	plt.plot(zcr)
	plt.axis([1,len(zcr),0,max(zcr)])
	plt.ylabel('ZCR')
	plt.plot([x1,x1],[min(zcr),max(zcr)],'r')
	plt.plot([x2,x2],[min(zcr),max(zcr)],'r')
	plt.show()
	'''
	return x1,x2
