module Corrimiento_izq (A, B, Fin, E, Y);
    parameter B_W = 4;

    input wire [B_W-1:0] A, B;
    input  Fin;
    
    output reg E;
    output reg [B_W-1:0] Y;

    wire [B_W-1:0] C, D, Not1, Or1;
    

    
    assign D = A << B;

    assign C = {B_W{1'b1}} << B;
    
    
    Not #(.B_W(B_W)) NOT1 (C, 0, 0, Not1);
    Or #(.B_W(B_W)) OR1 (D, Not1, Or1);
    
    always @(*) begin
   
	if (Fin)

	 Y = Or1;
	//Y = D | (~C);
    
    	else
    	
    	 Y = D;
    	 
    end

   always @(*) begin
   
	if (B<=4'b0100)

	E = A[B_W-B];
    
    	else
    	
    	E = Fin;
    	 
    end

endmodule