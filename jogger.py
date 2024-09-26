from rtmidi.midiconstants import NOTE_ON
from rtmidi.midiutil import open_midiinput, open_midioutput

# The JOG_MULTIPLIER is required for smooth jog operation. 
# Pioneer controllers seem to be sending MIDI signal at a much higher rate than XONE:4D. 
# If you send one fake Pioneer message for each Xone jog message, scratching sounds unnatural.
# You need to test different values for other controllers.
JOG_MULTIPLIER = 15 
BASE_CHANNEL_JOG = 176
BASE_CHANNEL_ON = 144
BASE_CHANNEL_OFF = 128

CONV_J_VAL = {
    1:65,   
    2:66,   
    4:67,   
    7:69,   
    11:71,  
    16:73,  
    20:75,  
    30:80,  
    127:63,
    126:62,
    125:62,
    124:61,
    121:59,
    117:57,
    112:55,
    108:53,
    98:48,
    97:47,
    }

tempo_values = [
    [63, 63],
    [63, 63],
    [63, 63],
    [63, 63],
]

def tempo(id):
    msb = [0xB0+id, 0x00, tempo_values[id][0]]
    lsb = [0xB0+id, 0x20, tempo_values[id][1]]
    midiout.send_message(msb)
    midiout.send_message(lsb)

def jog(msg, deck_id):
    v = CONV_J_VAL[msg[0][2]]

    ms = [176+deck_id, 0x22, v]
    print("jogging")
    print(ms)
    for i in range(JOG_MULTIPLIER):
        midiout.send_message(ms)

def touch_on(msg, deck_id):
    print("touch_on")
    touch = [0x90+deck_id, 0x36, 0x7F]
    midiout.send_message(touch)

def touch_off(msg, deck_id):
    print("touch_off")
    release = [0x90+deck_id, 0x36, 0x00]
    midiout.send_message(release)

def tempo_big(msg, deck_id):
    print("tempo_big")
    tempo_values[deck_id][0] = 127 - msg[0][2]
    tempo(deck_id)

def tempo_fine(msg, deck_id):   
    print("tempo_fine")
    tempo_values[deck_id][1] =  127 - msg[0][2]
    tempo(deck_id)     

CODE_LOOKUP = {}
for i in range(0, 15):
    CODE_LOOKUP[(144 + i, 33)] = touch_on
    CODE_LOOKUP[(128 + i, 33)] = touch_off
    CODE_LOOKUP[(176 + i, 37)] = jog
    CODE_LOOKUP[(176 + i, 16)] = tempo_big
    CODE_LOOKUP[(176 + i, 17)] = tempo_fine

def process(ims, deck_id):
    ims_2b = tuple(ims[0][:2])
    time_diff = ims[1]
    #Bottom row of buttons on the xone 1d sends double messages sometimes, this is a workaround
    if time_diff > 0.001:
        in_hex = [hex(i) for i in ims[0]]
        print(in_hex)
        channel = ims[0][0]

        if channel-deck_id == BASE_CHANNEL_JOG:
            print("JOG message received:" + str(ims) + " on channel " + str(int(channel) - int(BASE_CHANNEL_JOG)))
        elif channel-deck_id == BASE_CHANNEL_ON:
            print("ON message received:" + str(ims) + " on channel " + str(int(channel) - int(BASE_CHANNEL_ON)))
        elif channel-deck_id == BASE_CHANNEL_OFF:
            print("OFF message received:" + str(ims) + " on channel " + str(int(channel) - int(BASE_CHANNEL_OFF)))
        
        if ims_2b in CODE_LOOKUP:
            CODE_LOOKUP[ims_2b](ims, deck_id)
        else:
            msg = ims[0]
            midiout.send_message(msg)
                    
with open_midiinput(None)[0] as midiin:
    with open_midiinput(None)[0] as midiin2:
        with open_midioutput(None)[0] as midiout:
            while True:
                ims = midiin.get_message()
                ims2 = midiin2.get_message()
                
                if ims:
                    process(ims, 0)
                if ims2:
                    process(ims2, 1)