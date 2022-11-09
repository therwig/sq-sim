import sys, ROOT
if len(sys.argv)<2: exit('usage: python convert_calcHEP2csv.py [filename.txt]')
isBkg = ('BeamBg' in sys.argv[1])

f = ROOT.TFile(sys.argv[1].replace('.txt','.root'),'recreate')
t = ROOT.TTree('Events','Events')
if isBkg:
    t.ReadFile(sys.argv[1],'e:mInitialz:nInitialz:mAx:mAy:mAz:mBx:mBy:mBz:Mx:My:Mz:nx:ny:nz',' ')
    # label m as A, B to emphasize they are not pz ordered
    # m=mu- (pdg 13), M=mu+ (pdg -13), n = nucleon
else:
    t.ReadFile(sys.argv[1],'e:mInitialz:nInitialz:rx:ry:rz:sx:sy:sz:nx:ny:nz',' ')
    # r = recoil, s=scalar, n=nucleon
t.Write()
f.Close()
