import re
from typing import Any, Dict, List, Tuple

# Pyformat to psql format.
def build_query_by_args(
    query: str, params: Dict[str, Any], **rest: object
) -> Tuple[str, List[Any]]:
    query = query.format(**rest)

    # Generate query with serial positions.
    params_formatted = []
    for idx, key in enumerate(params.keys()):
        params_formatted.append(params[key])
        query = re.sub(f":{key}", f"${idx+1}", query)

    return query, params_formatted
