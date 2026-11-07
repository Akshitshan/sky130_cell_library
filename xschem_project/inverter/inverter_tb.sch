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
C {sky130_fd_pr/nfet_01v8.sym} -10 60 0 0 {name=M2
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
C {lab_pin.sym} 90 0 0 1 {name=p4 sig_type=std_logic lab=Vout}
C {gnd.sym} 10 120 0 0 {name=l1 lab=GND}
C {vsource.sym} -250 70 0 0 {name=V1 value=1.8 savecurrent=false}
C {lab_wire.sym} 10 -110 0 0 {name=p2 sig_type=std_logic lab=Vdd}
C {lab_wire.sym} -250 40 0 0 {name=p5 sig_type=std_logic lab=Vdd}
C {lab_wire.sym} 10 120 0 0 {name=p6 sig_type=std_logic lab=GND}
C {lab_wire.sym} -250 100 2 1 {name=p7 sig_type=std_logic lab=GND}
C {vsource.sym} -250 -90 0 0 {name=V2 value="pulse(0 1.8 1n 0.1n 0.1n 5n 10n)" savecurrent=false}
C {lab_wire.sym} -250 -60 2 1 {name=p1 sig_type=std_logic lab=GND}
C {code.sym} -410 -50 0 0 {name=s1 
only_toplevel=false
value=".lib /home/akshit/.ciel/ciel/sky130/versions/1689ac3f2dc763876eaf967227c7dfe831b031ae/sky130A/libs.tech/ngspice/sky130.lib.spice tt
.tran 0.1n 20n
.measure tran tphl TRIG v(vin) VAL=0.9 RISE=1 TARG v(vout) VAL=0.9 FALL=1
.measure tran tplh TRIG v(vin) VAL=0.9 FALL=1 TARG v(vout) VAL=0.9 RISE=1"}
C {lab_pin.sym} -90 0 0 0 {name=p3 sig_type=std_logic lab=Vin}
C {lab_pin.sym} -250 -120 0 0 {name=p8 sig_type=std_logic lab=Vin}
