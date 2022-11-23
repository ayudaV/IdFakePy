
import os
import cv2
import subprocess
import moviepy.editor as mp
from cloudLib.speech_to_text import audio_transcript_local
from cloudLib.vision_ai import detect_text_local
import shutil

def clearFolder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            
def get_frame_types(video_fn):
    command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
    out = subprocess.check_output(command + [video_fn]).decode()
    frame_types = out.replace('pict_type=','').split()
    return zip(range(len(frame_types)), frame_types)

def save_i_keyframes(video_fn):
    frame_types = get_frame_types(video_fn)
    i_frames = [x[0] for x in frame_types if x[1]=='I']
    if i_frames:
        basename = os.path.splitext(os.path.basename(video_fn))[0]
        cap = cv2.VideoCapture(video_fn)
        for frame_no in i_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ret, frame = cap.read()
            outname = basename+'_i_frame_'+str(frame_no)+'.jpg'
            cv2.imwrite('assets/keyframes/' + outname, frame)
            print ('Saved: '+outname)
        cap.release()
    else:
        print ('No I-frames in '+video_fn)

def transcribe_video(path:str):
    folder = 'assets/keyframes/'
    my_clip = mp.VideoFileClip(path)
    my_clip.audio.write_audiofile("assets/audio/video_audio.wav")
    result_audio = audio_transcript_local('assets/audio/video_audio.wav')
    print(result_audio)
    result = "\n".join([r.alternatives[0].transcript for r in result_audio])
    clearFolder(folder)
    save_i_keyframes(path)
    for filename in os.listdir(folder):
        result += "\n" + detect_text_local(folder + filename)
    return result
