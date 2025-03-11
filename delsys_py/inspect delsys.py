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
                                   imu = False,
                                   emg = True,
                                   channel_list=[0,1,2,3,4,5])
    odh = OnlineDataHandler(sm)
    #odh.analyze_hardware()
    #odh.visualize_channels([0,7], 500)
    #odh.visualize()
    odh.visualize_heatmap(feature_list=['MAV',
                        'ZC',
                        'SSC',
                        'WL',
                        'LS'])
    
