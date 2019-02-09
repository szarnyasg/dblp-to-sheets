# dblp-to-sheets

:warning: This script copies the row to your clipboard and will overwrite its content.

```
./extract.sh conf/sigmod/DateC74
./extract.sh journals/tods/Chen76
./extract.sh journals/corr/OngPV14
```

Add something like this to your `~/.bashrc`:

```
alias e="~/git/dblp-to-sheets/extract.py"
```

Now you can use `e ...` to grab any ref.
