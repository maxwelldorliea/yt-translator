from os import error
from pytube import YouTube as YT, captions
from gtts import gTTS




def vid_downloader(url:str)->None:
    yt_obj = YT(url);
    print(yt_obj.author, yt_obj.title)
    print(yt_obj.captions)
    cap = yt_obj.captions['a.en']
    caps = cap.generate_srt_captions()

    with open('caption.txt', 'w') as f:
        f.write(caps)

def get_only_sentence(filename) -> str:
    word:str  = ""
    with open(filename, 'r') as file:

        for i in file.read():
            if i.isalpha():
                word += i
        return word

def convrt_to_cap_audio(filename):
    word = get_only_sentence(filename)
    tts_en = gTTS(word, lang='en')

    with open('new_en.mp3', 'wb') as f:
        tts_en.write_to_fp(f)


