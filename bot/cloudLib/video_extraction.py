"""Transcribe speech from a video stored on GCS."""
from google.cloud import videointelligence
import os
import io
video_client = videointelligence.VideoIntelligenceServiceClient()
speech_features = [videointelligence.Feature.SPEECH_TRANSCRIPTION]
text_features = [videointelligence.Feature.TEXT_DETECTION]
config = videointelligence.SpeechTranscriptionConfig(
    language_code="pt-BR", enable_automatic_punctuation=True
)
video_context = videointelligence.VideoContext(speech_transcription_config=config)

def video_transcript(uri: str, filename: str):
    #os.system(f'curl {uri} | gsutil cp - gs://idfake-videofiles/{filename}')
    #bucket_uri = f'gs://idfake-videofiles/{filename}'
    #video_audio_transcript(bucket_uri)
    video_text_transcript_local(uri)
    
#Substituir isto posteriormente
def video_audio_transcript(uri: str):


    operation = video_client.annotate_video(
        request={
            "features": speech_features,
            "input_uri": uri,
            "video_context": video_context,
        }
    )

    print("\nProcessing video for speech transcription.")

    result = operation.result(timeout=600)

    # There is only one annotation_result since only
    # one video is processed.
    annotation_results = result.annotation_results[0]
    for speech_transcription in annotation_results.speech_transcriptions:

        # The number of alternatives for each transcription is limited by
        # SpeechTranscriptionConfig.max_alternatives.
        # Each alternative is a different possible transcription
        # and has its own confidence score.
        for alternative in speech_transcription.alternatives:
            print("Alternative level information:")

            print("Transcript: {}".format(alternative.transcript))
            print("Confidence: {}\n".format(alternative.confidence))

            print("Word level information:")
            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time
                end_time = word_info.end_time
                print(
                    "\t{}s - {}s: {}".format(
                        start_time.seconds + start_time.microseconds * 1e-6,
                        end_time.seconds + end_time.microseconds * 1e-6,
                        word,
                    )
                )

def video_text_transcript(uri: str):
    """Detect text in a video stored on GCS."""

    operation = video_client.annotate_video(
        request={"features": text_features, "input_uri": uri}
    )

    print("\nProcessing video for text detection.")
    result = operation.result(timeout=600)

    # The first result is retrieved because a single video was processed.
    annotation_result = result.annotation_results[0]

    for text_annotation in annotation_result.text_annotations:
        print("\nText: {}".format(text_annotation.text))

        # Get the first text segment
        text_segment = text_annotation.segments[0]
        start_time = text_segment.segment.start_time_offset
        end_time = text_segment.segment.end_time_offset
        print(
            "start_time: {}, end_time: {}".format(
                start_time.seconds + start_time.microseconds * 1e-6,
                end_time.seconds + end_time.microseconds * 1e-6,
            )
        )

        print("Confidence: {}".format(text_segment.confidence))

        # Show the result for the first frame in this segment.
        frame = text_segment.frames[0]
        time_offset = frame.time_offset
        print(
            "Time offset for the first frame: {}".format(
                time_offset.seconds + time_offset.microseconds * 1e-6
            )
        )
        print("Rotated Bounding Box Vertices:")
        for vertex in frame.rotated_bounding_box.vertices:
            print("\tVertex.x: {}, Vertex.y: {}".format(vertex.x, vertex.y))
            
def video_text_transcript_local(path:str):
    """Detect text in a local video."""

    with io.open(path, "rb") as file:
        input_content = file.read()

    operation = video_client.annotate_video(
        request={
            "features": text_features,
            "input_content": input_content,
            "video_context": video_context,
        }
    )

    print("\nProcessing video for text detection.")
    result = operation.result(timeout=300)

    # The first result is retrieved because a single video was processed.
    annotation_result = result.annotation_results[0]

    for text_annotation in annotation_result.text_annotations:
        print("\nText: {}".format(text_annotation.text))

video_transcript('./assets/video/video1.mp4', 'video1.mp4')