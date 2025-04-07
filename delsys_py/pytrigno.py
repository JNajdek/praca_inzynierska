def transform_channels_for_imu(active_sensors):
    channels = []
    for sensor in active_sensors:
        start_channel = (sensor - 1) * 9 + 1
        channels.extend(range(start_channel, start_channel + 9))

    group_map = {
        1: [0, 1, 2],
        2: [3, 4, 5],
        3: [6, 7, 8]
    }
    allowed_channels = set(channels)
    checked = [2]

    for group_id, blocked_positions in group_map.items():
        if group_id not in checked:
            allowed_channels &= {
                ch for ch in channels
                if (ch - 1) % 9 not in blocked_positions
            }
    return list(allowed_channels)

print(transform_channels_for_imu([1,3]))