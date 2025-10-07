# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 15:37:40 2025
- Explore EEG dataset
@author: Rahul
"""

#%% Load libraries
import os
import mne
from tkinter.filedialog import askopenfilename

#%%
eeg_filename = askopenfilename(title = "Select file",
                              filetypes = (
                                  ("SET file","*.set*"),
                                  ("EDF file","*.edf"),
                                  ("BrainAnalyser file","*.vhdr*")
                                  ))
datadir,_ = os.path.split(eeg_filename)
os.chdir(datadir)

# Load EEG data
if eeg_filename.find('.edf')>0:
    eeg_data = mne.io.read_raw_edf(eeg_filename, preload=True)
elif eeg_filename.find('.set')>0:
    eeg_data = mne.io.read_raw_eeglab(eeg_filename, preload=True)
elif eeg_filename.find('.vhdr')>0:
    eeg_data = mne.io.read_raw_brainvision(eeg_filename, preload=True)

# Get EEG info
srate       = eeg_data.info.get('sfreq')
times       = eeg_data.times
chanlist    = eeg_data.info.get('ch_names')

all_eeg_channels = ['Pz']

# select only EEG channels
eeg_data.pick_channels(all_eeg_channels)

eeg_data.filter(1.,None,fir_design='firwin').load_data()
eeg_data.filter(None,40,fir_design='firwin').load_data()

eeg_data.plot()

# Get the events
events = mne.events_from_annotations(eeg_data)

tmin, tmax = -2.2,0.3
baseline = (None, 0.0)

epochs_correct = mne.Epochs(eeg_data,
                            events = events[0],
                            event_id=11, 
                            tmin=tmin,tmax=tmax, 
                            baseline=baseline)

epochs_incorrect = mne.Epochs(eeg_data,
                              events = events[0],
                              event_id=12, 
                              tmin=tmin,tmax=tmax,
                              baseline=baseline)