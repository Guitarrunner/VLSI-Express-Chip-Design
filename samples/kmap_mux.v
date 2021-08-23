module kmap_mux (
    input c,
    input d,
    output [3:0] mux_in
); 
    
    always @(*) begin
        case ({ c, d })
            2'b00 : begin
                mux_in[0] = 1'b0;
                mux_in[1] = 1'b0;
                mux_in[2] = 1'b1;
                mux_in[3] = 1'b0;
            end
            2'b01 : begin
                mux_in[0] = 1'b1;
                mux_in[1] = 1'b0;
                mux_in[2] = 1'b0;
                mux_in[3] = 1'b0;
            end
            2'b11 : begin
                mux_in[0] = 1'b1;
                mux_in[1] = 1'b0;
                mux_in[2] = 1'b0;
                mux_in[3] = 1'b1;
            end
            2'b10 : begin
                mux_in[0] = 1'b1;
                mux_in[1] = 1'b0;
                mux_in[2] = 1'b1;
                mux_in[3] = 1'b0;
             end
        endcase
    end

endmodule