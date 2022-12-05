function [new_means_cell, new_variances, a] = EM_algorithm(pocet_neemitujicich_stavu, alfa, beta, N, priznaky, prechody_ppst, A)
    % vypocet novych strednich hodnot 
    T = 33; 
    new_means = []; 

    mean_numerator = 0; 
    mean_denominator = 0;
    
    new_means_cell = cell(1,3);
    for j = 2:1:pocet_neemitujicich_stavu
        for t = 1:1:T
            mean_numerator = mean_numerator + (alfa(t,j) * beta(t,j) * priznaky(t,:)); 
            mean_denominator = mean_denominator + (alfa(t,j) * beta(t,j)); 
        end
        mean_denominator = (mean_denominator * ones(13,1))';
        new_mean = mean_numerator ./ mean_denominator;  
        new_means(j-1, :) = new_mean;  
        new_means_cell{j-1} = new_mean; 
        
        mean_denominator = 0; 
        mean_numerator = 0; 
    end
    
     
 

    % vypocet novych varianci 
    new_variances = []; 

    var_numerator = 0; 
    var_denominator = 0;

    for j = 2:1:pocet_neemitujicich_stavu
        for t = 1:1:T
            soucin_vektoru = (priznaky(t,:) - new_means(j-1,:)') .* ((priznaky(t,:) - new_means(j-1,:)'))'; 
            var_numerator = var_numerator + (alfa(t,j) * beta(t,j) * soucin_vektoru); 
            var_denominator = var_denominator + (alfa(t,j) * beta(t,j)); 
        end
        var_denominator = (var_denominator * ones(13,1))';
        new_cov = var_numerator ./ var_denominator; % kovariancni matice -> z hlavni diagonaly ziskam variance
        new_variances(j-1, :) = diag(new_cov);   

        var_denominator = 0; 
        var_numerator = 0; 
    end
    
    output_variances = new_variances; 
    

    % nove pravdepodobnosti prechodu a_ij
    suma_num_a_ij = 0; 
    suma_denom_a_ij = 0; 
    a = []; 


    for i = 2:1:pocet_neemitujicich_stavu
        for j = 2:1:pocet_neemitujicich_stavu
            for t1 = 1:1:T-1
                suma_num_a_ij = suma_num_a_ij + alfa(t1,i) * prechody_ppst(i,j) * N(t1+1, j) * beta(t1+1, j);
            end

            for t2 = 1:1:T
               suma_denom_a_ij = suma_denom_a_ij + alfa(t2,i) * beta(t2,i); 
            end

            a(i,j) = suma_num_a_ij / suma_denom_a_ij;
            suma_denom_a_ij = 0; 
            suma_num_a_ij = 0; 
        end
    end
    

    % nove a_{iN}
    denominator_a_iN = 0; 

    for i = 2:1:pocet_neemitujicich_stavu
        numerator_a_iN = alfa(T,i) * beta(T,i); 
        for t = 1:1:T
            denominator_a_iN = denominator_a_iN + (alfa(t,i) * beta(t,i));
        end
        a(i,pocet_neemitujicich_stavu+1) = numerator_a_iN / denominator_a_iN;
        denominator_a_iN = 0; 
    end

    a(1,2) = A(1,2); 
    a = [a; zeros(1,5)]; 
end

