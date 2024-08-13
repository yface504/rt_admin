from moviepy.editor import *

# 載入你的MP4文件
video = VideoFileClip(r"C:\Users\even5\Desktop\20240804_171952.mp4")
                      
# 從視頻中提取音頻
audio = video.audio

# 將音頻存儲為MP3文件
audio.write_audiofile("output_audio.mp3")

# 釋放資源
audio.close()
video.close()
