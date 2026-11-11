module parity16(input [15:0] a, output p);
  assign p = ^a;
endmodule