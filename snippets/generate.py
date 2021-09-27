from typing import Any, Dict, List, Tuple
import yaml
import json
import os

def transform(snippet: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    snippet_id = snippet['name'][0]
    return (
        snippet_id,
        {
            'scope': 'markdown',
            'prefix': sum(map(lambda name: [name, '\\' + name], snippet['name']), []),
            'body': snippet['body'],
        }
    )

def main():
    with open(os.path.join(
        os.path.dirname(__file__),
        'snippets.yml',
    )) as f:
        data: List[Dict[str, Any]] = yaml.safe_load(f)

    snippets = list(map(transform, data))
    result = dict(snippets)

    if len(snippets) > len(result):
        raise ValueError('Duplicate snippet names')

    with open(os.path.join(
        os.path.dirname(__file__),
        '..',
        '.vscode',
        'generated.code-snippets'
    ), 'w') as f:
        json.dump(result, f, indent=2)

if __name__ == '__main__':
    main()
