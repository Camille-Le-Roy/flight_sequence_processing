########################################################################################################################
# - February 2019 - Camille Le Roy
# At the above date, this code is working under Python 3.7.0a4 - windows 7, with the following packages installed:
# numpy-1.14.0+mkl-cp37-cp37m-win_amd64.whl
# pandas-0.22.0-cp37-cp37m-win_amd64.whl
# matplotlib-2.1.2-cp37-cp37m-win_amd64.whl
# opencv_python-3.4.0-cp37-cp37m-win_amd64.whl
# * All downloaded from  https://www.lfd.uci.edu/~gohlke/pythonlibs/


# Set working directory:
import os
working_dir = ('C:/Users/H. GOMES RODRIGUES/PycharmProjects/flight_sequences_processing')
os.chdir(working_dir)
os.getcwd()
# Importing packages
import numpy as np
import pandas as pd
import cv2
import matplotlib
import math

# Importing datafile
# df = pd.read_csv('session_15.07.csv', sep=';')
# df = pd.read_csv('session_17.07.csv', sep=';')
# df = pd.read_csv('session_27.07.csv', sep=';')
# df = pd.read_csv('session_19.07.csv', sep=';')
# df = pd.read_csv('session_31.07.csv', sep=';')
# df = pd.read_csv('session_31.07session_31.07_CL17_050part2_only.csv', sep=';')
# df = pd.read_csv('session_09.08.csv', sep=';')
# df = pd.read_csv('session_17.08.csv', sep=';')
# df = pd.read_csv('session_21.08.csv', sep=';')
# df = pd.read_csv('session_25.08.csv', sep=';')
# df = pd.read_csv('session_01.09.csv', sep=';')
# df = pd.read_csv('session_27.08.csv', sep=';')
# df = pd.read_csv('session_08.08.csv', sep=';')
# df = pd.read_csv('session_12.09.csv', sep=';')
# df = pd.read_csv('session_04.09.csv', sep=';')
# df = pd.read_csv('session_23.08.csv', sep=';')
# df = pd.read_csv('session_28.07.csv', sep=';')
# df = pd.read_csv('session_30.07.csv', sep=';')
# df = pd.read_csv('session_21.09.csv', sep=';')
# df = pd.read_csv('session_21.09_only_CL17_131and132.csv', sep=';')
# df = pd.read_csv('session_19.08.csv', sep=';')
# df = pd.read_csv('session_20.07.csv', sep=';')
# df = pd.read_csv('session_23.07pm.csv', sep=';')
# df = pd.read_csv('session_15.08.csv', sep=';')
df = pd.read_csv('session_22.07.csv', sep=';')


# df = pd.read_csv('session_21.09.p.m(close).csv', sep=';')
df

# The code has been built to work with a certain type of input data.
# Look at how is built 'df' if you have to use your own data.

################################################# Formatting data ######################################################

list(df) # check column names

specimen_ID = df.loc[:,'specimen_ID'].astype('category')
date = df.loc[:,'date'].astype('category')
species = df.loc[:,'species'].astype('category')
sex = df.loc[:,'sex'].astype('category')
config = df.loc[:,'config'].astype('category')
shoot = df.loc[:,'shoot'].astype(int)

cam1 = df.loc[:,'cam1'].astype(str)
cam2 = df.loc[:,'cam2'].astype(str)
cam3 = df.loc[:,'cam3'].astype(str)

# Assigning cam(i) variable to their respective column in df
for i in range(df.columns.get_loc("cam1") , df.columns.get_loc("cam3")+1):
    vars()['cam'+str(int(i-(df.columns.get_loc("cam1")-1)))] = df.iloc[:,i]
# The cam1, cam2 and cam3 variable contain the filename of the video

# Assigning clap_cam(i) variable to their respective column in df
for i in range(df.columns.get_loc("clap_cam1") , df.columns.get_loc("clap_cam3")+1):
    vars()['clap_cam'+str(int(i-(df.columns.get_loc("clap_cam1")-1)))] = df.iloc[:,i]
# The 'clap_cam' variables are not required for the code to run

# Assigning offset_(i) variable to their respective column in df
for i in range(df.columns.get_loc("offset_1") , df.columns.get_loc("offset_3")+1):
    vars()['offset_'+str(int(i-(df.columns.get_loc("offset_1")-1)))] = df.iloc[:,i]
# The offset_1, offset_2 and offset_3 variables contain the offset between the different cameras

# Assigning S(i) variable to their respective column in df
# (i.e. starting time of individual flight sequences, viewed from cam1)
for i in  range(18):
    vars()['S'+str(int(i+1))] = df.loc[:,'S'+str(int(i+1))]
# The S1, S2, S3 etc. variables contain the starting time (in frame) of the different flight in the video
# i.e. the sequences we are interested in. Here the maximum amount of flight that occurs in one video is 18.



################################# CAMERA 1 - Cutting/Synchronizing/Subtracting Background #################################################
#################################               outputs automatically stored              #################################################

os.chdir(working_dir)
def createFolder(dir):                                                            # function to create folder
    try:                                                                          # receiving output videos
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print ('Error: Creating directory. ' +  dir)

flight_count = 1
for v in range(0,len(cam1)):   # start from the first specimen when v = 0
    current_date = str(df.iloc[v, 1])                                             # loading date
    current_videofile = str(cam1[v])                                              # loading video-file name
    current_species = species[v]                                                  # loading species name
    current_specimen = specimen_ID[v]                                             # loading specimen index

    all_flight_nb = []                                                            # Calculating numbers of
    for k in range(0, len(cam1)):                                                 # flights for all specimens
        for j in range(df.columns.get_loc("S1"), df.columns.get_loc("S18")):
            if math.isnan(df.iloc[k, j]):
                break
            val = (j + 1) - df.columns.get_loc("S1")
        all_flight_nb.append(val)

    working_dir = ('C:/Users/H. GOMES RODRIGUES/PycharmProjects/flight_sequences_processing')# setting current wd
    createFolder('./Flights_' + current_specimen + '_M.' + current_species + '/')            # creating specimen folder
    path_to_write = ('./Flights_' + current_specimen + '_M.' + current_species + '/')        # giving path to that folder
    os.chdir(path_to_write)                                                                  # entering into that folder

    for s in range(1,18): # start from the first flight when s = 1
        if math.isnan(vars()['S' + str(s)][v]):                                              # checking for sequence availability
            break

        cap = cv2.VideoCapture('D:/Gopro_Sequences_LOCAL/PERU_2017/GOPRO Sequences 2017/' +  # path to get raw video
                               current_date + '/' + 'cam1/' + current_videofile + '.mp4')

        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),                                      # defining frame size
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        # fourcc = cv2.VideoWriter_fourcc(*'a\0\0\0')                                             # MP4 codec
        # fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')                                     # AVI codec 1
        fourcc = cv2.VideoWriter_fourcc(*"DIB ")                                              # AVI codec 2 (heavy outputs but it always works !)

        if v == 0:
            current_flight_nb = str(s)
        else:
            current_flight_nb = str(s)
            if specimen_ID[v] == specimen_ID[v - 1]:
                current_flight_nb = all_flight_nb[v - 1] + s
                if specimen_ID[v] == specimen_ID[v - 2]:
                    current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + s
                    if specimen_ID[v] == specimen_ID[v - 3]:
                        current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + all_flight_nb[v - 3] + s
                        if specimen_ID[v] == specimen_ID[v - 4]:
                            current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + all_flight_nb[v - 3] + \
                                                all_flight_nb[v - 4] + s

        # file_to_write = ('Flight_' + str(current_flight_nb) + '_' + 'cam1_M.' + current_species   # naming the output video-file (original)
        #                  + '_' + current_specimen[5:8] + '.avi')
        #
        file_to_write = ('BS_Flight_' + str(current_flight_nb) + '_' + 'cam1_M.' + current_species   # naming the output video-file (BS)
                         + '_' + current_specimen[5:8] + '.avi')

        video = cv2.VideoWriter(str(file_to_write), fourcc, 240, size)                       # open-cv recording function

        fgbg = cv2.createBackgroundSubtractorMOG2()                                          # MOG2 function

        start = int(vars()['S'+ str(s)][v])                                                  # start-frame-nb
        stop = int(start + (7*240))                                                          # stop-frame-nb (7sec later by default)

        f = 1
        while True:                                                                          # start video loop
            ret, frame = cap.read()
            tot_frame = int(cap.get(7))
            f += 1                                                                           # frame passing
            if f%100 == 0:                                                                   # printing frequency
                print('filename:', cam1[v],'[cam1]', '  ',                                   # text printed
                      'Morpho',species[v], specimen_ID[v],'  ',
                      'Flight n°',current_flight_nb,'  ',
                      'frame n°', f,'  ',
                      'next flight in', int((start-f)/14400),'min',
                      int((start-f)/240) - (int((start-f)/14400)*60),'sec','   ',
                      'Global progress:', round(flight_count*100/(sum(all_flight_nb)),2),'%')

            fgmask = fgbg.apply(frame)                                                       # applying subtraction

            if f > start:
                cv2.imshow(str('Recording: '+ file_to_write), frame)                         # display original frame from start-f-n
                # video.write(frame) # SAVE ORIGINAL VERSION
                video.write(fgmask) #  SAVE SUBTRACTED VERSION
                cv2.imshow('subtracted', fgmask)                                             # display subtracted frame from start-f-n
                cv2.waitKey(4)
            if f == tot_frame:
                break
            if f > stop:                                                                     # stop from stop-f-n
                break
        cap.release()
        video.release()
        cv2.destroyAllWindows()
        flight_count += 1
    os.chdir(working_dir)                                                                    # leaving specimen folder



################################# CAMERA 2 - Cutting/Synchronizing/Subtracting Background #################################################
#################################               outputs automatically stored              #################################################

os.chdir(working_dir)
def createFolder(dir):                                                            # function to create folder
    try:                                                                          # receiving output videos
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print ('Error: Creating directory. ' +  dir)

flight_count = 1
for v in range(0,len(cam2)):   # start from the first specimen when v = 0
    current_date = str(df.iloc[v, 1])                                             # loading date
    current_videofile = str(cam2[v])                                              # loading video-file name
    current_species = species[v]                                                  # loading species name
    current_specimen = specimen_ID[v]                                             # loading specimen index

    all_flight_nb = []                                                            # Calculating numbers of
    for k in range(0, len(cam2)):                                                 # flights for all specimens
        for j in range(df.columns.get_loc("S1"), df.columns.get_loc("S18")):
            if math.isnan(df.iloc[k, j]):
                break
            val = (j + 1) - df.columns.get_loc("S1")
        all_flight_nb.append(val)

    working_dir = ('C:/Users/H. GOMES RODRIGUES/PycharmProjects/flight_sequences_processing')# setting current wd
    createFolder('./Flights_' + current_specimen + '_M.' + current_species + '/')            # creating specimen folder
    path_to_write = ('./Flights_' + current_specimen + '_M.' + current_species + '/')        # giving path to that folder
    os.chdir(path_to_write)                                                                  # entering into that folder

    for s in range(1,18): # start from the first flight when s = 1
        if math.isnan(vars()['S' + str(s)][v]):                                              # checking for sequence availability
            break

        cap = cv2.VideoCapture('D:/Gopro_Sequences_LOCAL/PERU_2017/GOPRO Sequences 2017/' +  # path to get raw video
                               current_date + '/' + 'cam2/' + current_videofile + '.mp4')

        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),                                      # defining frame size
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        # fourcc = cv2.VideoWriter_fourcc(*'a\0\0\0')                                             # MP4 codec
        # fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')  # AVI codec 1                      # AVI codec 1
        fourcc = cv2.VideoWriter_fourcc(*"DIB ")                                              # AVI codec 2 (heavy outputs but it always works !)

        if v == 0:
            current_flight_nb = str(s)
        else:
            current_flight_nb = str(s)
            if specimen_ID[v] == specimen_ID[v - 1]:
                current_flight_nb = all_flight_nb[v - 1] + s
                if specimen_ID[v] == specimen_ID[v - 2]:
                    current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + s
                    if specimen_ID[v] == specimen_ID[v - 3]:
                        current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + all_flight_nb[v - 3] + s
                        if specimen_ID[v] == specimen_ID[v - 4]:
                            current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + all_flight_nb[v - 3] + \
                                                all_flight_nb[v - 4] + s

        # file_to_write = ('Flight_' + str(current_flight_nb) + '_' + 'cam2_M.' + current_species   # naming the output video-file (original)
        #                  + '_' + current_specimen[5:8] + '.avi')
        #
        file_to_write = ('BS_Flight_' + str(current_flight_nb) + '_' + 'cam2_M.' + current_species   # naming the output video-file (BS)
                         + '_' + current_specimen[5:8] + '.avi')

        video = cv2.VideoWriter(str(file_to_write), fourcc, 240, size)                       # open-cv recording function

        fgbg = cv2.createBackgroundSubtractorMOG2()                                          # MOG2 function

        start = int(vars()['S'+ str(s)][v]) + offset_2[v]                                    # start-frame-nb considering offset CAM2
        stop = int(start + (7*240))                                                          # stop-frame-nb (7sec later by default)

        f = 1
        while True:                                                                          # start video loop
            ret, frame = cap.read()
            tot_frame = int(cap.get(7))
            f += 1                                                                           # frame passing
            if f % 100 == 0:                                                                 # printing frequency
                print('filename:', cam2[v], '[cam2]', '  ',                                  # printing information
                      'Morpho', species[v], specimen_ID[v], '  ',
                      'Flight n°', current_flight_nb, '  ',
                      'frame n°', f, '  ',
                      'next flight in', int((start - f) / 14400), 'min',
                      int((start - f) / 240) - (int((start - f) / 14400) * 60), 'sec', '   ',
                      'Global progress:', round(flight_count * 100 / (sum(all_flight_nb)), 2), '%')

            fgmask = fgbg.apply(frame)                                                       # applying subtraction

            if f > start:
                cv2.imshow(str('Recording: ' + file_to_write), frame)                       # display original frame from start-f-n
                # video.write(frame) # SAVE ORIGINAL VERSION
                video.write(fgmask) #  SAVE SUBTRACTED VERSION
                cv2.imshow('subtracted', fgmask)                                             # display subtracted frame from start-f-n
                cv2.waitKey(4)
            if f == tot_frame:
                break
            if f > stop:                                                                    # stop from stop-f-n
                break
        cap.release()
        video.release()
        cv2.destroyAllWindows()
        flight_count += 1
    os.chdir(working_dir)                                                                   # leaving specimen folder





################################# CAMERA 3 - Cutting/Synchronizing/Subtracting Background #################################################
#################################               outputs automatically stored              #################################################

os.chdir(working_dir)
def createFolder(dir):                                                            # function to create folder
    try:                                                                          # receiving output videos
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print ('Error: Creating directory. ' +  dir)

flight_count = 1
for v in range(0,len(cam3)): # start from the first specimen when v = 0
    current_date = str(df.iloc[v, 1])                                             # loading date
    current_videofile = str(cam3[v])                                              # loading video-file name
    current_species = species[v]                                                  # loading species name
    current_specimen = specimen_ID[v]                                             # loading specimen index

    all_flight_nb = []                                                            # Calculating numbers of
    for k in range(0, len(cam3)):                                                 # flights for all specimens
        for j in range(df.columns.get_loc("S1"), df.columns.get_loc("S18")):
            if math.isnan(df.iloc[k, j]):
                break
            val = (j + 1) - df.columns.get_loc("S1")
        all_flight_nb.append(val)

    working_dir = ('C:/Users/H. GOMES RODRIGUES/PycharmProjects/flight_sequences_processing')# setting current wd
    createFolder('./Flights_' + current_specimen + '_M.' + current_species + '/')            # creating specimen folder
    path_to_write = ('./Flights_' + current_specimen + '_M.' + current_species + '/')        # giving path to that folder
    os.chdir(path_to_write)                                                                  # entering into that folder

    for s in range(1,18): # start from the first flight when s = 1
        if math.isnan(vars()['S' + str(s)][v]):                                              # checking for sequence availability
            break

        cap = cv2.VideoCapture('D:/Gopro_Sequences_LOCAL/PERU_2017/GOPRO Sequences 2017/' +  # path to get raw video
                               current_date + '/' + 'cam3/' + current_videofile + '.mp4')

        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),                                      # defining frame size
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        # fourcc = cv2.VideoWriter_fourcc(*'a\0\0\0')                                             # MP4 codec
        # fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')  # AVI codec 1                      # AVI codec 1
        fourcc = cv2.VideoWriter_fourcc(*"DIB ")                                              # AVI codec 2 (heavy outputs but it always works !)

        if v == 0:
            current_flight_nb = str(s)
        else:
            current_flight_nb = str(s)
            if specimen_ID[v] == specimen_ID[v - 1]:
                current_flight_nb = all_flight_nb[v - 1] + s
                if specimen_ID[v] == specimen_ID[v - 2]:
                    current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + s
                    if specimen_ID[v] == specimen_ID[v - 3]:
                        current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + all_flight_nb[v - 3] + s
                        if specimen_ID[v] == specimen_ID[v - 4]:
                            current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + all_flight_nb[v - 3] + \
                                                all_flight_nb[v - 4] + s

        # file_to_write = ('Flight_' + str(current_flight_nb) + '_' + 'cam3_M.' + current_species   # naming the output video-file (original)
        #                  + '_' + current_specimen[5:8] + '.avi')
        #
        file_to_write = ('BS_Flight_' + str(current_flight_nb) + '_' + 'cam3_M.' + current_species   # naming the output video-file (BS)
                         + '_' + current_specimen[5:8] + '.avi')

        video = cv2.VideoWriter(str(file_to_write), fourcc, 240, size)                       # open-cv recording function

        fgbg = cv2.createBackgroundSubtractorMOG2()                                          # MOG2 function

        start = int(vars()['S'+ str(s)][v]) + offset_3[v]                                    # start-frame-nb considering offset CAM3
        stop = int(start + (7*240))                                                          # stop-frame-nb (7sec later by default)

        f = 1
        while True:                                                                          # start video loop
            ret, frame = cap.read()
            tot_frame = int(cap.get(7))
            f += 1                                                                           # frame passing
            if f % 100 == 0:                                                                 # printing frequency
                print('filename:', cam3[v], '[cam3]', '  ',                                  # printing information
                      'Morpho', species[v], specimen_ID[v], '  ',
                      'Flight n°', current_flight_nb, '  ',
                      'frame n°', f, '  ',
                      'next flight in', int((start - f) / 14400), 'min',
                      int((start - f) / 240) - (int((start - f) / 14400) * 60), 'sec', '   ',
                      'Global progress:', round(flight_count * 100 / (sum(all_flight_nb)), 2), '%')

            fgmask = fgbg.apply(frame)                                                       # applying subtraction

            if f > start:
                cv2.imshow(str('Recording: ' + file_to_write), frame)                          # display original frame from start-f-n
                # video.write(frame) # SAVE ORIGINAL VERSION
                video.write(fgmask) #  SAVE SUBTRACTED VERSION
                cv2.imshow('subtracted', fgmask)                                             # display subtracted frame from start-f-n
                cv2.waitKey(4)
            if f == tot_frame:
                break
            if f > stop:                                                                       # stop from stop-f-n
                break
        cap.release()
        video.release()
        cv2.destroyAllWindows()
        flight_count += 1
    os.chdir(working_dir)                                                                      # leaving specimen folder
















































################################# CAMERA 1 - Cutting/Synchronizing/Subtracting Background #################################################
#################################               outputs automatically stored              #################################################

os.chdir(working_dir)
def createFolder(dir):                                                            # function to create folder
    try:                                                                          # receiving output videos
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print ('Error: Creating directory. ' +  dir)

flight_count = 1
for v in range(0,len(cam1)):   # start from the first specimen when v = 0
    current_date = str(df.iloc[v, 1])                                             # loading date
    current_videofile = str(cam1[v])                                              # loading video-file name
    current_species = species[v]                                                  # loading species name
    current_specimen = specimen_ID[v]                                             # loading specimen index

    all_flight_nb = []                                                            # Calculating numbers of
    for k in range(0, len(cam1)):                                                 # flights for all specimens
        for j in range(df.columns.get_loc("S1"), df.columns.get_loc("S18")):
            if math.isnan(df.iloc[k, j]):
                break
            val = (j + 1) - df.columns.get_loc("S1")
        all_flight_nb.append(val)

    working_dir = ('C:/Users/H. GOMES RODRIGUES/PycharmProjects/flight_sequences_processing')# setting current wd
    createFolder('./Flights_' + current_specimen + '_M.' + current_species + '/')            # creating specimen folderE2Y
    path_to_write = ('./Flights_' + current_specimen + '_M.' + current_species + '/')        # giving path to that folder
    os.chdir(path_to_write)                                                                  # entering into that folder

    for s in range(1,18): # start from the first flight when s = 1
        if math.isnan(vars()['S' + str(s)][v]):                                              # checking for sequence availability
            break

        cap = cv2.VideoCapture('D:/Gopro_Sequences_LOCAL/PERU_2017/GOPRO Sequences 2017/' +  # path to get raw video
                               current_date + '/' + 'cam1/' + current_videofile + '.mp4')

        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),                                      # defining frame size
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        # fourcc = cv2.VideoWriter_fourcc(*'a\0\0\0')                                             # MP4 codec
        # fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')                                     # AVI codec 1
        fourcc = cv2.VideoWriter_fourcc(*"DIB ")                                              # AVI codec 2 (heavy outputs but it always works !)

        if v == 0:
            current_flight_nb = str(s)
        else:
            current_flight_nb = str(s)
            if specimen_ID[v] == specimen_ID[v - 1]:
                current_flight_nb = all_flight_nb[v - 1] + s
                if specimen_ID[v] == specimen_ID[v - 2]:
                    current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + s
                    if specimen_ID[v] == specimen_ID[v - 3]:
                        current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + all_flight_nb[v - 3] + s
                        if specimen_ID[v] == specimen_ID[v - 4]:
                            current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + all_flight_nb[v - 3] + \
                                                all_flight_nb[v - 4] + s

        file_to_write = ('Flight_' + str(current_flight_nb) + '_' + 'cam1_M.' + current_species   # naming the output video-file (original)
                         + '_' + current_specimen[5:8] + '.avi')

        # file_to_write = ('BS_Flight_' + str(current_flight_nb) + '_' + 'cam1_M.' + current_species   # naming the output video-file (BS)
        #                  + '_' + current_specimen[5:8] + '.avi')

        video = cv2.VideoWriter(str(file_to_write), fourcc, 240, size)                       # open-cv recording function

        fgbg = cv2.createBackgroundSubtractorMOG2()                                          # MOG2 function

        start = int(vars()['S'+ str(s)][v])                                                  # start-frame-nb
        stop = int(start + (7*240))                                                          # stop-frame-nb (7sec later by default)

        f = 1
        while True:                                                                          # start video loop
            ret, frame = cap.read()
            tot_frame = int(cap.get(7))
            f += 1                                                                           # frame passing
            if f%100 == 0:                                                                   # printing frequency
                print('filename:', cam1[v],'[cam1]', '  ',                                   # text printed
                      'Morpho',species[v], specimen_ID[v],'  ',
                      'Flight n°',current_flight_nb,'  ',
                      'frame n°', f,'  ',
                      'next flight in', int((start-f)/14400),'min',
                      int((start-f)/240) - (int((start-f)/14400)*60),'sec','   ',
                      'Global progress:', round(flight_count*100/(sum(all_flight_nb)),2),'%')

            fgmask = fgbg.apply(frame)                                                       # applying subtraction

            if f > start:
                cv2.imshow(str('Recording: '+ file_to_write), frame)                         # display original frame from start-f-n
                video.write(frame) # SAVE ORIGINAL VERSION
                # video.write(fgmask) #  SAVE SUBTRACTED VERSION
                cv2.imshow('subtracted', fgmask)                                             # display subtracted frame from start-f-n
                cv2.waitKey(4)
            if f == tot_frame:
                break
            if f > stop:                                                                     # stop from stop-f-n
                break
        cap.release()
        video.release()
        cv2.destroyAllWindows()
        flight_count += 1
    os.chdir(working_dir)                                                                    # leaving specimen folder



################################# CAMERA 2 - Cutting/Synchronizing/Subtracting Background #################################################
#################################               outputs automatically stored              #################################################

os.chdir(working_dir)
def createFolder(dir):                                                            # function to create folder
    try:                                                                          # receiving output videos
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print ('Error: Creating directory. ' +  dir)

flight_count = 1
for v in range(0,len(cam2)):   # start from the first specimen when v = 0
    current_date = str(df.iloc[v, 1])                                             # loading date
    current_videofile = str(cam2[v])                                              # loading video-file name
    current_species = species[v]                                                  # loading species name
    current_specimen = specimen_ID[v]                                             # loading specimen index

    all_flight_nb = []                                                            # Calculating numbers of
    for k in range(0, len(cam2)):                                                 # flights for all specimens
        for j in range(df.columns.get_loc("S1"), df.columns.get_loc("S18")):
            if math.isnan(df.iloc[k, j]):
                break
            val = (j + 1) - df.columns.get_loc("S1")
        all_flight_nb.append(val)

    working_dir = ('C:/Users/H. GOMES RODRIGUES/PycharmProjects/flight_sequences_processing')# setting current wd
    createFolder('./Flights_' + current_specimen + '_M.' + current_species + '/')            # creating specimen folder
    path_to_write = ('./Flights_' + current_specimen + '_M.' + current_species + '/')        # giving path to that folder
    os.chdir(path_to_write)                                                                  # entering into that folder

    for s in range(1,18): # start from the first flight when s = 1
        if math.isnan(vars()['S' + str(s)][v]):                                              # checking for sequence availability
            break

        cap = cv2.VideoCapture('D:/Gopro_Sequences_LOCAL/PERU_2017/GOPRO Sequences 2017/' +  # path to get raw video
                               current_date + '/' + 'cam2/' + current_videofile + '.mp4')

        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),                                      # defining frame size
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        # fourcc = cv2.VideoWriter_fourcc(*'a\0\0\0')                                             # MP4 codec
        # fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')  # AVI codec 1                      # AVI codec 1
        fourcc = cv2.VideoWriter_fourcc(*"DIB ")                                              # AVI codec 2 (heavy outputs but it always works !)

        if v == 0:
            current_flight_nb = str(s)
        else:
            current_flight_nb = str(s)
            if specimen_ID[v] == specimen_ID[v - 1]:
                current_flight_nb = all_flight_nb[v - 1] + s
                if specimen_ID[v] == specimen_ID[v - 2]:
                    current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + s
                    if specimen_ID[v] == specimen_ID[v - 3]:
                        current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + all_flight_nb[v - 3] + s
                        if specimen_ID[v] == specimen_ID[v - 4]:
                            current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + all_flight_nb[v - 3] + \
                                                all_flight_nb[v - 4] + s

        file_to_write = ('Flight_' + str(current_flight_nb) + '_' + 'cam2_M.' + current_species   # naming the output video-file (original)
                         + '_' + current_specimen[5:8] + '.avi')

        # file_to_write = ('BS_Flight_' + str(current_flight_nb) + '_' + 'cam2_M.' + current_species   # naming the output video-file (BS)
        #                  + '_' + current_specimen[5:8] + '.avi')

        video = cv2.VideoWriter(str(file_to_write), fourcc, 240, size)                       # open-cv recording function

        fgbg = cv2.createBackgroundSubtractorMOG2()                                          # MOG2 function

        start = int(vars()['S'+ str(s)][v]) + offset_2[v]                                    # start-frame-nb considering offset CAM2
        stop = int(start + (7*240))                                                          # stop-frame-nb (7sec later by default)

        f = 1
        while True:                                                                          # start video loop
            ret, frame = cap.read()
            tot_frame = int(cap.get(7))
            f += 1                                                                           # frame passing
            if f % 100 == 0:                                                                 # printing frequency
                print('filename:', cam2[v], '[cam2]', '  ',                                  # printing information
                      'Morpho', species[v], specimen_ID[v], '  ',
                      'Flight n°', current_flight_nb, '  ',
                      'frame n°', f, '  ',
                      'next flight in', int((start - f) / 14400), 'min',
                      int((start - f) / 240) - (int((start - f) / 14400) * 60), 'sec', '   ',
                      'Global progress:', round(flight_count * 100 / (sum(all_flight_nb)), 2), '%')

            fgmask = fgbg.apply(frame)                                                       # applying subtraction

            if f > start:
                cv2.imshow(str('Recording: ' + file_to_write), frame)                       # display original frame from start-f-n
                video.write(frame) # SAVE ORIGINAL VERSION
                # video.write(fgmask) #  SAVE SUBTRACTED VERSION
                cv2.imshow('subtracted', fgmask)                                             # display subtracted frame from start-f-n
                cv2.waitKey(4)
            if f == tot_frame:
                break
            if f > stop:                                                                    # stop from stop-f-n
                break
        cap.release()
        video.release()
        cv2.destroyAllWindows()
        flight_count += 1
    os.chdir(working_dir)                                                                   # leaving specimen folder





################################# CAMERA 3 - Cutting/Synchronizing/Subtracting Background #################################################
#################################               outputs automatically stored              #################################################

os.chdir(working_dir)
def createFolder(dir):                                                            # function to create folder
    try:                                                                          # receiving output videos
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print ('Error: Creating directory. ' +  dir)

flight_count = 1
for v in range(0,len(cam3)): # start from the first specimen when v = 0
    current_date = str(df.iloc[v, 1])                                             # loading date
    current_videofile = str(cam3[v])                                              # loading video-file name
    current_species = species[v]                                                  # loading species name
    current_specimen = specimen_ID[v]                                             # loading specimen index

    all_flight_nb = []                                                            # Calculating numbers of
    for k in range(0, len(cam3)):                                                 # flights for all specimens
        for j in range(df.columns.get_loc("S1"), df.columns.get_loc("S18")):
            if math.isnan(df.iloc[k, j]):
                break
            val = (j + 1) - df.columns.get_loc("S1")
        all_flight_nb.append(val)

    working_dir = ('C:/Users/H. GOMES RODRIGUES/PycharmProjects/flight_sequences_processing')# setting current wd
    createFolder('./Flights_' + current_specimen + '_M.' + current_species + '/')            # creating specimen folder
    path_to_write = ('./Flights_' + current_specimen + '_M.' + current_species + '/')        # giving path to that folder
    os.chdir(path_to_write)                                                                  # entering into that folder

    for s in range(1,18): # start from the first flight when s = 1
        if math.isnan(vars()['S' + str(s)][v]):                                              # checking for sequence availability
            break

        cap = cv2.VideoCapture('D:/Gopro_Sequences_LOCAL/PERU_2017/GOPRO Sequences 2017/' +  # path to get raw video
                               current_date + '/' + 'cam3/' + current_videofile + '.mp4')

        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),                                      # defining frame size
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        # fourcc = cv2.VideoWriter_fourcc(*'a\0\0\0')                                             # MP4 codec
        # fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')  # AVI codec 1                      # AVI codec 1
        fourcc = cv2.VideoWriter_fourcc(*"DIB ")                                              # AVI codec 2 (heavy outputs but it always works !)

        if v == 0:
            current_flight_nb = str(s)
        else:
            current_flight_nb = str(s)
            if specimen_ID[v] == specimen_ID[v - 1]:
                current_flight_nb = all_flight_nb[v - 1] + s
                if specimen_ID[v] == specimen_ID[v - 2]:
                    current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + s
                    if specimen_ID[v] == specimen_ID[v - 3]:
                        current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + all_flight_nb[v - 3] + s
                        if specimen_ID[v] == specimen_ID[v - 4]:
                            current_flight_nb = all_flight_nb[v - 1] + all_flight_nb[v - 2] + all_flight_nb[v - 3] + \
                                                all_flight_nb[v - 4] + s

        file_to_write = ('Flight_' + str(current_flight_nb) + '_' + 'cam3_M.' + current_species   # naming the output video-file (original)
                         + '_' + current_specimen[5:8] + '.avi')

        # file_to_write = ('BS_Flight_' + str(current_flight_nb) + '_' + 'cam3_M.' + current_species   # naming the output video-file (BS)
        #                  + '_' + current_specimen[5:8] + '.avi')

        video = cv2.VideoWriter(str(file_to_write), fourcc, 240, size)                       # open-cv recording function

        fgbg = cv2.createBackgroundSubtractorMOG2()                                          # MOG2 function

        start = int(vars()['S'+ str(s)][v]) + offset_3[v]                                    # start-frame-nb considering offset CAM3
        stop = int(start + (7*240))                                                          # stop-frame-nb (7sec later by default)

        f = 1
        while True:                                                                          # start video loop
            ret, frame = cap.read()
            tot_frame = int(cap.get(7))
            f += 1                                                                           # frame passing
            if f % 100 == 0:                                                                 # printing frequency
                print('filename:', cam3[v], '[cam3]', '  ',                                  # printing information
                      'Morpho', species[v], specimen_ID[v], '  ',
                      'Flight n°', current_flight_nb, '  ',
                      'frame n°', f, '  ',
                      'next flight in', int((start - f) / 14400), 'min',
                      int((start - f) / 240) - (int((start - f) / 14400) * 60), 'sec', '   ',
                      'Global progress:', round(flight_count * 100 / (sum(all_flight_nb)), 2), '%')

            fgmask = fgbg.apply(frame)                                                       # applying subtraction

            if f > start:
                cv2.imshow(str('Recording: ' + file_to_write), frame)                          # display original frame from start-f-n
                video.write(frame) # SAVE ORIGINAL VERSION
                # video.write(fgmask) #  SAVE SUBTRACTED VERSION
                cv2.imshow('subtracted', fgmask)                                             # display subtracted frame from start-f-n
                cv2.waitKey(4)
            if f == tot_frame:
                break
            if f > stop:                                                                       # stop from stop-f-n
                break
        cap.release()
        video.release()
        cv2.destroyAllWindows()
        flight_count += 1
    os.chdir(working_dir)                                                                      # leaving specimen folder













































