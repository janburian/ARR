clc
clear all
close all

%% Melovske kepstralni koeficienty - MFCC

%% Nacteni signalu
filename = "00010001.wav";
[y,Fs] = audioread(filename);
plot(y);

%% Hz to mel (Hranicni body filtru)
frek = Fs / 2; 
mel = hz2mel(frek);

counter = 0; 
bm = []; % hranice  
idx = 1; 
for i = 0:(mel/16):mel
    fprintf('%d %f %f \n', counter, i, mel2hz(i))
    bm(idx) = mel2hz(i); 
    counter = counter + 1;
    idx = idx + 1; 
end

%% 
counter = 0; 
frekvenceHz = []; % frekvence pro filtry 
idx = 1; 
for i = 0:(frek/128):frek
    fprintf('bod %d v Hz %f (v melech %f) \n', counter, i, hz2mel(i))
    frekvenceHz(idx) = i; 
    counter = counter + 1;
    idx = idx + 1; 
end

%% Filters
filters_num = 15; 
matrix = []; 

for i = 1:(filters_num)
    for j = 1:length(frekvenceHz)-1
        freq = frekvenceHz(1,j); 
        hodnota = OneFilter(freq, i, bm); 
        matrix(i,j) = hodnota; 
    end
end

filters = matrix

%%
n_times_window = round((length(y) - 256) / 80) % kolikrat mohu posunout okenko  

%% 
len_segment = 256; 
shift = 80; 

for u = 0:1:n_times_window-1
    data = y(u*shift + 1 : u*shift + len_segment); 
    
    % Hammingovo okenko 
    w = hamming(len_segment); 
    data_ham = data .* w;
    
    % DFT
    data_dft = fft(data_ham); 
    
    % 
    amps2 = abs(data_dft); 
    
    mid = length(amps2) / 2; 
    amps1 = amps2(1:mid) * 2; 
   
end

figure; 
plot(amps1); 





