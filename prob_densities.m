function [N] = prob_densities(priznaky, means, covs)
    for i = 1:length(priznaky)
        for j = 1:1:3
            constant = (1 / sqrt(2 * pi)^13) * (1 / sqrt (det(covs{1,j}))); 
            exponent = -1/2 * ((priznaky(i,:) - means{1,j})) * inv(covs{1,j}) * ((priznaky(i,:) - means{1,j})'); 
            N(i, j) = constant * exp(exponent); 
        end
    end

    N = [zeros(length(priznaky),1) N zeros(length(priznaky),1)];
end

