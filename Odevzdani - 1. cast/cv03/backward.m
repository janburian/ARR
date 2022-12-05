function [beta, ppst_log_beta] = backward(pocet_neemitujicich_stavu, prechody_ppst, N, T)

    % Inicializace
    for i = 2:pocet_neemitujicich_stavu
        beta(T, i) = prechody_ppst(i, pocet_neemitujicich_stavu+1); 
    end

    % Rekurze  
    suma = 0;
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
    beta = [beta zeros(33,1)]; 
    
end

