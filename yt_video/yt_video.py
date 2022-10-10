from os import error
from pytube import YouTube as YT, captions
from gtts import gTTS




def vid_downloader(url:str, filename:str)->None:
    yt_obj = YT(url);
    print(yt_obj.author, yt_obj.title)
    print(yt_obj.captions)
    cap = yt_obj.captions['en']
    caps = cap.generate_srt_captions()
    comp_filename = filename + ".txt"

    with open(comp_filename, 'w') as f:
        f.write(caps)

def get_only_sentence(filename) -> str:
    word:str  = ""
    with open(filename, 'r') as file:

        for i in file.read():
            if i.isalpha():
                word += i
        return word

def convrt_to_cap_audio(filename):
    filename = filename + ".txt"
    word = get_only_sentence(filename)
    tts_en = gTTS(word, lang='en')

    with open('new_en.mp3', 'wb') as f:
        tts_en.write_to_fp(f)


