module counter12 (
    input clk,
    input reset,
    input enable,
    output [3:0] Q,
    output c_enable,
    output c_load,
    output [3:0] c_d
); //
    assign c_enable = enable;
    count4 the_counter (clk, c_enable, c_load, c_d, Q );
    assign c_d = 4'd1;
    always @(*) begin
        c_load   = 1'b0;
        if (reset) c_load = 1'b1;
        else if (enable & (Q == 4'd12)) c_load = 1'b1;
    end

endmodule