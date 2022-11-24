
import os
import cv2
import subprocess
import moviepy.editor as mp
from cloudLib.speech_to_text import transcribe_audio_local
from cloudLib.vision_ai import detect_text_local
import shutil
import threading
import logging

folder = 'assets/keyframes/'


def visual_transcribe(path: str):
    clear_folder(folder)
    save_i_keyframes(path)
    return [detect_text_local(folder + filename) for filename in os.listdir(folder)]


def audio_trancribe(path: str):
    my_clip = mp.VideoFileClip(path)
    my_clip.audio.write_audiofile("assets/audio/video_audio.wav")
    result_audio = transcribe_audio_local('assets/audio/video_audio.wav')
    logging.info(
        "video_transcriptor    : audio_trancribe result:" + result_audio)
    return [r.alternatives[0].transcript for r in result_audio]


def clear_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logging.warning(
                f'video_trancriptor  : Failed to delete {file_path}. Reason: {e}')


def get_frame_types(video_fn):
    command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
    out = subprocess.check_output(command + [video_fn]).decode()
    frame_types = out.replace('pict_type=', '').split()
    return zip(range(len(frame_types)), frame_types)


def save_i_keyframes(video_fn):
    frame_types = get_frame_types(video_fn)
    i_frames = [x[0] for x in frame_types if x[1] == 'I']
    if i_frames:
        basename = os.path.splitext(os.path.basename(video_fn))[0]
        cap = cv2.VideoCapture(video_fn)
        for frame_no in i_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ret, frame = cap.read()
            outname = basename+'_i_frame_'+str(frame_no)+'.jpg'
            cv2.imwrite('assets/keyframes/' + outname, frame)
            logging.info('Saved: '+outname)
        cap.release()
    else:
        logging.info('No I-frames in '+video_fn)


def transcribe_video(path: str):
    vt = threading.Thread(target=visual_transcribe, args=(1,))
    at = threading.Thread(target=audio_trancribe, args=(1,))
    vt.start()
    at.start()
    logging.info("video_trancriptor    : wait for the transcriptions to finish")
    vt.join()
    at.join()
    logging.info("video_trancriptor    : all done")
    result = "\n".join(vt + at)
    logging.info("video_trancriptor    :" + result)

    return result
