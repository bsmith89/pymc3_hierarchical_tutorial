#!/usr/bin/env python3

import json
import sys

if __name__ == '__main__':
    nb = json.load(sys.stdin)
    for cell in nb['cells']:
        if 'outputs' in cell:
            cell['outputs'] = []
        if 'execution_count' in cell:
            cell['execution_count'] = None
        if 'output_type' in cell:
            del cell['output_type']
        cell['metadata'] = {}

    json.dump(nb, sys.stdout, sort_keys=True, indent=1)
