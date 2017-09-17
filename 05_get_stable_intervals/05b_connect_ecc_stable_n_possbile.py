import copy
import json
import os


def set_new_id(interval, new_id):
    """Set new id for the interval and save the old id."""
    interval['old_ids'] = [interval['id']]
    interval['id'] = new_id


def connect_intervals(json_intervals):
    """Connect 'ecc stable and 'ecc possible movement' intervals.

    Gets a list of intervals and returns a list of list intervals,
    where consecutive intervals of type 'ecc stable' and 'ecc possible movement'
    will be joined, if both of them are stable.
    """
    connected_intervals = []
    for i, interval in enumerate(json_intervals):
        curr_interval = copy.deepcopy(interval)

        if curr_interval["info"] == 'ecc stable':
            ecc_stable_interval = curr_interval

        elif curr_interval["info"] == 'ecc possible movement':
            assert ecc_stable_interval['id'] == curr_interval['id'] - 1

            # both intervals not moved
            if ecc_stable_interval['stable'] and curr_interval['stable']:
                curr_interval['start_video_name'] = ecc_stable_interval['start_video_name']
                curr_interval['first_frame'] = ecc_stable_interval['first_frame']
                curr_interval['info'] = 'manuell connected'
                curr_interval['old_ids'] = [ecc_stable_interval['id'], curr_interval['id']]
                curr_interval['id'] = len(connected_intervals)

                connected_intervals.append(curr_interval)

            else:
                # save old id and set new id
                set_new_id(ecc_stable_interval, len(connected_intervals))
                connected_intervals.append(ecc_stable_interval)

                set_new_id(curr_interval, len(connected_intervals))
                connected_intervals.append(curr_interval)

        else:
            set_new_id(curr_interval, len(connected_intervals))
            connected_intervals.append(curr_interval)

    return connected_intervals


for cam_id in range(4):
    path = "05a_Cam_{CAM_ID}_intervals_ecc_stable.json".format(CAM_ID=cam_id)
    with open(path, 'r') as jsonfile:
        json_intervals = json.load(jsonfile)
        connected_intervals = connect_intervals(json_intervals)

        basename_json = os.path.splitext(os.path.basename(path))[0]
        output_path = '05b_{basename}_join.json'.format(basename=basename_json[4:])

        with open(output_path, 'w') as fp:
                json.dump(connected_intervals, fp)
        print('File was saved to {output_path}'.format(output_path=output_path))

        with open(os.path.join('../docs', output_path), 'w') as fp:
            json.dump(connected_intervals, fp)
