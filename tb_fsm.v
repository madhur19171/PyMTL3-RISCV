`timescale 1ns/1ps
module tb_vdf_a3 (
    
);
reg clk=1'b0,reset, data_in;
wire data_out;
vdf_a3 in1(.clk(clk), .reset(reset), .data_in(data_in), .data_out(data_out));
initial begin
    $dumpfile("my_dump.vcd");
    $dumpvars(0,tb_vdf_a3);
    reset = 1'b0;
    data_in = 1'b0;
    #2 data_in = 1'b1;
    #10 data_in = 1'b0;
    #15 reset = 1'b1;
    #2 reset = 1'b0;
    #5 data_in = 1'b1;
    #10 data_in = 1'b0;
    #8 data_in = 1'b1;
    #20 $finish;
end    
always #5 clk = ~clk;

endmodule