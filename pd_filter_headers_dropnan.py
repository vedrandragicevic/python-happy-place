import pandas
import boto3

session = boto3.Session()
s3_resource = session.resource('s3')
s3_client = boto3.client('s3')


def lambda_handler(event, context):
    # Download from S3 bucket
    # s3_client.download_file("bucket_name", "key", "tmp_filename")

    # Read from 'tmp_filename'
    main_df = pandas.read_csv('mock_data.csv')
    print(main_df.to_string())
    """
        MAIN DF PRINT:
                id first_name   last_name                      email       ip_address
            0    1      Alwyn       Aplin      aaplin0@earthlink.net   77.123.197.237
            1    2  Guinevere    Stealfox                        NaN  197.182.173.163
            2    3   Sashenka     O'Fairy         sofairy2@patch.com     57.144.11.85
            3    4   Alphonse    Prescote         aprescote3@free.fr   218.158.219.68
            4    5        NaN     Stimson        sstimson4@github.io    216.116.53.33
            5    6     Darice       Abdon        dabdon5@vinaora.com    229.44.70.153
            6    7     Dannye  Minichillo                        NaN     10.28.174.99
            7    8       Trev      Fanton         tfanton7@baidu.com   196.36.106.137
            8    9      Barbi         NaN       bburford8@weebly.com   246.48.169.207
            9   10    Gaylord     Cackett  gcackett9@dailymail.co.uk   219.124.141.97
            10  11      Carny   Swetenham    cswetenhama@twitpic.com              NaN
            11  12     Ambros    Nannetti                        NaN    41.27.123.117
    """

    # Checking for headers
    # headers = main_df.columns
    # print(headers)

    header_list = main_df.columns.values.tolist()
    print(header_list)
    """
        HEADERS LIST PRINT:
            ['id', 'first_name', 'last_name', 'email', 'ip_address']
    """

    # Check entire df for nan values, returns Boolean
    is_empty = main_df.isnull().values.all()
    print(is_empty)
    """
        BOOLEAN OUTPUT:
            False
    """

    # Drop rows that have nan
    filtered_df = main_df.dropna()
    print(filtered_df.to_string())
    """
       ONLY ROWS THAT HAVE VALUES:
           id first_name last_name                      email      ip_address
            0   1      Alwyn     Aplin      aaplin0@earthlink.net  77.123.197.237
            2   3   Sashenka   O'Fairy         sofairy2@patch.com    57.144.11.85
            3   4   Alphonse  Prescote         aprescote3@free.fr  218.158.219.68
            5   6     Darice     Abdon        dabdon5@vinaora.com   229.44.70.153
            7   8       Trev    Fanton         tfanton7@baidu.com  196.36.106.137
            9  10    Gaylord   Cackett  gcackett9@dailymail.co.uk  219.124.141.97
    """

    # Check if df is empty again
    is_empty_filtered = filtered_df.isnull().values.all()
    print(is_empty_filtered)
    """
        BOOLEAN OUTPUT:
            False
    """

    # Save df as csv file to lambda tmp storage
    filtered_df.to_csv("/tmp/file_name_new.csv", sep=',', index=False)


if __name__ == '__main__':
    lambda_handler("", "")
