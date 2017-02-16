clear all
close all

lx= 1.2 % model length
lz= 1 % model depth
dx= 0.01 % sampling interval in x direction
dz= 0.01 % sampling interval in z direction 
ax= 1 % correlation length in x direction
az= 10; % correlation length in z direction
nu= 0.5; % Hurst number

stoch_model = stochmod(lz,lx,dz,dx,ax,az,nu,randi(100000,1));

imagesc(stoch_model)
axis equal
axis tight

%save('stoch_model.mat','stoch_model','-v7.3')