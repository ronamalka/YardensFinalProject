import fleep
from pydub import AudioSegment
import ffmpeg
import librosa
import soundfile  # to read audio file
import numpy as np
from dtw import dtw
from numpy.linalg import norm
import pickle
from asteroid.models import BaseModel
import asteroid
import soundfile as sf


def wav_check(filename):
    with open(filename, "rb") as file:
        info = fleep.get(file.read(128))
    file_type = info.extension[0]
    return file_type == 'wav'



def number_of_channels(filename):
    audio_file = AudioSegment.from_file(file=filename, format="wav")
    return audio_file.channels



def mp3_check(filename):
    with open(filename, "rb") as file:
        info = fleep.get(file.read(128))
    file_type = info.extension[0]
    return file_type == 'mp3'



def create_wav_from_mp3(filename, wav_filename):
    sound = AudioSegment.from_mp3(filename)
    sound.export(wav_filename, format="wav")
    return None



def create_mono_from_non_mono(filename, mono_filename):     #wav_only
    sound = AudioSegment.from_wav(filename)
    sound = sound.set_channels(1)
    sound.export(mono_filename, format="wav")
    return None



def split_stereo_to_two_separate_mono(filename):             #wav_only
    stereo_audio = AudioSegment.from_file(filename, format="wav")
    mono_audios = stereo_audio.split_to_mono()
    mono_left = mono_audios[0].export("mono_left.wav", format="wav")
    mono_right = mono_audios[1].export("mono_right.wav", format="wav")
    return None



def extract_feature(file_name, **kwargs):     #**kwargs= keyword argument, type(**kwargs)=dictionary, its used when number of passed arguments is unknown to avoid errors.
    """
    Extract feature from audio file `file_name`
        Features supported:
            - MFCC (mfcc)
            - Chroma (chroma)
            - MEL Spectrogram Frequency (mel)
            - Contrast (contrast)
            - Tonnetz (tonnetz)
        e.g.:
        `features = extract_feature(path, mel=True, mfcc=True)
        """
    mfcc = kwargs.get("mfcc")
    chroma = kwargs.get("chroma")
    mel = kwargs.get("mel")
    contrast = kwargs.get("contrast")
    tonnetz = kwargs.get("tonnetz")
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        if chroma or contrast:
            stft = np.abs(librosa.stft(X))                #stft = short time fourier transform,  used to determine the sinusoidal frequency and phase content of local sections of a signal as it changes over time.
        result = np.array([])
        if mfcc:
            mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfccs))                                              #np.hstack = concatenates items to result
        if chroma:
            chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T, axis=0)
            result = np.hstack((result, mel))
        if contrast:
            contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, contrast))
        if tonnetz:
            tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T, axis=0)
            result = np.hstack((result, tonnetz))
    return result



def return_user_recording(user_features, recordingfile1, recordingfile2):
    #base_features = extract_feature(user_voice, mfcc=True, chroma=True, mel=True).reshape(1, -1)
    base_features = user_features
    features1 = extract_feature(recordingfile1, mfcc=True, chroma=True, mel=True).reshape(1, -1)
    features2 = extract_feature(recordingfile2, mfcc=True, chroma=True, mel=True).reshape(1, -1)
    dist1, cost_matrix1, acc_cost_matrix1, path1 = dtw(base_features, features1, dist=lambda base_features, features1: norm(base_features - features1, ord=1))
    dist2, cost_matrix2, acc_cost_matrix2, path2 = dtw(base_features, features2, dist=lambda base_features, features2: norm(base_features - features2, ord=1))
    info = []
    info.append([recordingfile1, features1, dist1, cost_matrix1, acc_cost_matrix1, path1])
    info.append([recordingfile2, features2, dist2, cost_matrix2, acc_cost_matrix2, path2])
    if info[0][2] <= info[1][2]:
        return info[0][0]
    else:
        return info[1][0]



def separate_audio(filename, model_path):
    model = pickle.load(open(model_path, 'rb'))
    model.separate(filename, resample = True, force_overwrite=True)
    return None



def remove_silence(audio_file, clear_filename): #clear_filename must have .wav suffix
    # read wav data
    audio, sr = librosa.load(audio_file, sr=8000, mono=True)
    # print(audio.shape, sr)
    clips = librosa.effects.split(audio, top_db=25)
    # print(clips)
    wav_data = []
    for c in clips:
        # print(c)
        data = audio[c[0]: c[1]]
        wav_data.extend(data)
    sf.write(clear_filename, wav_data, sr)
    return None









