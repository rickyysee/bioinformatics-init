#!/bin/bash

# initialize ref_count variable
ref_count=""
error_match=0
error_four=0

# for each fastq file in the directory
for file in *.fastq
do
	count=$(wc -l < "$file") # store the line count in a variable
	echo "$file: $count lines"

	# if ref count is empty
	if [ -z "$ref_count" ]; then
		# make sure reference line count is divisible by 4
		if (( count % 4 != 0 )); then
			printf "\tWARNING: $file line count ($count) is not a multiple of 4\n" >&2
			error_four=1
		fi
		ref_count=$count

	# this else block will only be evaluated on files after the reference (first)
	else
		# if the current count is not divisible by 4
		if (( count % 4 != 0 )); then
			printf "\tWARNING: $file line count ($count) is not a multiple of 4\n" >&2
			error_four=1
		fi

		# if the current count is not equal to the reference
		if [ "$count" -ne "$ref_count" ]; then
			printf "\tERROR: $file line count ($count) should be $ref_count\n" >&2
			error_match=1
		fi
	fi

done

echo

# error messages
if [[ "$error_match" -eq 1 && "$error_four" -eq 1 ]]; then
	echo "Line count mismatch detected!" >&2
	echo "Line count(s) not a multiple of 4!" >&2
	exit 1
elif [ "$error_match" -eq 1 ]; then
	echo "Line count mismatch detected!" >&2
	exit 1
elif [ "$error_four" -eq 1 ]; then
	echo "Line count(s) not a multiple of 4!" >&2
	exit 1
else
	echo "All files have the same line count: $ref_count"
fi