## Instructions

First convert the CalcHEP outputs from our theory friends into root files.

```
E=20
for f in data/${E}GeVBeam/*txt;
do
    python3 scripts/convert_calcHEP2root.py $f > /dev/null 2>&1
    echo finished converting $f
done
python3 scripts/convert_calcHEP2root.py data/${E}GeVBeamBg.txt > /dev/null 2>&1

```

Calculate other variables that we might be interested in using via some friend trees.

```
root -b scripts/makeBkgFriend.C # might need to change from "20GeV" manually
```

For the signal, the scalar needs to first be decayed to muons, which we do in a custom step for signal only.
Its possible to (randomly) decay the scalar multiple times to produce extra events.

```
nDecays=10
root -b scripts/decayS.C\(\"data/${E}GeVBeam/mS900MeV${E}.root\",0.900,$nDecays\);
root -b scripts/decayS.C\(\"data/${E}GeVBeam/mS800MeV${E}.root\",0.800,$nDecays\);
root -b scripts/decayS.C\(\"data/${E}GeVBeam/mS700MeV${E}.root\",0.700,$nDecays\);
root -b scripts/decayS.C\(\"data/${E}GeVBeam/mS600MeV${E}.root\",0.600,$nDecays\);
root -b scripts/decayS.C\(\"data/${E}GeVBeam/mS500MeV${E}.root\",0.500,$nDecays\);
root -b scripts/decayS.C\(\"data/${E}GeVBeam/mS400MeV${E}.root\",0.400,$nDecays\);
root -b scripts/decayS.C\(\"data/${E}GeVBeam/mS300MeV${E}.root\",0.300,$nDecays\);
root -b scripts/decayS.C\(\"data/${E}GeVBeam/mS220MeV${E}.root\",0.220,$nDecays\);
root -b scripts/decayS.C\(\"data/${E}GeVBeam/mS1000MeV${E}.root\",1,$nDecays\);
root -b scripts/decayS.C\(\"data/${E}GeVBeam/mS2000MeV${E}.root\",2,$nDecays\);
root -b scripts/decayS.C\(\"data/${E}GeVBeam/mS3000MeV${E}.root\",3,$nDecays\);
root -b scripts/decayS.C\(\"data/${E}GeVBeam/mS4000MeV${E}.root\",4,$nDecays\);
```

And after this last step the signals friends can also be produced.

```
for f in data/${E}GeVBeam/*_decayed.root;
do
    root -b scripts/makeSigFriend.C\(\"$f\"\);
    echo finished converting $f
done
```
