module programCounter (clk, rst, PCin, enable, PCout);
	
	//inputs
	input clk, rst,enable;
	input [10:0] PCin;
	
	//outputs 
	output reg [10:0] PCout;
	
	//Counter logic
	always@(posedge clk, negedge rst) begin
		if(~rst) begin
			PCout <= 11'd2046;
		end
		else if (~enable) begin
			PCout <= PCout;
		end
		else
		PCout <= PCin;
	end
	
endmodule
