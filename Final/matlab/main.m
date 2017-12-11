 % clear out any old variables sitting around
clear all

%% Run Feedback Loop
% initial concentrations (y1, y2, y3, y4, y5, y6, y7)
yinit = [1, 1, 1, 1, 1, 1, 1]; % units in nM

% parameters
v1b = 9;
k1b = 1;
k1i = .56;
c = .01;
p = 8;
k1d = .12;
k2b = .3;
q = 2;
k2d = .05;
k2t = .24;
k3t = .02;
k3d = .12;
v4b = 3.6;
k4b = 2.16;
r = 3;
k4d = .75;
k5b = .24;
k5d = .06;
k5t = .45;
k6t = .06;
k6d = .12;
k6a = .09;
k7a = .003;
k7d = .09;

params = [v1b, k1b, k1i, c, p, k1d, k2b, q, k2d, k2t, k3t, k3d, v4b, k4b, ...
            r, k4d, k5b, k5d, k5t, k6t, k6d, k6a, k7a, k7d];

% (function handle, time array, initial conditions, additional ode15s params, parameters)
options = odeset('RelTol',1e-6, 'AbsTol',1e-8);

tic;
[~,~] = ode23( @feedback_loop, 0:0.1:1000, yinit, [], params );
ode23time = toc;
tic;
[~,~] = ode45( @feedback_loop, 0:0.1:1000, yinit, [], params );
ode45time = toc;
tic;
[~,~] = ode23s( @feedback_loop, 0:0.1:1000, yinit, [], params );
ode23stime = toc;
tic;
[~,y] = ode15s( @feedback_loop, 0:0.1:1000, yinit, [], params );
ode15stime = toc;

ode23time
ode45time
ode23stime
ode15stime

[t,y] = ode15s( @feedback_loop, 0:0.1:50, y(end,:), [], params );

figure;

plot( t, y(:,1), 'r--' );
hold on;
plot( t, y(:,3), 'r' );
plot( t, y(:,4), 'g--' );
plot( t, y(:,7), 'g' );
plot( t, y(:,5) + y(:,6) + y(:,7), 'b' );
%plot( t, y(:,6), 'Color', 'k' );
%plot( t, y(:,7), 'Color', 'y' );
legend( { 'Per2/CRY mRNA','Per2/CRY complex in nucleus','Bmal1 mRNA', ...
            'transcriptionally active BMAL1*', 'total BMAL1 protein'} );
title('Feedback Loop of PER');
xlabel('time (s)');
ylabel('concentration (nM)');