function [z] = mel2hz(f)

z = 700*(10.^(f/2595)-1);

