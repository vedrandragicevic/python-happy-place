import pandas as pd


def main():
    df1 = pd.DataFrame(
        {"Tube_name": ["A02352", "A2352351", "A232523"],
            "Tube_surname": ["B05215", "B132532", "B223523"],
            "Tube_nickname": ["C2352350", "C123525", "C2325"]}, index=None)

    df4 = pd.DataFrame(
        {"TubeRack_name": ["B2"],
            "TubeRack_surname": ["C2"],
            "TubeRack_nickname": ["D2"]}, index=None)

    print(df1)
    """
    OUTPUT: 
        Tube_name Tube_surname Tube_nickname
    0    A02352       B05215      C2352350
    1  A2352351      B132532       C123525
    2   A232523      B223523         C2325
    """
    print(df4)
    """
    OUTPUT: 
        TubeRack_name TubeRack_surname TubeRack_nickname
    0            B2               C2                D2
    """
    # header_list_df4 = df4.columns.values.tolist()
    # header_list_df1 = df1.columns.values.tolist()

    header_list_df4 = list()
    header_list_df1 = list()
    for col in df4.columns:
        header_list_df4.append(col)

    for col in df1.columns:
        header_list_df1.append(col)

    header_merged = list()
    header_merged.extend(header_list_df1)
    header_merged.extend(header_list_df4)
    print("MERGED HEADER LIST: ", header_merged)

    """
    OUTPUT:
    MERGED HEADER LIST:  ['Tube_name', 'Tube_surname', 'Tube_nickname', 'TubeRack_name', 'TubeRack_surname', 'TubeRack_nickname']
    """

    result = pd.DataFrame(data=[], index=None, columns=header_merged)

    for index, column_value in df4.iterrows():
        for column, value in df1.iterrows():
            content_list = list()
            content_list.extend(value)
            content_list.extend(column_value)
            print("CONTENT LIST: ", content_list)

            result = result.append(pd.DataFrame([content_list], columns=header_merged), ignore_index=True)

    print(result.to_string())
    """
    OUTPUT:
        Tube_name Tube_surname Tube_nickname TubeRack_name TubeRack_surname TubeRack_nickname
    0    A02352       B05215      C2352350            B2               C2                D2
    1  A2352351      B132532       C123525            B2               C2                D2
    2   A232523      B223523         C2325            B2               C2                D2
    """


if __name__ == '__main__':
    main()
