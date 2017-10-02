 % clear out any old variables sitting around
clear all

%% Run dimerization simulation
% initial concentrations (P1, P2, P1P2)
yinit = [2, 3, 1]; % units in nM

% parameters
k1 = 1; % dimerization rate (in units of nM^-1s^-1)
k2 = 2; % de-dimerization rate (in units of s^-1)
params = [k1,k2];

% (function handle, time array, initial conditions, additional ode15s params, parameters)
[t,y] = ode15s( @dimer_v1, 0:0.01:10, yinit, [], params );

figure;

plot( t, y(:,1), 'Color', 'r' );
hold on;
plot( t, y(:,2), 'Color', 'b' );
plot( t, y(:,3), 'Color', 'm' );
legend( { 'P1','P2','P1P2'} );
title('Dimerization of P1 and P2 into P1P2');
xlabel('time (s)');
ylabel('concentration (nM)');

%% Run dimerization with degradation simulation
% initial concentrations (P1, P2, P1P2)
yinit = [2, 3, 1]; % units in nM

% parameters
k1 = 1; % dimerization rate (in units of nM^-1s^-1)
k2 = 2; % de-dimerization rate (in units of s^-1)
d1 = 1; % degradation rate of P1 (in units of s^-1)
d2 = 1; % degradation rate of P2 (in units of s^-1)
d3 = 1; % degradation rate of P1P2 (in units of s^-1)
params = [k1,k2,d1,d2,d3];

% (function handle, time array, initial conditions, additional ode15s params, parameters)
[t,y] = ode15s( @dimer_w_degr_v1, 0:0.01:10, yinit, [], params );

figure;
plot( t, y(:,1), 'Color', 'r' );
hold on;
plot( t, y(:,2), 'Color', 'b' );
plot( t, y(:,3), 'Color', 'm' );
legend( { 'P1','P2','P1P2'} )
title('Dimerization of P1 and P2 into P1P2 with Degradation');
xlabel('time (s)');
ylabel('concentration (nM)');
