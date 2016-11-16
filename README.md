# Filechanger

Hacky script made for changing file names in bulk for my dad <3

- uppercase
- lowercase
- replace
- insert
- remove

## Examples
### Lowercase
Sets lowercase for filenames on position 1 in current folder (and subfolders)
```
python filechanger.py . lower 1
```

Sets lowercase for filenames on position 1 in specific folder (and subfolders) for **UNIX/Mac**
```
python filechanger.py /path/to/folder lower 1
```

Sets lowercase for filenames on position 1 in specific folder (and subfolders) for **Windows**
```
python filechanger.py C:\path\to\folder lower 1
```

### Uppercase
Sets uppercase for filenames on position 1 to 4 (inclusive)
```
python filechanger.py . upper 1:4
```
Sets uppercase for filenames on position 1 to 4 (inclusive) in current folder but not subfolders
```
python filechanger.py . upper 1:4 nonrecursive
```

### Insert
Inserts "FISH" for file names on position 2 in current folder
```
python filechanger.py . insert 2 FISH
```

### Remove characters
Removes character on position 3-5 in current folder
```
python filechanger.py . remove 3:5
```

### Replace characters
Replaces characters on position 2-4 in current folder with "FISH"
```
python filechanger.py . replace 2:4 FISH
```
