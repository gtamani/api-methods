#Music with python

import sounddevice as sd
import numpy as np
import threading
import random

class Composer:

    def __init__(self,crotchet):
        self.framerate = 44100
        self.frequencies = [self.get_frequency(note,3) for note in range(1,13)]
        self.frequencies += [self.get_frequency(note,4) for note in range(1,13)]
        self.crotchet = crotchet
        self.notes = {"C#":1,"C":0,"D#":3,"D":2,"E":4,"F#":6,"F":5,"G#":8,"G":7,"A#":10,"A":9,"B":11}
        self.triads = {"dim":[0,3,6],"M":[0,4,7],"m":[0,3,7],"aug":[0,4,8]}
        self.septims = {"maj7":{"M":11},"7":{"M":10,"m":10,"dim":9}}
        self.suspended = {"sus4":{"M":5},"sus2":{"M":2}}

    def get_frequency(self,note,octava):
        expo = (octava-3)*12 + (note-10)
        return 440*((2**(1/12)) ** expo)

    def beep(self,frequency,time):
        t = np.linspace(0,time/1000,int(self.framerate*time/1000))
        wave = np.sin(2*np.pi * frequency * t)
        sd.play(wave,self.framerate)
        sd.wait()
        
    def get_scale_and_chords(self,chord):
        count,found = 0,False
        while not found:
            keys =  list(self.notes.keys())
            y = keys[count] 
            if y in chord:
                splitted = chord.replace(y,"")
                chord = y
                found,count = True,0
            else:
                count += 1
        agreg = []
        found = False
        while not found and count <= 1:
            keys =  list(self.septims.keys())
            y = keys[count]  
            if y in splitted:
                splitted = splitted.replace(y,"")
                agreg.append(y)
                found = True
            else:
                count += 1
        mode = "M"
        for i in self.triads.keys():
            if i in splitted:
                splitted = splitted.replace(i,"")
                mode = i
        if agreg:
            agreg = [self.septims[agreg[0]][mode]]
        for i in self.suspended.keys():
            if i in splitted:
                splitted = splitted.replace(i,"")
                agreg.append(self.suspended[i][mode])
        scale = [0,2,4,5,7,9,11] if mode == "M" else [0,2,3,5,7,8,10]
        scale = [(self.notes[chord]+x)%12  for x in scale]
        return scale,[(x + self.notes[chord]) for x in self.triads[mode] + agreg]
        
    def generate_melody(self,scale):
        time_for_chord = self.crotchet * 4
        note_duration = 0
        notes = []
        
        #Time and pitch
        while time_for_chord:
            note_duration = random.choice([self.crotchet/2]*3+[self.crotchet]*4+[self.crotchet*x for x in [1.5,2,2.5,3,3.5,4]])
            if note_duration <= time_for_chord:
                pitch = random.choice(scale+[scale[0],scale[3],scale[4]])
                notes.append((pitch,note_duration))
                time_for_chord -= note_duration

        return notes



    def play_chord(self,chord):
        threads = []
        for i in chord:
            th = threading.Thread(target=lambda:self.beep(self.frequencies[i],self.crotchet*4))
            th.start()
            threads.append(th)
        for th in threads:
            th.join()

    def play_melody(self,list_of_notes):
        for i in list_of_notes:
            self.beep(self.frequencies[i[0]],i[1])
            


def play_progresion(progression,answer):
    composer = Composer(500)
    for i in progression:
        scale,chord_notes = composer.get_scale_and_chords(i)
        melody = composer.generate_melody(scale)

        #play_chord(chord_notes)
        if answer == "m":
            composer.play_melody(melody)
        else:
            composer.play_chord(chord_notes)
    composer.beep(composer.frequencies[composer.notes[progression[0]]],composer.crotchet)



def main():
    progression = []
    print("Inserte 4 acordes")
    for i in range(4):
        chord = input(str(i+1)+". ")
        progression.append(chord)
        
    answers = ["m","c"]
    answer = ""
    while answer.lower() not in answers:
        answer = input("melody or chords? (m/c): ")
    play_progresion(progression,answer)

if __name__ == "__main__":
    print([500/2]*3+[500]*4+[500*x for x in [1.5,2,2.5,3,3.5,4]])
    main()
