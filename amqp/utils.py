from sqlalchemy.orm.state import InstanceState
from datetime import datetime as dt
def serialize(dict):
    for k, v in dict.copy().items():
        if isinstance(v, dt):
            dict[k] = v.isoformat()
        elif isinstance(v, InstanceState):
            dict.pop(k)
    return dict