module sample10 (
    A,
    B,
    Fin,
    E,
    Y
);
  parameter BW = 4;

  input wire [BW-1:0] A, B;
  input Fin;

  output reg E;
  output reg [BW-1:0] Y;

  wire [BW-1:0] C, D, Not1, Or1;



  assign D = A << B;

  assign C = {BW{1'b1}} << B;


  Not #(
      .BW(BW)
  ) NOT1 (
      C1,
      0,
      0,
      Not1
  );
  Or #(
      .BW(B_W)
  ) OR1 (
      D1,
      Not1,
      Or1
  );

  always_comb begin

    if (Fin) Y = Or1;
    //Y = D | (~C);

    else

      Y = D;

  end

  always_comb begin

    if (B <= 4'b0100) E = A[BW-B];

    else E = Fin;

  end

endmodule
