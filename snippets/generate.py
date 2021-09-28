from typing import Any, Dict, List, Optional, Tuple
import functools
import yaml
import json
import os
from collections import Counter

InputSnippet = Dict[str, Any]
OutputSnippet = Tuple[str, Dict[str, Any]]

def transform_snippet(category: Optional[str], snippet: InputSnippet) -> OutputSnippet:
    snippet_id = f"{snippet['name'][0]}{'' if category is None else f' ({category})'}"
    return (
        snippet_id,
        {
            'scope': 'markdown',
            'prefix': sum(map(lambda name: [name, '\\' + name], snippet['name']), []),
            'body': snippet['body'],
        }
    )

def transform_category(category: Dict[str, Any]) -> List[OutputSnippet]:
    category_id: Optional[str] = category['category']
    snippets: List[InputSnippet] = category['snippets']
    return list(map(functools.partial(transform_snippet, category_id), snippets))

def check_duplicate_id(snippets: List[OutputSnippet]) -> None:
    counter = Counter(map(lambda x: x[0], snippets))
    duplicate_ids = list(filter(lambda snippet_id: counter[snippet_id] > 1, counter.keys()))
    if len(duplicate_ids) > 0:
        raise ValueError(f"Duplicate snippet ids: {', '.join(duplicate_ids)}")

def main():
    with open(os.path.join(
        os.path.dirname(__file__),
        'snippets.yml',
    )) as f:
        categories: List[Dict[str, Any]] = yaml.safe_load(f)

    snippets = sum(list(map(transform_category, categories)), [])
    check_duplicate_id(snippets)

    result = dict(snippets)


    with open(os.path.join(
        os.path.dirname(__file__),
        '..',
        '.vscode',
        'generated.code-snippets'
    ), 'w') as f:
        json.dump(result, f, indent=2)

if __name__ == '__main__':
    main()
