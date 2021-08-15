module O_Opera (A,B, Control, FlagZ, RA, RB);

//BW = 16 bits

input [7:0] A, B;
input Control, FlagZ;
output reg [7:0] RA, RB;

   always@(*) begin
	if (~FlagZ && ~Control)
 		RA = B;
	else
		RA = A;

    end

always@(*) begin
	if (~FlagZ && ~Control)
 		RB = A;
	else
		RB = B;

    end
endmodule