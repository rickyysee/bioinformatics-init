for i in HTSeq/*;
do
	scripts/rename.py $i -r annotations/IR_NCs.txt -o renamed
done