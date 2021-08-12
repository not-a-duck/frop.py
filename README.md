# Froppy 🐸

Mass rename files and directories with a simple `frop.py` in your shell.

By default,

* it creates a temporary file in `/tmp`
* it uses `nvim` to edit this temporary file
* creates new directories when the new filenames require these

# Basic usage

```bash
frop.py
```

Edit all the files within your favourite editor (which is neovim of course).
Then when you're all done, write and quit that temporary file, and watch Python
do all the renaming you ordered.

#
