step1:
	python3 py/step1_csv_to_tree.py

step2: 
	g++ -o run_step2 step2_initial_to_final.cpp `root-config --glibs` `root-config --cflags`

step3:
	python3 py/plot_inputs.py -b

step4_threeMu: 
	g++ -o run_step4_threeMu step4_3mu_analysis.cpp `root-config --glibs` `root-config --cflags`

# split1:
# 	g++ -o run_split1 splitMuons.cpp `root-config --glibs` `root-config --cflags`

split2:
	g++ -o run_split2 splitMuons.cpp `root-config --glibs` `root-config --cflags`
