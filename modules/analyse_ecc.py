import numpy as np
import pandas as pd
import pandas.util.testing as pdt

import modules.pd_utils as pd_utils

def extend_cam_id_ts(df):
    """Extend df with cam ids and timestamps.

    This function extracts information about the camera id and the timestamps of
    the first and last frame from the videonames (column curr_img_name
    and succ_img_name).
    >>> data = [('Cam_0_2016-07-19T12:41:22.353295Z--2016-07-19T12:47:02.199607Z.mkv',
    ...          'Cam_0_2016-07-19T12:41:22.353295Z--2016-07-19T12:47:02.199607Z.mkv')]
    >>> df = pd.DataFrame(data = data, columns=['curr_img_name', 'succ_img_name'])
    >>> df = extend_cam_id_ts(df)
    >>> df['curr_start_ts'].loc[0]
    Timestamp('2016-07-19 12:41:22.353295+0000', tz='<iso8601.Utc>')
    """
    curr_meta = df.apply(lambda row: pd_utils.extract_metadata_videoname(row['curr_img_name']), axis=1)
    curr_meta.columns = ['curr_cam_id', 'curr_start_ts', 'curr_end_ts']
    df = df.merge(curr_meta, left_index=True, right_index=True)
    succ_meta = df.apply(lambda row: pd_utils.extract_metadata_videoname(row['succ_img_name']), axis=1)
    succ_meta.columns = ['succ_cam_id', 'succ_start_ts', 'succ_end_ts']
    df = df.merge(succ_meta, left_index=True, right_index=True)
    return df


def extend_distance(df):
    """Extend df with distance.

    >>> data = [('A', '[[1,0,3],[1,0,4]]')]
    >>> df = pd.DataFrame(data=data, columns=['foo', 'warp_matrix'])
    >>> extend_distance(df)
    >>> df['distance'].loc[0]
    5.0
    """
    def get_distance(row):
        if pd.isnull(row['warp_matrix']):
            return np.NaN
        else:
            return np.linalg.norm(pd_utils.str_to_numpy(row['warp_matrix'])[:, 2])
    df['distance'] = df.apply(lambda row: get_distance(row), axis=1)


# %%
def load_ecc_csv_to_pd(path):
    """Load the data from the csv file to a pandas df."""
    names = ['id', 'curr_img_name', 'succ_img_name', 'cc', 'warp_matrix']
    df = pd.read_csv(path, sep=';', names=names, index_col=0)
    return df
# %%


def load_and_prepare(path):
    """Load data from ecc csv file and prepare it for further analysis."""
    df = load_ecc_csv_to_pd(path)
    df = extend_cam_id_ts(df)
    extend_distance(df)
    return df


def get_intervalls(path, accuracy):
    df = load_and_prepare(path)

    pdt.assert_series_equal(df['succ_cam_id'], df['curr_cam_id'], check_names=False)

    df_prep = df.drop(['warp_matrix', 'cc', 'succ_cam_id'], axis=1)

    shifted = df[['curr_img_name', 'curr_start_ts', 'curr_end_ts']].shift(1)
    shifted.columns = ['pred_img_name', 'pred_start_ts', 'pred_end_ts']

    df_ext = df_prep.merge(shifted, left_index=True, right_index=True)

    # `df_prep['distance']` beschreibt die Bewegung welche von `curr_start` zu `succ_start` stattgefunden hat.

    shifted = df[['curr_img_name', 'curr_start_ts', 'curr_end_ts']].shift(1)
    shifted.columns = ['pred_img_name', 'pred_start_ts', 'pred_end_ts']

    df_ext = df_prep.merge(shifted, left_index=True, right_index=True)

    df_selection = df_ext[(df_ext['distance'] > accuracy)]

    df_ext = df_prep.merge(shifted, left_index=True, right_index=True)

    # calculate all intervals
    intervalle = []
    excluded = []
    start = None
    for i, (index, row) in enumerate(df_selection.iterrows()):

        # first intervall begins with first video in year
        if i == 0:

            # start with the first video in year
            start = df_ext.loc[0]['curr_img_name']
            end = df_ext.loc[index]['pred_img_name']
            intervalle.append((start, end))

            excluded.append(df_ext.loc[index]['curr_img_name'])

            start = df_ext.loc[index]['succ_img_name']

        else:
            if (index - 1) not in df_selection.index.values:
                end = df_ext.loc[index]['pred_img_name']
                intervalle.append((start, end))

            excluded.append(df_ext.loc[index]['curr_img_name'])

            start = df_ext.loc[index]['succ_img_name']

            if i == len(df_selection) - 1:
                end = df_ext.loc[max(df_ext.index.values)]['succ_img_name']
                intervalle.append((start, end))
    return intervalle, excluded
