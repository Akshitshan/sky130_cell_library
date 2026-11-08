v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 10 -30 10 30 {lab=Vout}
N -50 -60 -30 -60 {lab=Vin}
N -50 -60 -50 50 {lab=Vin}
N -50 50 -50 60 {lab=Vin}
N -50 60 -30 60 {lab=Vin}
N 10 90 10 120 {lab=GND}
N 10 -60 80 -60 {lab=Vdd}
N 10 -110 80 -110 {lab=Vdd}
N 80 -110 80 -60 {lab=Vdd}
N 10 60 80 60 {lab=GND}
N 80 60 80 100 {lab=GND}
N 10 100 80 100 {lab=GND}
N 10 0 90 -0 {lab=Vout}
N 10 -110 10 -90 {lab=Vdd}
N -90 0 -50 0 {lab=Vin}
C {sky130_fd_pr/pfet_01v8.sym} -10 -60 0 0 {name=M1
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
C {sky130_fd_pr/nfet_01v8.sym} -10 60 0 0 {name=M2
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
C {ipin.sym} -90 0 0 0 {name=p1 lab=Vin}
C {opin.sym} 90 0 0 0 {name=p2 lab=Vout}
C {iopin.sym} 10 -110 3 0 {name=p3 lab=Vdd}
C {iopin.sym} 10 120 1 0 {name=p4 lab=GND}
