from asteroid.models import BaseModel
import soundfile as sf
import pickle
import preprocessing_functions1

model_path = "ConvTasNet_Libri2Mix_sepnoisy_8k.pk1"
##model_path = "C:\\Workspace\\sensound\\ConvTasNet_Libri2Mix_sepnoisy_8k.pk1"
""""C:\Workspace\sensound\ConvTasNet_Libri2Mix_sepnoisy_8k.pk1"
This function will get as an input a wav file of a conversation and user's features.
the function will separate the wav file into 2 wav files of the 2 person in the recording.
it will returns a clear wav file only of the user recording which it identifies it by its user features.
"""
def separation_and_recognition(filename, user_features):
    # load a desired wav audio file, preprocess it then separate it.

    i = filename.index(".")
    new_filename1 = filename[:i] + "_est1" + filename[i:]
    new_filename2 = filename[:i] + "_est2" + filename[i:]

    clear_recording = "clear_recording.wav"

    # need to change the following two lines manually depending on the filename.
    #############################################
    wav_filename = "wav_file.wav"
    mono_filename = "mono_file.wav"
    clear_filename = "clear_file.wav"
    #############################################

    # user_features =  #need to have user voice data(recording or extracted recording features) which is acquired upon signing up to the app.

    wav_check = preprocessing_functions1.wav_check(filename)
    if not wav_check:
        print('file format is not wav!!')
        mp3_check = preprocessing_functions1.mp3_check(filename)
        if not mp3_check:
            print('please load a wav file!')
            quit()
        print('converting to wav')
        preprocessing_functions1.create_wav_from_mp3(filename, wav_filename)

    if not wav_check:
        number_of_channels = preprocessing_functions1.number_of_channels(wav_filename)
        if number_of_channels != 1:
            print('converting to mono')
            preprocessing_functions1.create_mono_from_non_mono(filename, mono_filename)
            preprocessing_functions1.separate_audio(mono_filename, model_path)
            the_recording = preprocessing_functions1.return_user_recording(user_features, "mono_file_est1.wav", "mono_file_est2.wav")
            preprocessing_functions1.remove_silence(the_recording, clear_recording)
            return None
        preprocessing_functions1.separate_audio(wav_filename, model_path)
        the_recording = preprocessing_functions1.return_user_recording(user_features, "wav_file_est1.wav", "wav_file_est2.wav")
        preprocessing_functions1.remove_silence(the_recording, clear_recording)
        return None

    number_of_channels = preprocessing_functions1.number_of_channels(filename)
    if number_of_channels != 1:
        print('converting to mono')
        preprocessing_functions1.create_mono_from_non_mono(filename, mono_filename)
        preprocessing_functions1.separate_audio(mono_filename, model_path)
        the_recording = preprocessing_functions1.return_user_recording(user_features, "mono_file_est1.wav", "mono_file_est2.wav")
        preprocessing_functions1.remove_silence(the_recording, clear_recording)
        return None

    preprocessing_functions1.separate_audio(filename, model_path)
    the_recording = preprocessing_functions1.return_user_recording(user_features, new_filename1, new_filename2)
    preprocessing_functions1.remove_silence(the_recording, clear_recording)
    return None
