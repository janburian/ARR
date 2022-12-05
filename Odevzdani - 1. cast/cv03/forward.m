function [alfa, ppst_log_alfa] = forward(pocet_neemitujicich_stavu, prechody_ppst, N, T)
%% Vypocet alfy
  
    % Inicializace 
    for j = 2:1:pocet_neemitujicich_stavu
        alfa(j, 1) = (prechody_ppst(1,j) * N(1, j))'; 
    end


    % Rekurze  
    suma = 0; 
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
    alfa = [alfa zeros(33,1)]; 
    
end

