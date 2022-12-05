function [z] = mel2hz(f_mel)
% Prevod melu na Hz
    % f_mel - frekvence v melech 
z = 700*(10.^(f_mel/2595)-1);

