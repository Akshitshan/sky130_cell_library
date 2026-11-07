v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 0 -200 0 -170 {lab=Vdd}
N 0 -110 0 -80 {lab=#net1}
N -80 20 80 20 {lab=Y}
N -0 -20 0 20 {lab=Y}
N -80 20 -80 40 {lab=Y}
N 80 20 80 40 {lab=Y}
N -80 100 -80 120 {lab=GND}
N -80 120 80 120 {lab=GND}
N 80 100 80 120 {lab=GND}
N -0 120 -0 140 {lab=GND}
N -0 -140 10 -140 {lab=Vdd}
N 10 -170 10 -140 {lab=Vdd}
N 0 -170 10 -170 {lab=Vdd}
N 0 -0 120 -0 {lab=Y}
N -0 -50 100 -50 {lab=Vdd}
N 100 -180 100 -50 {lab=Vdd}
N -0 -180 100 -180 {lab=Vdd}
N -80 70 -70 70 {lab=GND}
N -70 70 -70 100 {lab=GND}
N -80 100 -70 100 {lab=GND}
N 80 70 90 70 {lab=GND}
N 90 70 90 100 {lab=GND}
N 80 100 90 100 {lab=GND}
C {sky130_fd_pr/pfet_01v8.sym} -20 -140 0 0 {name=MP1
W=1.68
L=0.15
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} -20 -50 0 0 {name=MP2
W=1.68
L=0.15
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} -100 70 0 0 {name=MN1
W=0.42
L=0.15
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 60 70 0 0 {name=MN2
W=0.42
L=0.15
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {iopin.sym} 0 -200 0 0 {name=p1 lab=Vdd}
C {ipin.sym} -120 -100 0 0 {name=p6 lab=A}
C {ipin.sym} -120 -60 2 1 {name=p9 lab=B}
C {lab_pin.sym} -120 -100 2 0 {name=p4 sig_type=std_logic lab=A}
C {lab_pin.sym} -120 -60 2 0 {name=p8 sig_type=std_logic lab=B}
C {lab_pin.sym} -40 -50 0 0 {name=p5 sig_type=std_logic lab=A}
C {lab_pin.sym} -120 70 0 0 {name=p2 sig_type=std_logic lab=A}
C {lab_pin.sym} -40 -140 0 0 {name=p11 sig_type=std_logic lab=B}
C {lab_pin.sym} 40 70 0 0 {name=p3 sig_type=std_logic lab=B}
C {opin.sym} 120 0 0 0 {name=p7 lab=Y}
C {iopin.sym} 0 140 0 0 {name=p10 lab=GND}
