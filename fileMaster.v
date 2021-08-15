module Ajuste (A, FlagC, FlagZ, X);

//Ajusta mantisa si FlagC y FlagZ están encendidos
//BW = 23 bits

    input wire [22:0] A;
    input wire FlagC, FlagZ;
    output reg [22:0] X;

    wire [22:0] D;

    assign D = A >> 1'd1;
    
    always @(*) begin
     if (FlagZ && FlagC | ~FlagZ && FlagC)

	X = D ;	

     else
	X = A;
    end
endmodule
