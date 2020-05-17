from __future__ import print_function
from fenics import *
from mshr import *
import matplotlib.pyplot as plt


# Create mesh
R = 1. # radius
N = 20 # mesh density
domain = Circle(Point(0., 0.), R)
mesh = generate_mesh(domain, N)
#plot(mesh,linewidth=0.3)


#define function space, function u, and test function v
degreeElements = 3
FS = FunctionSpace(mesh, 'Lagrange', degreeElements)
u = Function(FS)
v = TestFunction(FS)

# define functions a and f
a  = Expression('1-0.5*(x[0]*x[0]+x[1]*x[1])', degree=degreeElements)
f  = 1

# define function g
class G(UserExpression):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def eval_cell(self, value, x, ufc_cell):
        value[0]=x[1]

g  = G(degree=degreeElements)


#impose Dirichlet boundary conditions
def right_boundary(x, on_boundary):
    return on_boundary and x[0]>=0

uD = Expression('x[0]',degree=degreeElements)
bc = DirichletBC(FS, uD, right_boundary)

# weak formulation of the problem
Res = a*dot(grad(u), grad(v))*dx - f*v*dx - g*v*ds

# solve the problem
solve(Res == 0, u, bc)

# plot solution
c = plot(u,mode='color',title='$u$')
plt.colorbar(c)
plot(mesh,linewidth=0.3)
plt.show()

# plot a*grad(u)
VFS = VectorFunctionSpace(mesh, 'Lagrange', degreeElements)
sigma=project(a*grad(u),VFS)
c=plot(sigma,title='$a \\nabla u$',width=.008)
plt.colorbar(c)
plot(mesh,linewidth=0.3)
plt.show()

# plot solution for div(a*grad(u))
divSigma = project(div(sigma), FS)
c=plot(divSigma,mode='color',title='$\\nabla \cdot (a \\nabla u)$',vmin=-1.1,vmax=-0.9)
plt.colorbar(c)
plot(mesh,linewidth=0.3)
plt.show()
