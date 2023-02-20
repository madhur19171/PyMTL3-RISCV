module ripple_carry_4bit(q, clk, reset);
input clk, reset;
output [3:0] q;

Tff tff1(q[0], clk, reset);

Tff tff2(q[1], q[0], reset);

Tff tff3(q[2], q[1], reset);

Tff tff4(q[3], q[2], reset);

endmodule

module Tff(q, clk, reset);
output q;
input clk, reset;
wire d;

Dff dff1(q,d,clk, reset);
not n1(d,q);

endmodule

module Dff(q, d, clk, reset);
input clk, d, reset;
output q;
always@(posedge reset or negedge clk)
    begin
        if(reset)
            q<=1'b0;
        else
            q<=d;
    end
endmodule