from moviepy.editor import *

# 載入你的MP4文件
video = VideoFileClip(r"E:\下載\Line的傳訊息聲.mp4")
                      
# 從視頻中提取音頻
audio = video.audio

# 將音頻存儲為MP3文件
audio.write_audiofile("output_audio.mp3")

# 釋放資源
audio.close()
video.close()
