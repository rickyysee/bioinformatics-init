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
  echo "Extracting genomic location and locus tags from annotation..."
  awk -F '\t' -v OFS='\t' '/^[^#]/{print $4, $5, $9}' $ncbi |
  sed -nE 's/^([^[:space:]]*)\t([^[:space:]]*)\tgene_id "([^"]*)".*$/\1\t\2\t\3/p' |
  awk -F '\t' '!first[$3]++' > $output

  echo "Filtering by counted genes..."
  awk -F '\t' '/^[^_]/{print $1}' $counts |
  awk -F '\t' 'NR==FNR{seen[$1]; next} $3 in seen{print $0 > "temp"}' - $output


  echo "Obtaining transcript IDs..."
  awk -F '\t' -v OFS='\t' '
  NR==FNR{
  key = $1 FS $2
  seen[key] = $3;
  next
  }
  {
  key = $4 FS $5
  }
  key in seen{
  print seen[key], $4, $5, $9
  }
  ' $output $annotated |
  sed -nE 's/^([^[:space:]]*)\t([^[:space:]]*)\t([^[:space:]]*)\tgene_id "([^"]*)".*$/\1\t\2\t\3\t\4/p' |
  awk -F '\t' '!first[$1]++ {print $0 > "temp"}'
  mv temp $output

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