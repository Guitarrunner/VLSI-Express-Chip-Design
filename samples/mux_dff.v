module mux_dff (
    input clk,
    input w, R, E, L,
    output Q
);
    wire mux_0;
    assign mux_0 = E ? w : Q;
        
    always @(posedge clk) begin
        if (L) Q <= R;
        else Q <= mux_0;
    end

endmodule