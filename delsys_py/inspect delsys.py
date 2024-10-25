# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 12:47:23 2024

@author: Lab412
"""

from libemg.streamers import delsys_streamer
from libemg.data_handler import OnlineDataHandler

if __name__ == "__main__":
    streamer, sm = delsys_streamer(emg_port = 50043, 
                                   aux_port = 50044, 
                                   imu = True,
                                   channel_list=[0,2,3])
    odh = OnlineDataHandler(sm)
    #odh.analyze_hardware()
    # odh.visualize_channels([0,1], 500)
    odh.visualize()
    
