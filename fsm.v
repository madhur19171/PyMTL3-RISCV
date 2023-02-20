module vdf_a3 (
    input clk,
    input reset,
    input data_in,
    output data_out);

reg data_out_mod=1'b0;
parameter s0 = 2'b00, s1 = 2'b01, s2 = 2'b10;
reg [1:0] present_state, next_state;
always @(posedge clk) begin
    if(reset == 1)
        present_state  <= s0;
    else
        present_state <= next_state;
end

always @(*) begin
    case(present_state)
        s0: if(data_in==0)
                next_state = s0;
            else
                next_state = s1;
        s1: if(data_in==1)
                next_state = s1;
            else
                next_state = s2;
        s2: next_state = s0;
    default next_state = s0;
    endcase
end

always @(*) begin
    if(present_state == s2 & data_in == 1)
        data_out_mod = 1'b1;
end
assign data_out = data_out_mod;

endmodule