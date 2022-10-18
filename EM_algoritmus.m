clc
close all
clear all 
%% EM algoritmus (cviceni 3) 
%% Nacteni souboru .txt 
priznaky = load('test_1.txt'); 

%% Ziskani strednich hodnot 
for i = 1:1:13
    mean_priznaky(1,i) = mean(priznaky(:,i)); 
    var_priznaky(1,i) = var(priznaky(:,i)); 
end

mean_priznaky(2,:) = mean_priznaky(1,:); 
mean_priznaky(3,:) = mean_priznaky(1,:); 

var_priznaky(2,:) = var_priznaky(1,:);
var_priznaky(3,:) = var_priznaky(1,:);

%% Variance jednotlivych slozek a, n, o
varis_a = var_priznaky(1,:); 
varis_n = var_priznaky(2,:); 
varis_o = var_priznaky(3,:); 

%% Stredni hodnoty pro jednotlivych slozek a, n, o
mean_a = mean_priznaky(1,:); 
mean_n = mean_priznaky(2,:); 
mean_o = mean_priznaky(3,:); 

%% Kovariancni matice pro jednotlive slozky a, n, o
cov_a = diag(varis_a); 
cov_n = diag(varis_n); 
cov_o = diag(varis_o); 

%%
% Pole matic
covs = cell(1,3); 
covs{1,1} = cov_a; 
covs{1,2} = cov_n; 
covs{1,3} = cov_o; 

% Pole matic
means = cell(1,3); 
means{1,1} = mean_a; 
means{1,2} = mean_n; 
means{1,3} = mean_o; 

%% Vypocet hustot pravdepodobnosti
for i = 1:length(priznaky)
    for j = 1:1:3
        constant = (1 / sqrt(2 * pi)^13) * (1 / sqrt (det(covs{1,j}))); 
        exponent = -1/2 * ((priznaky(i,:) - means{1,j})) * inv(covs{1,j}) * ((priznaky(i,:) - means{1,j})'); 
        N(i, j) = constant * exp(exponent); 
    end
end

N = [zeros(length(priznaky),1) N zeros(length(priznaky),1)];

%% Matice ppsti prechodu
A = [0 1.0 0 0 0; 
     0 0.5 0.5 0 0; 
     0 0 0.5 0.5 0; 
     0 0 0 0.5 0.5; 
     0 0 0 0 0]; 
 
%% Forward-backward algoritmus
prechody_ppst = A; 
pocet_neemitujicich_stavu = 4; 
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
    vysl_ppst_alfa = vysl_ppst_alfa + alfa(T,i) * prechody_ppst(i,pocet_neemitujicich_stavu+1); 
end


ppst_log_alfa = log(vysl_ppst_alfa);

%% Vypocet bety
% Inicializace
for i = 2:pocet_neemitujicich_stavu
    beta(T, i) = prechody_ppst(i, pocet_neemitujicich_stavu+1); 
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

alfa = [alfa zeros(33,1)]; 
beta = [beta zeros(33,1)]; 

%% EM algoritmus
% vypocet novych strednich hodnot 
T = 33; 
new_means = []; 
new_covariances = []; 

mean_numerator = 0; 
mean_denumerator = 0;

for t = 2:1:T 
    for i = 1:1:13
        mean_numerator = mean_numerator + (alfa(t,i) * beta(t,i) * priznaky(i,:)); 
        mean_denumerator = mean_denumerator + (alfa(t,i) * beta(t,i))
    end
    
    
end
    

