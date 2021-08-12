#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from random import choice
from string import ascii_lowercase, digits
from subprocess import run

TMP_DIR = Path("/tmp")
EDITOR = "nvim"


def select(symbols, length):
    return "".join([choice(symbols) for _ in range(length)])


def generate_filename():
    """Generate a filepath in tmp directory"""
    filename = select(digits + ascii_lowercase, 32)
    filepath = TMP_DIR / f"{filename}.txt"
    return filepath


parser = ArgumentParser(__file__)
parser.add_argument(
    "pattern",
    nargs="*",
    help="[OPTIONAL] A pattern to match all files with, by default it matches everything",
)

parser.add_argument(
    "--recursive",
    "-r",
    dest="recursive",
    type=str,
    help="[OPTIONAL] Recurse through all subdirectories from here, or not (on by default)",
)

parser.set_defaults(
    recursive="",
)

args = parser.parse_args()

# We take the first argument of an pseudo-optional list of arguments
pattern = args.pattern[0] if args.pattern else "*"

# Any of these keywords may disable recursion
recursive = args.recursive.lower() not in [
    "false",
    "n",
    "no",
    "off",
]

# NOTE: We could also import tempfile and create the temporary file more
# idiomatically, but I don't really care for users of other operating systems

# Generate a unique filename for our temporary file
# do-while
filepath = generate_filename()
while filepath.exists():
    filepath = generate_filename()

# Create tempfile
f = open(filepath, "w")
current_directory = Path(".")

if recursive:
    current_lines = [str(item) for item in current_directory.rglob(pattern)]
else:
    current_lines = [str(item) for item in current_directory.glob(pattern)]

if current_lines:
    f.write("\n".join(current_lines))

f.close()

# Let some editor edit the filepaths
run([EDITOR, filepath])

# Now we check what the Rock has been cooking 🍲
f = open(filepath, "r")
future_lines = f.read().split("\n")
f.close()

# Delete the temporary file, it has served its purpose
Path(filepath).unlink()

N_CUR = len(current_lines)
N_FUT = len(future_lines)

if N_CUR > N_FUT:
    # For zip, it is okay when the number of future lines is greater than the
    # number of current lines, it simply means the first N_CUR lines will be
    # used for the filesystem actions
    print(
        f"The number of lines in the before ({N_CUR}) and after ({N_FUT}) are too different to continue safely"
    )
    exit(1)

for old, new in zip(current_lines, future_lines):
    if old == new:
        # If nothing changed, simply skip
        continue

    # Out with the old, in with the new!
    print(f"{old} -> {new}")

    np = Path(new)
    if np.exists():
        print(f"{old} stays {old}, {new} already exists")
        continue

    # Generate all new required paths to make the new filepath possible
    np.parent.mkdir(parents=True, exist_ok=True)

    op = Path(old)
    op.rename(new)
