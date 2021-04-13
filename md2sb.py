import re
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("file", help="path to the Markdown file")
args = parser.parse_args()

s=None
if args.file is None:
    s=r"""
"""
elif args.file == '-':
    s = sys.stdin.read()
else:
    f = open(args.file)
    s = f.read()

r = re.compile(r"\$(.+?)\$",)
r2 = re.compile(r"\[([!\"#%&'()*+,-./{|}<>_~]+ .+)$") # not used

print('\n'.join([r.sub(r'[$ \1 ]', l) for l in s.split("\n")]))
