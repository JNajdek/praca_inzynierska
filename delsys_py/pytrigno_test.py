"""
Tests communication with and data acquisition from a Delsys Trigno wireless
EMG system. Delsys Trigno Control Utility needs to be installed and running,
and the device needs to be plugged in. Tests can be run with a device connected
to a remote machine if needed.

The tests run by this script are very simple and are by no means exhaustive. It
just sets different numbers of channels and ensures the data received is the
correct shape.

Use `-h` or `--help` for options.
"""
import matplotlib.pyplot as plt
import argparse


fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot([], [], 'r-') # Returns a tuple of line objects, thus the comma

try:
    import pytrigno
except ImportError:
    import sys
    sys.path.insert(0, '..')
    import pytrigno


def check_emg(host):
    dev = pytrigno.TrignoEMG(channel_range=(0, 1), samples_per_read=270,
                             host=host)

    # test single-channel
    dev.start()
    for i in range(2):
        data = dev.read()
        print("single emg")
        print(data)
        # line1.set_ydata(data[[0]])
        # fig.canvas.draw()
        # fig.canvas.flush_events()
#        assert data.shape == (1, 270)
    dev.stop()

    # test multi-channel
    dev.set_channel_range((0, 7))
    dev.start()
    for i in range(4):
        data = dev.read()
        print("multi emg")
        print(data)
  #      assert data.shape == (5, 270)
    dev.stop()


def check_accel(host):
    dev = pytrigno.TrignoAccel(channel_range=(0, 7), samples_per_read=10,
                               host=host)

    dev.start()
    for i in range(4):
        data = dev.read()
        print("single acc")
        print(data)
 #       assert data.shape == (3, 10)
    dev.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-a', '--addr',
        dest='host',
        default='localhost',
        help="IP address of the machine running TCU. Default is localhost.")
    args = parser.parse_args()
    

    check_emg(args.host)
    check_accel(args.host)