from datetime import datetime
import json
from typing import Dict, List, Any

def transforming_json(json_data:List[Dict[str,Any]])-> json:
    for item in json_data:
        item['price'] = item['price'][:-2] + '.' + item['price'][-2:]
        item['end_date'] = datetime.fromtimestamp(int(item['end_date'])).strftime('%Y-%m-%d')
        item['start_date'] = datetime.fromtimestamp(int(item['start_date'])).strftime('%Y-%m-%d')
        item['release_date'] = datetime.fromtimestamp(int(item['release_date'])).strftime('%Y-%m-%d')

    return json.dumps(json_data)