import requests


def get_request(url, headers):
    response = requests.get(url, headers=headers)
    response = response.json()
    return response


def get_all_plates_barcodes(url, plates_url, headers, instrument_location_id, logger):
    """
    Get container information of all containers in a list of container barcodes
    :param url:                  API url to fetch container information based on barcode
    :param plates_url:           Get Plates URL
    :param headers:              Headers for API call
    :param instrument_location_id:   Instrument benchling location ID
    :param logger:   Variable for printing outputs
    :return yield plate barcodes: Generator
    """
    token_exists = True
    while token_exists:
        plates_response = get_request(url, headers)

        if plates_response.get('error'):
            return []

        for plate in plates_response.get('plates'):
            yield plate.get('barcode')

        next_token = plates_response.get('nextToken')
        if next_token != '':
            url = f"{plates_url}?pageSize=100&nextToken={next_token}&ancestorStorageId={instrument_location_id}&returning=plates.barcode%2CnextToken"
        else:
            token_exists = False
            logger.info(f"FETCHED ALL PLATES FROM BENCHLING THAT ARE STORED IN THE RACCER!")


if __name__ == '__main__':
    # FETCHING ALL PLATE IDS FROM BENCHLING THAT ARE STORED IN THE RACCER ASSET ID
    get_plate_url = f"GET PLATE URL"
    instrument_location_id = "TEST_INSTRUMENT"
    get_plate_by_location_url = f"{get_plate_url}?pageSize=100&ancestorStorageId={instrument_location_id}&returning=plates.barcode%2CnextToken"

    all_plates_barcodes_list_generator = get_all_plates_barcodes(url=get_plate_by_location_url,
                                                                 plates_url=get_plate_url, headers=headers,
                                                                 instrument_location_id=instrument_location_id, logger=logger)
    all_plates_barcodes_benchling_list = [item for item in all_plates_barcodes_list_generator]