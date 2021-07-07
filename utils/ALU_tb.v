`timescale 10us/1ns

module ALU_tb;

    parameter BW = 4;
    

    reg [BW-1:0] ALUA, ALUB;
    reg [3:0] ALUControl;
    reg ALUFlagIn;

    //wire FlagZ, FlagN, FlagC, FlagV;
    wire FlagC, FlagZ, FlagN, FlaV;
    //reg c1,c2,c3,b1,b2,b3;
    wire [BW-1:0] ALUResult;
    


    ALU #(.B_W(BW)) UUT (.ALUA(ALUA), .ALUB(ALUB), .ALUFlagIn(ALUFlagIn), .ALUControl(ALUControl), .ALUResult(ALUResult), .FlagC(FlagC), .FlagZ(FlagZ), .FlagN(FlagN), .FlagV(FlagV));


    initial begin
        $display("\n-- Starting Simulation --");
        $dumpfile("./ALU.vcd");
        $dumpvars(0, ALU_tb);

        #10
	$display("\n-- Prueba a --\n");
	//Selecciona a
        ALUA=4'b1111; ALUB=4'b0111; ALUFlagIn= 1'b0; ALUControl=4'h2;
        #10  



        $display("-- Finishing Simulation --\n");
        $finish;
    end

    initial begin
      $monitor("FlIn=%b,A=%b, B=%b, K=%b, C=%b, Z=%b, N=%b, V=%b", ALUFlagIn, ALUA, ALUB, ALUResult, FlagC, FlagZ, FlagN, FlagV);
  end

endmodule
