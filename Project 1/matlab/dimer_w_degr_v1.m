function dydt = dimer_w_degr_v1( t, y, params )
k1 = params(1);
k2 = params(2);
d1 = params(3);
d2 = params(4);
d3 = params(5);

P1 = y(1);
P2 = y(2);
P1P2 = y(3);

dydt(1,1) = k2*P1P2 - k1*P1*P2 - d1*P1;
dydt(2,1) = k2*P1P2 - k1*P1*P2 - d2*P2;
dydt(3,1) = k1*P1*P2 - k2*P1P2 - d3*P1P2;
