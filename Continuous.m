nx=101;
nz=101;

x=-5:.1:5;
z=linspace(.6,10.6,101);
sensitivity=zeros(101);
datax=-1.22;
for i=1:nx
    for j=1:nz
        sensitivity(j,i)=z(j)/((x(i)-datax)^2+z(j)^2);
    end
end

% histeq

mplot=sensitivity;
% mplot=padarray(sensitivity,[1,1],'post');
pcolor(x,z,mplot);
set(gca,'ydir','reverse')
axis square;