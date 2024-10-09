from biosiglive import (
    LivePlot, 
    #save , 
    PytrignoClient, 
    RealTimeProcessingMethod, 
    PlotType
    )

# Define the system from which you want to get the data.
interface = PytrignoClient(system_rate=100, ip="localhost")
n_electrodes = 4
raw_emg = None
muscle_names = [
    "Pectoralis major",
    "Deltoid anterior",
    "Deltoid medial",
    "Deltoid posterior"
]

# Add device to the interface
interface.add_device(
    nb_channels=n_electrodes,
    device_type="emg",
    name="emg",
    rate=2000,
    processing_method=RealTimeProcessingMethod.ProcessEmg,
    moving_average_window=600
)

# Add plots
emg_plot = LivePlot(
    name="emg",
    rate=100,
    plot_type=PlotType.Curve,
    nb_subplots=n_electrodes,
    channel_names=muscle_names
)

emg_plot.init(plot_windows=500, y_labels="Processed EMG (mV)")
emg_raw_plot = LivePlot(
    name="emg_raw",
    rate=100,
    plot_type=PlotType.Curve,
    nb_subplots=n_electrodes,
    channel_names=muscle_names
)
emg_raw_plot.init(plot_windows=10000, colors=(255, 0, 0), y_labels="EMG (mV)")
while True:
# Get data from Vicon interface and process it.
    raw_emg = interface.get_device_data(
        channel_idx=[4,5,6,7],
        device_name="emg")
    print(raw_emg)
    emg_proc = interface.devices[0].process()
    # Update plots.
    emg_plot.update(emg_proc[:, -1:])
    emg_raw_plot.update(raw_emg)
    # Add data to the binary file.
    #save({"raw_emg": raw_emg, "process_emg":emg_proc[:, -1]}, "emg.bio")