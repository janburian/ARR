clc
close all
clear all 

%% EM algoritmus (Cviceni 3) 
%% Nacteni souboru .txt 
priznaky = load('test_1.txt'); 

%% Ziskani pocatecnich strednich hodnot 
for i = 1:1:13
    mean_priznaky(1,i) = mean(priznaky(:,i)); 
    var_priznaky(1,i) = var(priznaky(:,i)); 
end

mean_priznaky(2,:) = mean_priznaky(1,:); 
mean_priznaky(3,:) = mean_priznaky(1,:); 

var_priznaky(2,:) = var_priznaky(1,:);
var_priznaky(3,:) = var_priznaky(1,:);

%% Pocatecni variance jednotlivych slozek a, n, o
varis_a = var_priznaky(1,:); 
varis_n = var_priznaky(2,:); 
varis_o = var_priznaky(3,:); 

%% Stredni hodnoty pro jednotlivych slozek a, n, o
mean_a = mean_priznaky(1,:); 
mean_n = mean_priznaky(2,:); 
mean_o = mean_priznaky(3,:); 

%% Vytvoreni kovariancnich matic pro jednotlive slozky a, n, o
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

%% Matice ppsti prechodu
A = [0 1.0 0 0 0; 
     0 0.5 0.5 0 0; 
     0 0 0.5 0.5 0; 
     0 0 0 0.5 0.5; 
     0 0 0 0   0]; 
 
%% Forward-backward algoritmus
prechody_ppst = A; 
pocet_neemitujicich_stavu = 4; 
suma = 0; 
T = length(priznaky);

for i = 1:7
    %% Vypocet hustot pravdepodobnosti
    N = prob_densities(priznaky, means, covs); 

    %% Vypocet alfy
    [alfa, ppst_log_alfa] = forward(pocet_neemitujicich_stavu, prechody_ppst, N, T); 

    %% Vypocet bety
    [beta, ppst_log_beta] = backward(pocet_neemitujicich_stavu, prechody_ppst, N, T);

    %% EM algoritmus
    [new_means, new_variances, a] = EM_algorithm(pocet_neemitujicich_stavu, alfa, beta, N, priznaky, prechody_ppst, A); 

    new_covs = cell(1,3); 
    new_covs{1} = diag(new_variances(1,:)); 
    new_covs{2} = diag(new_variances(2,:)); 
    new_covs{3} = diag(new_variances(3,:)); 
    
    means = new_means;
    covs = new_covs; 
    prechody_ppst = a;
end


