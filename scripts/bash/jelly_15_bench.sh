main_dir="/ifs/groups/rosenMRIGrp/kr3288/extended"
splits=("groupaa" "groupab" "groupac" "groupad" "groupae" "groupaf" "groupag" "groupah" "groupai" "groupaj")
for split in "${splits[@]}"; do
	python3 script_generatorv2.py jelly-15-mers_${split}.sh "/ifs/groups/rosenMRIGrp/kr3288/jellyfish_gen_new_UPDATED.bash /ifs/groups/rosenMRIGrp/kr3288/extended/${split} 15 false" /ifs/groups/rosenMRIGrp/kr3288/bench_jelly
done