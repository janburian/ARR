clc
clear all
close all

%% Melovske kepstralni koeficienty - MFCC
%% Nacteni signalu
filename = "00010001.wav";
[y, Fs] = audioread(filename);
plot(y);

%% Hz to mel (Hranicni body filtru)
frek = Fs / 2; % prenasene pasmo 
mel = hz2mel(frek);

counter = 0; 
bm = []; % hranice filtru  
idx = 1; 
for i = 0:(mel/16):mel
    fprintf('%d %f %f \n', counter, i, mel2hz(i))
    bm(idx) = mel2hz(i); 
    counter = counter + 1;
    idx = idx + 1; 
end

%% Vypocet frekvenci pro filtry 
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
matrix = zeros(filters_num, 128); 

for i = 1:filters_num
    for j = 1:length(frekvenceHz)-1
        freq = frekvenceHz(1,j); 
        hodnota = OneFilter(freq, i, bm); 
        matrix(i,j) = hodnota; 
    end
end

filters = matrix; 

%% Vypocet poctu posunuti okenka 
n_times_window = round((length(y) - 256) / 80); 

%% Rozdeleni vstupniho signalu na mikrosegmenty 
len_segment = 256; % velikost okenka 256 vzorku 
posun = 80; % velikost posunu 80 vzorku

cepOne_matrix = zeros(944, 15); 

for k = 0:1:n_times_window-1
    % Hammingovo okenko 
    w = hamming(len_segment);
    
    data = y(k * posun + 1 : k * posun + len_segment); % posun Hammingova okenka pro k-te okno
     
    data_ham = data .* w;
    
    % DFT
    data_dft = abs(fft(data_ham)); 
    
    % Absolutni hodnota dat_
    %amps2 = abs(data_dft); 
    
    mid = length(data_dft) / 2; 
    amps1 = data_dft(1:mid); 
    
    %% Vypocet energie jednotlivych filtru 
    energie = filters * amps1; % spocteni energie jednotlivych filtru pro k-te okno
   
    %% Logaritmus ve spektru 
    data_log = log10(energie); % kepstralni pristup

    %% Kosinova transformace
    cepOne = dct(data_log);  
    cepOne_matrix(k+1, :) = cepOne'; % Ukladani jednotlivych hodnot do radek matice
end

figure; 
plot(amps1); 





