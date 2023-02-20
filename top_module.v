`include "adder.v"
module top_module( 
    input [2:0] a, b,
    input cin,
    output [2:0] cout,
    output  [2:0] sum );
    adder a1(.a(a[0]), .b(b[0]), .cin(cin), .cout(cout[0]), .sum(sum[0]));
    adder a2(.a(a[1]), .b(b[1]), .cin(cout[0]), .cout(cout[1]), .sum(sum[1]));
    adder a3(.a(a[2]), .b(b[2]), .cin(cout[1]), .cout(cout[2]), .sum(sum[2]));

endmodule