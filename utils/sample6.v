module Look_ahead(A, B, Cin, Co, V, F);

parameter B_W = 4;

input wire [B_W-1:0] A, B;
wire [B_W-1:0] A1, B1;

input wire Cin;
output [B_W-1:0] F;
output reg Co;
output reg V;

wire [B_W:0] W_C;
wire [B_W-1:0] W_G, W_P, W_F;

	assign A1 = A;
	assign B1 = B;

genvar  ii;
generate
    for (ii=0; ii<B_W; ii=ii+1)
    begin
        Sum Sum_inst(.a(A1[ii]), .b(B1[ii]), .cin(W_C[ii]), .suma(W_F[ii]), .carry());
    end
endgenerate

genvar jj;
generate
    for (jj=0; jj<B_W; jj=jj+1)
    begin
        assign W_G[jj] = A1[jj] & B1[jj];
        assign W_P[jj] = A1[jj] | B1[jj];
        assign W_C[jj+1] = W_G[jj] | (W_P[jj] & W_C[jj]);
    end
endgenerate

assign W_C[0] = Cin;

assign F = W_F;
always @(*) begin
	 if ((A1[B_W - 1] != B1[B_W-1]) & W_C[B_W] == 1 | (A1[B_W - 1] == B1[B_W-1]) & W_C[B_W - 1] == A1[B_W - 1] & W_C[B_W ] ==1)
	           Co = W_C[B_W];  
	       else
	           Co = 1'b0;
	       end 

always @(*) begin
	 if ((A1[B_W - 1] == B1[B_W -1]) & (A1[B_W - 1]!= W_F[B_W - 1]) | (A[B_W - 1] == B1[B_W -1]) & (A1[B_W - 1]!= W_F[B_W - 1]) & (W_C[B_W] == 1'b1 ))
	           V = 1'b1;  
	       else
	           V = 1'b0;
	       end
endmodule

