
from django.db import transaction, connections

def run_query(query, args=None):
    default_conn = connections['default']
    with default_conn.cursor() as cur:
        if args:
            cur.execute(query, args)
        else:
            cur.execute(query)
        return cur.fetchall()