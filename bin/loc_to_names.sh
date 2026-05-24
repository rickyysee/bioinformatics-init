#!/bin/bash

usage="Usage: $(basename "$0") -[h|m|r] -[n|a|c|q] <inputs> -o <output>" # usage statement if help is called or args are incorrect
# initialize some variables to default 0 values
match_flag=0
rename_flag=0
output=0

help()
{
  # display help
  echo
  echo "This script is used to convert gene names in a counts file (such as those from HTSeq) to meaningful names by utilizing a curated annotation file from a de novo assembly workflows."
  echo
  echo $usage
  echo
  echo "Function"
  echo "-m           Match locus tags to annotated genes in a curated gtf file"
  echo "                Expects: <NCBI.gtf> <annotated.gtf> <counts.tsv>"
  echo "-r           Rename genes in a counts file by using the curated.tsv file from -m"
  echo "                Expects: <curated.tsv> <counts.tsv>"
  echo
  echo "Files"
  echo "-n           Set NCBI.gtf file to use"
  echo "-a           Set annotated.gtf file to use"
  echo "-c           Set counts.tsv file to use"
  echo "-q           Set curated.tsv file to use"
  echo "-o           Set output file (default is curated.tsv for -m and renamed_counts.tsv for -r)"
  echo
  echo "Help"
  echo "-h           Display this help page"
  echo
  echo "Ricky Cantua (2026)"
  echo
}

match()
{
  ### Extract NCBI gene id and store in temporary file
  echo "Extracting genomic location and locus tags from annotation..."
  awk -F '\t' -v OFS='\t' '/^[^#]/{print $4, $5, $9}' $ncbi | # print the genomic location (fields 4 and 5) and gene info (field 9)
  sed -E 's/^([^[:space:]]*)\t([^[:space:]]*)\tgene_id "([^"]*)".*$/\1\t\2\t\3/p' | # extract the gene id and return genomic location and gene id
  awk -F '\t' '!first[$3]++' > $output # return entire line of first occurrence of third field (gene id) to avoid duplicates

  ### Filter genomic location of locus tags by those found in counts
  echo "Filtering by counted genes..."
  awk -F '\t' '/^[^_]/{print $1}' $counts | # get the locus tags from counts file
  awk -F '\t' 'NR==FNR{seen[$1]; next} $3 in seen{print $0 > "temp"}' - $output # make an array of lines from stdout, then print entire line from temp when field 3 matches array
  mv temp $output

  ### Get curated transcript id from genomic location
  echo "Obtaining transcript IDs..."
  # This next command lines up the temp and annotated files by start and end of genome location
  awk -F '\t' -v OFS='\t' '
  # =====
  # first pass is on the curated.tsv file
  # key = start and end
  # value = locus tag
  # =====
  NR==FNR{
    key = $1 FS $2
    seen[key] = $3;
    next
  }
  # =====
  # create same key for annotated file
  # =====
  {
  key = $4 FS $5
  }
  # =====
  # when both keys match, print the value (locus tag), genome location and gene info
  # =====
  key in seen{
    print seen[key], $4, $5, $9
    }
  ' $output $annotated |
  sed -E 's/^([^[:space:]]*)\t([^[:space:]]*)\t([^[:space:]]*)\tgene_id "([^"]*)".*transcript_id "([^"]*)".*$/\1\t\2\t\3\t\5/p' | # extract the transcript id and return locus tag, genomic location, and transcript id
  awk -F '\t' '!first[$1]++ {print $0 > "temp"}'
  mv temp $output

  ### Remove lines where locus tag and transcript id are the same or transcript id is empty
  echo "Cleaning up..."
  awk -F '\t' '$1 != $4 {print $0}' $output |
  awk -F '\t' '$4 != "" {print $0 > "temp"}'
  mv temp $output

  echo "Done"
}

rename()
{
  ### Rename given counts file with curated file
  echo "Renaming $counts..."
  awk -F '\t' '
  # =====
  # first pass on curated file, create an array with locus tags as keys and annotations as values
  # =====
  NR==FNR{seen[$1] = $4; next} {
  # =====
  # second pass on counts file, if first column is in seen array, change that column to the array value (annotation)
  # =====
  if ($1 in seen) {
    $1 = seen[$1]
  } print}' $curated $counts > $output # print out lines to a specified output file
  echo "Done"
}

while getopts "hmrn:a:c:q:o:" opt; do # get the options and do things depending on what was called
  case $opt in
    h)
    # help page will be called then script exits
    help
    exit 0;;
    m)
    # set the match_flag to true
    match_flag=1;;
    r)
    # set the rename_flag to true
    rename_flag=1;;
    
    # following options are to take user arguments as file names for each respective option
    n)
    ncbi=$OPTARG;;
    a)
    annotated=$OPTARG;;
    c)
    counts=$OPTARG;;
    q)
    curated=$OPTARG;;
    o)
    output=$OPTARG;;
    \?)
    # exit if an invalid (not in above opt list) option is used
    echo "Error: invalid option" >&2
    echo $usage >&2
    exit 1;;
  esac
done

shift $((OPTIND - 1)) # shift the options so "$@" only contains non-option arguments

if [[ $match_flag == 1 && $rename_flag == 1 ]]; then # if both -m and -r are called, exit with an error
  echo "Error: -m and -r are mutually exclusive" >&2
  echo $usage >&2
  exit 1
elif [[ $match_flag == 1 ]]; then # if only -m is called
  if [[ $output == 0 ]]; then
    output=curated.tsv # default output for match
  fi
  match
elif [[ $rename_flag == 1 ]]; then # if only -r is called
  if [[ $output == 0 ]]; then
    output=renamed_counts.tsv # default output for rename
  fi
  rename
fi