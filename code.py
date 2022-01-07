import board
import analogio
import digitalio
import audiobusio
import audiocore
import audiomixer
import config

TRIGGER_VALUE = config.TRIGGER_VALUE
trigger1 = analogio.AnalogIn(board.A0)
trigger2 = analogio.AnalogIn(board.A1)
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

audio = audiobusio.I2SOut(board.GP10, board.GP11, board.GP9)
sample1 = audiocore.WaveFile(open(config.SAMPLE1_PATH, "rb"))
sample2 = audiocore.WaveFile(open(config.SAMPLE2_PATH, "rb"))
mixer = audiomixer.Mixer(voice_count=2, sample_rate=44100, channel_count=1,
                         bits_per_sample=16, samples_signed=True)
mixer.voice[0].level = config.SAMPLE1_LEVEL
mixer.voice[1].level = config.SAMPLE2_LEVEL

audio.play(mixer)
sample1triggered = False
sample2triggered = False

while True:
    led.value = trigger1.value > TRIGGER_VALUE or trigger2.value > TRIGGER_VALUE
    if trigger1.value > TRIGGER_VALUE and sample1triggered == False:
        mixer.voice[0].play(sample1)
        sample1triggered = True

    if trigger2.value > TRIGGER_VALUE and sample2triggered == False:
        mixer.voice[1].play(sample2)
        sample2triggered = True    
    
    if trigger1.value <= TRIGGER_VALUE:
        sample1triggered = False

    if trigger2.value <= TRIGGER_VALUE:
        sample2triggered = False   