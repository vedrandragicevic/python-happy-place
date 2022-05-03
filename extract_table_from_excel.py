import pandas
from skimage.measure import label, regionprops
import numpy as np


def lambda_handler(event, context):
    """
    DEPENDENCIES:
        - pandas
        - numpy
        - scikit-image
        - xlrd

    EXTRACTS A TABLE FROM THE EXCEL FILE PROVIDED IN THE REPOSITORY.
    LOADS ENTIRE FILE INTO A PANDAS DF. CREATES A BINARY MATRIX FROM THAT DF.
    EVERY CELL IN THE DF WHICH CONTAINS VALUE IS CONSIDERED AS 1 AND OTHERS AS 0.
    CREATES A IMAGE FROM THAT REGION THAT HAS 1s IN THE MATRIX.
    CREATES A DATAFRAME FROM THAT REGION.
    """
    print(event)

    with open('example_messed_up.xls', mode='rb') as file:
        df = pandas.read_excel(file, header=None)

    binary_rep = np.array(df.notnull().astype('int'))

    list_of_dataframes = []
    # Label connected regions of an integer array
    l = label(binary_rep)
    # Measure properties of labeled image regions
    for s in regionprops(l):
        # the bbox contains the extremes of the bounding box
        # So the top left and bottom right cell locations of the table
        list_of_dataframes.append(df.iloc[s.bbox[0]:s.bbox[2], s.bbox[1]:s.bbox[3]])

    print(list_of_dataframes[0].to_string())


if __name__ == '__main__':
    lambda_handler('', '')
