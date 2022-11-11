E=20
# for f in data/${E}GeVBeam/*txt;
# do
#     python3 scripts/convert_calcHEP2root.py $f > /dev/null 2>&1
#     echo finished converting $f
# done

#python3 scripts/convert_calcHEP2root.py data/${E}GeVBeamBg.txt > /dev/null 2>&1
rt scripts/makeBkgFriend.C

# nDecays=10
# rt scripts/decayS.C\(\"data/${E}GeVBeam/mS900MeV${E}.root\",0.900,$nDecays\);
# rt scripts/decayS.C\(\"data/${E}GeVBeam/mS800MeV${E}.root\",0.800,$nDecays\);
# rt scripts/decayS.C\(\"data/${E}GeVBeam/mS700MeV${E}.root\",0.700,$nDecays\);
# rt scripts/decayS.C\(\"data/${E}GeVBeam/mS600MeV${E}.root\",0.600,$nDecays\);
# rt scripts/decayS.C\(\"data/${E}GeVBeam/mS500MeV${E}.root\",0.500,$nDecays\);
# rt scripts/decayS.C\(\"data/${E}GeVBeam/mS400MeV${E}.root\",0.400,$nDecays\);
# rt scripts/decayS.C\(\"data/${E}GeVBeam/mS300MeV${E}.root\",0.300,$nDecays\);
# rt scripts/decayS.C\(\"data/${E}GeVBeam/mS220MeV${E}.root\",0.220,$nDecays\);
# rt scripts/decayS.C\(\"data/${E}GeVBeam/mS1000MeV${E}.root\",1,$nDecays\);
# rt scripts/decayS.C\(\"data/${E}GeVBeam/mS2000MeV${E}.root\",2,$nDecays\);
# rt scripts/decayS.C\(\"data/${E}GeVBeam/mS3000MeV${E}.root\",3,$nDecays\);
# rt scripts/decayS.C\(\"data/${E}GeVBeam/mS4000MeV${E}.root\",4,$nDecays\);

# for f in data/${E}GeVBeam/mS4000MeV${E}*_decayed.root;
for f in data/${E}GeVBeam/*_decayed.root;
do
    rt scripts/makeSigFriend.C\(\"$f\"\);
    echo finished converting $f
done

