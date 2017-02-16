function s = stochmod(lz,lx,dz,dx,az,ax,nu,seed);
% lx= model length
% lz= model depth
% dx= sampling interval in x direction
% dz= sampling interval in z direction 
% ax= correlation length in x direction
% az= correlation length in z direction
% nu= Hurst number
% z.B. stochmod(100,100,0.1,0.1,2,10,0.5);

if (lx >= lz)
  n = (round(lx/dx));
else
  n = (round(lz/dz));
end
%
h=1; 
while n > (2^h)
  h=h+1; 
end
n=2^h;

kxnyq = 1/(2*dx);
dkx = 2*kxnyq/n;
kx = [0:dkx:kxnyq]*2*pi;

kznyq = 1/(2*dz);
dkz = 2*kznyq/n;
kz(1:n/2+1) = [0:dkz:kznyq]*2*pi;
kz(n/2+2:n) = [-kznyq+dkz:dkz:-dkz]*2*pi;

ax = round(ax/dx);
az = round(az/dz);

%calculate power spectrum for 1st and 3rd quadrant
for i=1:n/2+1
   for j=1:n
      p(j,i)= (1+(kx(i)*ax).^2+(kz(j)*az).^2).^-(nu+1);
   end
end   
p = sqrt(p);
rand('seed',seed);
% rand('state',740);

p = p .* exp(-sqrt(-1).*(rand(n,n/2+1)-0.5)*2*pi);

%there are 4 points (dc value and 3 other points) without imaginary parts
p(1,1)=real(p(1,1));
p(1,n/2+1)=real(p(1,n/2+1));
p(n/2+1,1)=real(p(n/2+1,1));
p(n/2+1,n/2+1)=real(p(n/2+1,n/2+1));

%enforce symmtry along top and central horizonal axis
p(1,n/2+2:n)=fliplr(conj(p(1,2:n/2)));
p(n/2+1,n/2+2:n)=fliplr(conj(p(n/2+1,2:n/2)));

%enforce symmetry along left and central vertical axis
p(n/2+2:n,1)=flipud(conj(p(2:n/2,1)));
p(n/2+2:n,n/2+1)=flipud(conj(p(2:n/2,n/2+1)));

%enforce symmetries for 2nd and 4th quandrants
p(2:n/2,n/2+2:n)=flipud(fliplr(conj(p(n/2+2:n,2:n/2))));
p(n/2+2:n,n/2+2:n)=flipud(fliplr(conj(p(2:n/2,2:n/2))));

s = real(ifft2(p));
s=s-mean(mean(s));
s=s/max(max(s));
s = s ./ mean(std(s));
s = s(1:(round(lz/dz)+1),1:(round(lx/dx)+1));  % "+1" - Jens

% % Normalization - small grid (Jens):
s=s-mean(mean(s));
s=s/max(max(s));
s = s ./ mean(std(s));


%figure(3)
%imagesc(s);,axis equal,colorbar;

% % Histogramm der Verteilung (Jens)
% for kk=1:(round(lz/dz)+1)
%     start_row = (kk-1)*(round(lx/dx)+1) + 1;
%     end_row = kk*(round(lx/dx)+1);
%     histo_vek(start_row:end_row) = s(kk,:);
% end;
% 
% figure(4)
% hist(histo_vek, 50);
