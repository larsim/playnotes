import pyaudio
import numpy as np

p = pyaudio.PyAudio()

volume = 1.0    # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 0.4   # in seconds, may be float
f = 440.0        # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

notes = {"F#3": 185.00}
notes["b3"] = 246.94
notes["d4"] = 293.66
notes["F#4"] =  369.99
notes["a4"] = 440.00
notes["a3"] = 220.00
notes["e3"] = 164.81
notes["C#4"] = 277.18
notes["C#3"] = 138.59
notes["A#3"] = 233.08
notes["D#4"] = 311.13
notes["A#4"] = 466.16
notes["D#3"] = 155.56
notes["a2"] = 110.00
notes["A#2"] = 116.54
notes["G#3"] = 207.65

def pf(freq):
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*freq/fs)).astype(np.float32)
    if freq == 0:
        samples *= 0.0
    stream.write(samples)

def p(txt):
    pf(notes[txt])

def play(txt):
    print(txt)
    freqs = []
    octave = 4
    i = 0
    prev = ""
    for c in txt:
        if c in "123456":
            octave = int(c)
            i = 0
            continue
        elif c in "cdefgab":
            tmptxt = str(c) + str(octave)
            prev = tmptxt
            if i >= len(freqs):
                freqs.append(notes[tmptxt])
            else:
                freqs[i] = notes[tmptxt]
        elif c in "CDEFGAB":
            tmptxt = str(c) + "#" + str(octave)
            prev = tmptxt
            if i >= len(freqs):
                freqs.append(notes[tmptxt])
            else:
                freqs[i] = notes[tmptxt]
        elif c == '-':
            if i >= len(freqs):
                freqs.append(0.0)
        elif c == '_':
            if i >= len(freqs):
                freqs.append(notes[tmptxt])
            else:
                freqs[i] = notes[tmptxt]
        else:
            continue
        i += 1
    for f in freqs:
        #print(f)
        pf(f)
    #input("")

#play("4|--------d__---------d---d-|\n3|F-b--Fb-------b__------b--|\n")
#play("4|F__---d__---F--dF-a__------|\n3|------------------------a__|\n")
#play("4|---d---d-F__---------d---|\n3|------a------------a----a|\n")
#play("4|d-F__---d__---F--dF-a__---|\n")
#play("4|F__---------C__-----------|\n3|------a--Fa-------C__---F-|\n")
#play("3|-CF-A__-------------------|\n") # NOE RART HER

play("4|--------------D__---------|\n3|------F-b--Fb-------b__---|\n")
play("4|D---D-F__---D__---F--DF-A__|\n3|---b-----------------------|\n")
play("4|---------D---D-F__-------|\n3|---A__------A------------|\n")
play("3|--D---D-F__---D__---F--DF-|\n2|A----A--------------------|\n")

play("4|------------------C__-----|\n3|A__---F__---A--FA-------C_|\n")
play("3|----F--CF-A___------F-G--e|\n")
play("3|G-b__-------F-G--eG-b__---|\n")
play("4|------------C__-----------|\n3|----F-G--eG-------F__---b-|\n")
play("4|----D__-------------------|\n3|-Fb-----------F-G--eG-b__-|\n")
play("4|--------------C__---------|\n3|------F-G--eG-------F__---|\n")
play("4|------D---D-F--DF-F____---|\n3|b--Fb----b----------------|\n")

stream.stop_stream()
stream.close()