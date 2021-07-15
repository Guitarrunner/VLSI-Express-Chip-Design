module Incremento (A, B, Cout, Fin, V, Y);
    parameter B_W = 4;
    input wire Fin;
    output reg Cout;
    input wire [B_W-1:0] A, B;
    output reg [B_W-1:0] Y;
    output reg V;
    wire v0,v1, C1, C2;
    wire [B_W-1:0] inc;
    wire [B_W-1:0] inc1;
	
	Look_ahead #(.B_W(B_W)) Inc (B, 4'b0001, 4'b0000, C1, v0, inc);
	
	Look_ahead #(.B_W(B_W)) Inc1 (A, 4'b0001,4'b0000, C2, v1, inc1);
	

   always @ (*) begin

	if(Fin)
    	Y<= inc;


	else
	Y<= inc1;
	
	
    end
  always @ (*) begin

	if(Fin)
    	Cout=C1;


	else
	Cout=C2;
	
	
    end
       always @ (*) begin
	if(Fin)
    	V=v0;


	else
	V=v1;
	
	
    end
endmodule
