module cmp8(input [7:0] a, input [7:0] b, output lt, output eq);
  assign lt = a < b;
  assign eq = (a == b);
endmodule