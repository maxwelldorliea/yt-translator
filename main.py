from yt_video.yt_video import *
import sys

vid_downloader(sys.argv[1], sys.argv[2])
convrt_to_cap_audio(sys.argv[2])
