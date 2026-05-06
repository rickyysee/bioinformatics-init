## General Bioinformatics
This is a repository to store and update various bioinformatics tools/scripts that I write. Currently, the organization is simply by language.

- bin = Bash
- lib = Python

In the future, the organization may be changed to reflect different use cases.

### Python Scripts

|Name             |Description        |
|---              |---                |
|`genome.py`      |Gather simple statistics on a genome file. Expects a `.gz` fasta file and produces GC%|
|`ls.py`          |Mimics the function of Bash's `ls` command|
|`rename.py`      |Rename the first column of a file based on a name map file|

### Bash Scripts

|Name             |Description        |
|---              |---                |
|`loc_to_names.sh`|Specific use case. Update gene names in a counts file (such as that produced by HTSeq) based on the old and new genome annotation file|
|`rename.sh`       |Simple script to run `rename.py` on multiple files|