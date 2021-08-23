module 256_to_1 ( 
    input [1023:0] in,
    input [7:0] sel,
    output [3:0] out );
    
    assign out[0] = in[sel*4 + 0];
    assign out[1] = in[sel*4 + 1];
    assign out[2] = in[sel*4 + 2];
    assign out[3] = in[sel*4 + 3];
    
    // assign out = in[((sel+1)*4)-1:(sel*4)];

endmodule