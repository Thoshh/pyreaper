# Introduction #

Small console tool that detects duplicated files by hashing them and then deletes these duplicated files leaving just one of them.

# Requirements #

  * Python 2.6

# Usage #

`reaper [options] <path to folder> [<path to folder...>]`

## Options ##

```
  --version             show version number and exit
  -h, --help            show this help message and exit
  -n, --dont-delete     skips delete process, useful for only detect
                        duplicates or create the digests
  -p, --print-rm-commands
                        skips delete process and prints a set of "rm" commands
                        so you can delete the duplicate files yourself
  -i, --interactive     interactive mode, will ask for each duplicate. By
                        default it deletes every duplicate found but the first
                        one
  -y, --dont-ask-confirmation
                        skips confirmation question.
  -s, --store-hashes    store and keep calculated hashes in .digest hidden
                        files
  -d, --delete-empty-trees
                        deletes empty trees when finishes
  -e EXTENSION, --ext=EXTENSION
                        only digests files with the given extension
  -v, --verbose         outputs much more information during process
                        (sometimes even too much)
  --ignore-stored-hashes
                        ignores stored calculated hashes in .digest hidden
                        files, this means every hash will be recalculated
```

## Examples ##

Here's a small list of examples:

  * Show duplicates found in one folder but do not delete anything
    * `reaper -n <path_to_folder>`
  * Print a script to manually delete any duplicate found between two folders
    * `reaper -p <path_to_folder> <path_to_second_folder>`
  * Digest a large folder and show duplicates (Keeping digest files will help running the command as many times as you want without calculating each time, it's a time saver when you dont know what you want to do with duplicated files)
    * `reaper -sn <path_to_folder>`
  * Find duplicates, delete them and delete empty trees
    * `reaper -d <path_to_folder>`