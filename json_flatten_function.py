import pandas as pd
import json


def flatten_json(nested_json, exclude=['']):
    """Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
            exclude: Keys to exclude from output.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name='', exclude=exclude):
        if type(x) is dict:
            for a in x:
                if a not in exclude: flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out


if __name__ == '__main__':
    this_dict = {'events': [
      {'id': 142896214,
       'playerId': 37831,
       'teamId': 3157,
       'matchId': 2214569,
       'matchPeriod': '1H',
       'eventSec': 0.8935539999999946,
       'eventId': 8,
       'eventName': 'Pass',
       'subEventId': 85,
       'subEventName': 'Simple pass',
       'positions': [{'x': 51, 'y': 49}, {'x': 40, 'y': 53}],
       'tags': [{'id': 1801, 'tag': {'label': 'accurate'}}]},
     {'id': 142896214,
       'playerId': 37831,
       'teamId': 3157,
       'matchId': 2214569,
       'matchPeriod': '1H',
       'eventSec': 0.8935539999999946,
       'eventId': 8,
       'eventName': 'Pass',
       'subEventId': 85,
       'subEventName': 'Simple pass',
       'positions': [{'x': 51, 'y': 49}, {'x': 40, 'y': 53},{'x': 51, 'y': 49}],
       'tags': [{'id': 1801, 'tag': {'label': 'accurate'}}]}
    ]}

    new_df = pd.DataFrame([flatten_json(x) for x in this_dict['events']])

    with open('test.json', 'w') as f:
        f.write(new_df.to_json(orient='records', lines=True))
