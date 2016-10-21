# VAD
voice active detection (python ver/simple and easy-to-use)

##Before use
You must have MyEnframe.py and vad.py and your files in the same direction
##Usage
`from vad import vad`
`[x1,x2]=vad(signal,fs)`
##Input
|Input|Description|
|--------|--------|
|signal|The signal which you want to get active-voice frame imformation|
|fs|Sampling rate of the signal|
##Output
| Output | Description |
|--------|--------|
|x1|The frame header of voice active part|
|x2|The tail frame of voice active part|
##Requirements
python 2
numpy

