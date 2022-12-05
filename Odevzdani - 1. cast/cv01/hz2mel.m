function z = hz2mel(f_Hz)
% Prevod Hz na mel 
    % f_Hz - frekvence v Hz
z = 2595 * log10(1 + f_Hz/700);

