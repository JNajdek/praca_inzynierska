import os
from pathlib import Path
from dotenv import get_key
from numpy.ma.core import shape

from build.lib.libemg.data_handler import RegexFilter
from build.lib.libemg.feature_extractor import FeatureExtractor
from libemg.streamers import delsys_streamer
from libemg.data_handler import OnlineDataHandler, OfflineDataHandler
import numpy as np
if __name__ == "__main__":
    streamer, sm = delsys_streamer(emg_port = 50043,
                                   aux_port = 50044,
                                   imu = False,
                                   emg = True,
                                   channel_list=[0,1,2,3])
    odh = OnlineDataHandler(sm)
    # odh.analyze_hardware()
    # odh.visualize_channels([0,7], 500)
    #odh.visualize()
    odh.visualize_heatmap(feature_list=['MEAN','MNF',
                        'MNP',
                        'MPK'
                         ])








    # #tylko dla emg
    # regex_filters=[]
    # regex_filters.append(RegexFilter(left_bound='/', right_bound="emg.csv", values=['_'], description='emg'))
    # ofdh = OfflineDataHandler()
    #
    # #current_dir = os.path.dirname(os.path.abspath(__file__))
    # # path = '../data_records'
    # # normalized_path = os.path.abspath(path)
    # # if os.path.isabs(normalized_path):
    # #
    # #     output_dir_path = normalized_path
    # # else:
    # #
    # #     exit()
    # # # Utwórz pełną ścieżkę do katalogu "data_records"
    # # folder = os.path.join(output_dir_path, 'recorded_data_2025-03-25_11-28-41')
    #
    # folder = get_key( str(Path("../.env")), "LAST_TARGET_FOLDER")
    # print(folder)
    # folder = os.path.normpath(folder)
    #
    # ofdh.get_data(folder, regex_filters, delimiter=' ')
    # ofdh_new = ofdh.isolate_channels([2])
    # windows, _ = ofdh_new.parse_windows(1,1)
    # fe = FeatureExtractor()
    # feature_set_dict = fe.extract_features(['MEAN'], windows)
    # fe.visualize(feature_set_dict)
