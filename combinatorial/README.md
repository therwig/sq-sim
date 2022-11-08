# SQ simulation

In general the steps are recorded in the Makefile.

1. Convert the gen muons from csv to a ROOT Tree

```
make step1
# python3 py/step1_csv_to_tree.py
```

The resulting data file will go into the `data/` directory.

2. Propogate muons through target

```
make step2
./run_step2 <RANDSEED>
```

This can be run many times in parallel if desired, in order to accumulate a larger samples of single muon events.
I.e.
```
time ./run_step2 10 &
time ./run_step2 11 &
time ./run_step2 12 &
...
hadd data/final_muons_noSkim.root data/final_muons_*.root 
```

3. Plot some properties of the muons that have passed through the target

```
make step3
# python3 py/plot_inputs.py
```

4. Run the multi-muon analysis

There are two flavors of the analysis, requiring either 2 or 3 muons to be simulated. First we develop the three muon analysis:

```
make step4_threeMu
./run_step4_threeMu
```

And second we consider the minimal, two-muon analysis.
To perform this efficiently, we split all final muons into bins according to their final position in the bending plane.

```
mkdir data/splitMuons
make split1
./run_split1
```

Unfortunately, this code was overwritten by step2 and must be reproduced (TODO).  In the mean time we can run over premade inputs.


After this splitting step, the pairs of mu+ and mu- in each bin can be used to produce masses.

```
make split2
./run_split2
```

This results in a large set of muon pairs, with masses, for further analyis.