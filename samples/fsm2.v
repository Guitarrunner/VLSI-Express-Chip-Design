module fsm1 (
    input clk,
    input in,
    input reset,
    output out); //

    parameter A=0, B=1, C=2, D=3; 
    reg [1:0] state, next_state;

    always @(*) begin    // This is a combinational always block
        // State transition logic
        case (state)
            A : begin
                  if (in) next_state = B;
                  else next_state = A;
            	end
             B : begin
                   if (in) next_state = B;
                   else next_state = C;
                 end
            C : begin
                   if (in) next_state = D;
                   else next_state = A;
            	end
             D : begin
                   if (in) next_state = B;
                   else next_state = C;
                 end
        endcase
    end

    always @(posedge clk) begin    // This is a sequential always block
        // State flip-flops with asynchronous reset
        if (reset) begin
           state <= A;
        end else begin
           state <= next_state; 
        end
    end

    // Output logic
    assign out = (state == D);

endmodule
