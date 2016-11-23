# Filechanger

Hacky scripts made for changing file names in bulk for my dad <3

Supports: Python 2.7+

py-files can be opened directly, via cmd/bash or import module.

## Examples
### Lowercase
Sets lowercase for filenames on position 1 in current folder (and subfolders)
```
python filechanger.py . lower 1
```
```
import filechanger
filechanger.lower('.', 1, 1)
```

Sets lowercase for filenames on position 1 in specific folder (and subfolders) for **UNIX/Mac**
```
python filechanger.py /path/to/folder lower 1
```
```
import filechanger
filechanger.lower('/path/to/folder', 1, 1, True)
```

Sets lowercase for filenames on position 1 in specific folder (and subfolders) for **Windows**
```
python filechanger.py C:\path\to\folder lower 1
```
```
import filechanger
filechanger.lower('C:\path\to\folder', 1, 1, True)
```

### Uppercase
Sets uppercase for filenames on position 1 to 4 (inclusive)
```
python filechanger.py . upper 1:4
```
```
import filechanger
filechanger.upper('C:\path\to\folder', 1, 4)
```
Sets uppercase for filenames on position 1 to 4 (inclusive) in current folder AND subfolders
```
python filechanger.py . upper 1:4 nonrecursive
```
```
import filechanger
filechanger.upper('C:\path\to\folder', 1, 4, True)
```

### Insert
Inserts "FISH" for file names on position 2 in current folder
```
python filechanger.py . insert 2 FISH
```
```
import filechanger
filechanger.insert('C:\path\to\folder', 2, 'FISH')
```

### Remove characters
Removes character on position 3-5 in current folder
```
python filechanger.py . remove 3:5
```
```
import filechanger
filechanger.remove('C:\path\to\folder', 3, 5)
```

### Replace characters
Replaces characters on position 2-4 in current folder with "FISH"
```
python filechanger.py . replace 2:4 FISH
```
```
import filechanger
filechanger.replace('C:\path\to\folder', 2, 4, 'FISH')
```

### Export file names
Exports file names in folder to csv-file
```
python fileexporter.py /path/to/file.csv /path/to/folder
```
```
import fileexporter
fileexporter.export('C:\path\to\folder', 'C:\path\to\exported-file.csv')
```

### Rename files based on csv
Renames file matches in first column to file names in second column (relative paths)
```
python csvrenamer.py /path/to/file.csv /path/to/folder
```
```
import csvrenamer
csvrenamer.rename('C:\path\to\folder', 'C:\path\to\exported-file.csv')
```
