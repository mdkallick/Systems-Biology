function dydt = feedback_loop( t, y, params )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
v1b = params(1);
k1b = params(2);
k1i = params(3);
c = params(4);
p = params(5);
k1d = params(6);
k2b = params(7);
q = params(8);
k2d = params(9);
k2t = params(10);
k3t = params(11);
k3d = params(12);
v4b = params(13);
k4b = params(14);
r = params(15);
k4d = params(16);
k5b = params(17);
k5d = params(18);
k5t = params(19);
k6t = params(20);
k6d = params(21);
k6a = params(22);
k7a = params(23);
k7d = params(24);

y1 = y(1);
y2 = y(2);
y3 = y(3);
y4 = y(4);
y5 = y(5);
y6 = y(6);
y7 = y(7);


dydt(1,1) = (v1b * (y7 + c))/((k1b * (1 + ((y3/k1i)^p))) + (y7 + c)) - (k1d * y1);
dydt(2,1) = (k2b * (y1^q)) - (k2d * y2) - (k2t * y2) + (k3t * y3);
dydt(3,1) = (k2t * y2) - (k3t * y3) - (k3d * y3);
dydt(4,1) = ((v4b * (y3^r))/((k4b^r) + (y3^r))) - (k4d * y4);
dydt(5,1) = (k5b * y4) - (k5d * y5) - (k5t * y5) + (k6t * y6);
dydt(6,1) = (k5t * y5) - (k6t * y6) - (k6d * y6) + (k7a * y7) - (k6a * y6);
dydt(7,1) = (k6a *y6) - (k7a * y7) - (k7d * y7);

end

