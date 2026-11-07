v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 20 30 20 60 {lab=Y}
N 20 60 230 60 {lab=Y}
N 230 30 230 60 {lab=Y}
N 130 180 130 210 {lab=#net1}
N 20 -0 30 -0 {lab=Vdd}
N 30 -30 30 -0 {lab=Vdd}
N 20 -30 30 -30 {lab=Vdd}
N 220 -0 230 -0 {lab=Vdd}
N 220 -30 220 -0 {lab=Vdd}
N 220 -30 230 -30 {lab=Vdd}
N 130 240 140 240 {lab=GND}
N 140 240 140 270 {lab=GND}
N 130 270 140 270 {lab=GND}
N 20 -60 20 -30 {lab=Vdd}
N 20 -60 130 -60 {lab=Vdd}
N 130 -80 130 -60 {lab=Vdd}
N 130 -60 230 -60 {lab=Vdd}
N 230 -60 230 -30 {lab=Vdd}
N 130 270 130 290 {lab=GND}
N 130 60 130 120 {lab=Y}
N 130 90 240 90 {lab=Y}
N 130 150 240 150 {lab=GND}
N 240 150 240 290 {lab=GND}
N 130 290 240 290 {lab=GND}
N 130 290 130 310 {lab=GND}
C {sky130_fd_pr/pfet_01v8.sym} 0 0 0 0 {name=MP1
W=0.84
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
C {sky130_fd_pr/pfet_01v8.sym} 250 0 0 1 {name=MP2
W=0.84
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
C {sky130_fd_pr/nfet_01v8.sym} 110 150 0 0 {name=MN1
W=0.84
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
C {sky130_fd_pr/nfet_01v8.sym} 110 240 0 0 {name=MN2
W=0.84
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
C {ipin.sym} -80 80 0 0 {name=p6 lab=A}
C {ipin.sym} -80 120 2 1 {name=p9 lab=B}
C {opin.sym} 240 90 0 0 {name=p3 lab=Y}
C {iopin.sym} 130 -80 0 0 {name=p1 lab=Vdd}
C {iopin.sym} 130 310 0 0 {name=p2 lab=GND}
C {lab_pin.sym} -80 80 2 0 {name=p4 sig_type=std_logic lab=A}
C {lab_pin.sym} -20 0 0 0 {name=p5 sig_type=std_logic lab=A}
C {lab_pin.sym} 90 150 0 0 {name=p10 sig_type=std_logic lab=A}
C {lab_pin.sym} -80 120 2 0 {name=p8 sig_type=std_logic lab=B}
C {lab_pin.sym} 90 240 0 0 {name=p7 sig_type=std_logic lab=B}
C {lab_pin.sym} 270 0 2 0 {name=p11 sig_type=std_logic lab=B}
