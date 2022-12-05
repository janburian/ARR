function [hodnota] = OneFilter(frekvenceHz, cisloFiltru, bm)
hodnota = 0; 

if ((bm(cisloFiltru) < frekvenceHz) && (frekvenceHz <= bm(cisloFiltru + 1)))
    hodnota = (frekvenceHz - bm(cisloFiltru)) / (bm(cisloFiltru + 1) - bm(cisloFiltru));
end

if ((bm(cisloFiltru + 1) < frekvenceHz) && (frekvenceHz <= bm(cisloFiltru + 2)))
    hodnota = (frekvenceHz - bm(cisloFiltru + 2)) / (bm(cisloFiltru + 1) - bm(cisloFiltru + 2));
end

%FILTERS Summary of this function goes here
%   hranice vektor hranic filtru 
%   cisloFiltru - ktery filtr vybirame
%   Hz 


