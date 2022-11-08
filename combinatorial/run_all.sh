#OA python3 step1_csv_to_tree.py

# g++ -o run_step2 step2_initial_to_final.cpp `root-config --glibs` `root-config --cflags`
# ./run_step2 3 # random seed

# g++ -o run_step4b step4b_analysis.cpp `root-config --glibs` `root-config --cflags`
# ./run_step4b

# python3 plot_inputs.py -b

# time ./run_step2 40 &
# time ./run_step2 41 &
# time ./run_step2 42 &
# time ./run_step2 43 &
# time ./run_step2 34 &
# time ./run_step2 35 &
# time ./run_step2 36 &
# time ./run_step2 37 &
# time ./run_step2 38 &
# time ./run_step2 39 &

# time ./run_step4b _part1 0 393396 &
# time ./run_step4b _part2 393396 786692 &
# time ./run_step4b _part3 786692 1180188 &
# time ./run_step4b _part4 1180188 1573586 &

# time ./run_step4b _part1 0 262264 &
# time ./run_step4b _part2 262264 524528 &
# time ./run_step4b _part3 524528 786793 &
# time ./run_step4b _part4 786793 1049057 &
# time ./run_step4b _part5 1049057 1311321 &
# time ./run_step4b _part6 1311321 1573586 &

time ./run_step4b realDist_noskim

g++ -o run_split split.cpp `root-config --glibs` `root-config --cflags`

