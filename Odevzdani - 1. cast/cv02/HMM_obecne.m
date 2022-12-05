clc
clear all
close all

%% Skryte markovske modely - obecne (Cviceni 2)
%% Nacteni souboru .mat
filename = 'ANO.mat'; 
structure = cell2mat(struct2cell(load(filename)));

%% Nacteni souboru .txt 
filename_priznaky = 'test_1.txt'; 
priznaky = load(filename_priznaky); 

%% Variance a stredni hodnoty jednotlivych slozek 
varis = structure.varis; 
means = structure.means; 

size_varis = size(varis);

num_lines = size_varis(1); 
num_rows = size_varis(2); 

%% Vytvoreni pole kovariancnich matic a strednich hodnot pro jednotlive slozky
covs_cell = cell(1, num_lines); 
means_cell = cell(1, num_lines); 

for i = 1:1:num_lines
    cov = diag(varis(i, :)); 
    covs_cell{1, i} = cov; 
    
    mean = means(i, :); 
    means_cell{1, i} = mean; 
end

%% Vypocet hustot pravdepodobnosti
for i = 1:length(priznaky)
    for j = 1:1:num_lines
        constant = (1 / sqrt(2 * pi)^13) * (1 / sqrt (det(covs_cell{1,j}))); 
        exponent = -1/2 * ((priznaky(i,:) - means_cell{1,j})) * inv(covs_cell{1,j}) * ((priznaky(i,:) - means_cell{1,j})'); 
        N(i, j) = constant * exp(exponent); 
    end
end

N = [zeros(length(priznaky),1) N zeros(length(priznaky),1)];

%% Forward-backward algoritmus
prechody_ppst = structure.A; 
N_stavy = length(prechody_ppst); 

pocet_neemitujicich_stavu = N_stavy - 1; 
suma = 0; 
T = length(priznaky);

%% Vypocet alfy
% Inicializace 
for j = 2:1:pocet_neemitujicich_stavu
    alfa(j, 1) = (prechody_ppst(1,j) * N(1, j))'; 
end


% Rekurze  
for t = 2:1:T
    for j = 2:1:pocet_neemitujicich_stavu
        for i = 2:1:pocet_neemitujicich_stavu
            suma = suma + alfa(i, t-1) * prechody_ppst(i,j); 
        end
        alfa(j,t) = suma * N(t,j); 
        suma = 0;
    end
end

alfa = alfa'; 

% Vysledna pravdepodobnost
vysl_ppst_alfa = 0;  

for i = 2:1:pocet_neemitujicich_stavu
    vysl_ppst_alfa = vysl_ppst_alfa + alfa(T,i) * prechody_ppst(i, N_stavy); 
end


ppst_log_alfa = log(vysl_ppst_alfa);

%% Vypocet bety
% Inicializace
for i = 2:pocet_neemitujicich_stavu
    beta(T, i) = prechody_ppst(i, N_stavy); 
end


% Rekurze  
for t = T-1:-1:1
    for i = 2:1:pocet_neemitujicich_stavu
        for j = 2:1:pocet_neemitujicich_stavu
            suma = suma + prechody_ppst(i,j) * N(t+1, j) * beta(t+1, j); 
        end
        beta(t,i) = suma; 
        suma = 0;
    end
end


% Vysledna pravdepodobnost
vysl_ppst_beta = 0;  

for j = 2:1:pocet_neemitujicich_stavu
    vysl_ppst_beta = vysl_ppst_beta + prechody_ppst(1,j) * N(1, j) * beta(1,j); 
end


ppst_log_beta = log(vysl_ppst_beta); %(= ppst_log_alfa)





