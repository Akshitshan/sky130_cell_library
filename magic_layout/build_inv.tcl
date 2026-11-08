# In Magic's tkcon:  set name inv_x2; set Wp 1.68; set Wn 0.84; source ../build_inv.tcl
proc rp {layer x1 y1 x2 y2} {
    set x1 [format %.2f $x1]; set y1 [format %.2f $y1]
    set x2 [format %.2f $x2]; set y2 [format %.2f $y2]
    box ${x1}um ${y1}um ${x2}um ${y2}um
    paint $layer
}
proc up {v} {global dP; return [expr {$v + $dP}]}
proc dn {v} {global dN; return [expr {$v - $dN}]}

# extra width relative to the x1 inverter (Wp 0.84, Wn 0.42)
set dP [expr {$Wp - 0.84}]
set dN [expr {$Wn - 0.42}]

# well and diffusion
rp nwell -0.66 -0.59 0.69 [up 1.40]
rp pdiff -0.46 -0.39 0.49 [up 0.45]
rp ndiff -0.46 [dn -1.60] 0.49 -1.18

# gate poly and input pad
rp polysilicon -0.06 [dn -1.82] 0.09 [up 0.64]
rp polysilicon -0.45 -0.97 0.09 -0.65

# taps
rp nsubstratendiff -0.46 [up 0.86] 0.51 [up 1.17]
rp nsubstratencontact -0.33 [up 0.93] 0.38 [up 1.10]
rp psubstratepdiff -0.46 [dn -2.24] 0.51 [dn -1.93]
rp psubstratepcontact -0.33 [dn -2.17] 0.38 [dn -2.00]

# diffusion and poly contacts
rp pdcontact -0.36 -0.29 -0.17 [up 0.35]
rp pdcontact 0.20 -0.29 0.39 [up 0.35]
rp ndcontact -0.36 [dn -1.50] -0.17 -1.28
rp ndcontact 0.20 [dn -1.50] 0.39 -1.28
rp pcontact -0.37 -0.89 -0.20 -0.72

# local interconnect
rp locali -0.46 -0.39 -0.07 [up 0.45]
rp locali 0.10 -0.39 0.49 [up 0.45]
rp locali -0.34 [up 0.45] -0.17 [up 0.86]
rp locali -0.46 [up 0.86] 0.51 [up 1.17]
rp locali -0.46 [dn -1.60] -0.07 -1.18
rp locali 0.10 [dn -1.60] 0.49 -1.18
rp locali -0.34 [dn -1.93] -0.17 [dn -1.60]
rp locali -0.46 [dn -2.24] 0.51 [dn -1.93]
rp locali -0.45 -0.97 -0.03 -0.65
rp locali 0.20 -1.18 0.39 -0.39

# li to metal1 contacts
rp viali -0.23 [up 0.93] -0.02 [up 1.10]
rp viali -0.23 [dn -2.17] -0.02 [dn -2.00]
rp viali -0.37 -0.89 -0.20 -0.72
rp viali 0.25 -0.86 0.42 -0.69

# metal1: rails, input pad, output wire
rp metal1 -1.46 [up 0.86] 1.51 [up 1.17]
rp metal1 -1.46 [dn -2.24] 1.51 [dn -1.93]
rp metal1 -1.12 -0.99 0.03 -0.63
rp metal1 0.19 -0.98 1.22 -0.64

# ports, numbered like inverter.mag: Vdd 1, GND 2, Vout 3, Vin 4
box 1.16um [format %.2f [up 0.96]]um 1.26um [format %.2f [up 1.07]]um
label Vdd
port make
box 1.16um [format %.2f [dn -2.14]]um 1.26um [format %.2f [dn -2.03]]um
label GND
port make
box 1.04um -0.84um 1.09um -0.79um
label Vout
port make
box -1.02um -0.84um -0.97um -0.79um
label Vin
port make

save $name