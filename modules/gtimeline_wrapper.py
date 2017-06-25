


def create_gtimeline_dict(df, row_label, bar_label, start, end, tooltip):
    """Create dict from dataframe to use with google timeline.

    After create dict you can convert it to json and used it for google timeline.

    Args:
        df (pandas.DataFrame): pandas dataframe which contains the following columns.
        row_label (str): columns name of `df` to use for row_label.
        bar_label (str): columns name of `df` to use for bar_label.
        start (str): columns name of column which contains start timestamp (type:timestamp)  of an interval.
        end (str): columns name of column which contains end timestamp (type:timestampt) of an interval.
        tooltip (str): columns name of column which contains a short description.
    """
    def create_date_str(ts):
        string = 'Date({Y}, {M}, {D}, {h}, {m}, {s}, {ms})'.format(
            Y=ts.year,
            # Important: When using this Date String Represenation,
            # as when using the new Date() constructor, months are
            # indexed starting at zero (January is month 0, December is month 11).
            M=ts.month - 1,
            D=ts.day,
            h=ts.hour,
            m=ts.minute,
            s=ts.second,
            ms=str(ts.microsecond)[:3])
        return string

    def create_header(row_label, bar_label, start_label, end_label):
        heading = [
            {"type": "string", "id": row_label},
            {"type": "string", "id": bar_label},
            {"type": "string", "role": "tooltip", "p":
                {"html": "true"}
             },
            {"type": "date", "id": start_label},
            {"type": "date", "id": end_label}
        ]
        return heading

    def create_row(row_label, bar_label, tooltip, start_ts, end_ts):
        start_ts_str = create_date_str(start_ts)
        end_ts_str = create_date_str(end_ts)
        row = {"c": [
            {"v": str(row_label)},
            {"v": str(bar_label)},
            {"v": tooltip},
            {"v": start_ts_str},
            {"v": end_ts_str}
        ]}
        return row

    # initialize base structure
    data = dict(cols=None, rows=[])
    data['cols'] = create_header('cam_id', 'interval_id', 'start_time', 'end_time')
    for i, row in enumerate(df.iterrows()):
        row = row[1]
        row_to_ins = create_row(str(row[row_label]), str(
            row[bar_label]), row[tooltip], row[start], row[end])
        data['rows'].append(row_to_ins)

    return data
