import numpy as np
import matplotlib.pyplot as plt
import openmc
from sparcnx.materials import tungsten, flibe, lead, inconel_625

# Radii Parameters
R0 = 370
a = 114
t_fw = 2
t_vv1 = 2
t_mult = 3
t_vv2 = 2
t_blanket = 125
Rboundary = 1000

# Material Parameters
plasma_mat = None
fw_mat = flibe
vv_mat = flibe
mult_mat = flibe
blanket_mat = flibe
outside_mat = None
materials = [plasma_mat, fw_mat, vv_mat, mult_mat, blanket_mat, outside_mat]
materials = openmc.Materials([mat for mat in set(materials) if mat is not None])

# Surfaces
cyl0 = openmc.YCylinder(x0=R0, r=a)
cyl1 = openmc.YCylinder(x0=R0, r=a+t_fw)
cyl2 = openmc.YCylinder(x0=R0, r=a+t_fw+t_vv1)
cyl3 = openmc.YCylinder(x0=R0, r=a+t_fw+t_vv1+t_mult)
cyl4 = openmc.YCylinder(x0=R0, r=a+t_fw+t_vv1+t_mult+t_vv2)
cyl5 = openmc.YCylinder(x0=R0, r=a+t_fw+t_vv1+t_mult+t_vv2+t_blanket)
sph1 = openmc.Sphere(r=Rboundary, boundary_type='reflective')
plane1 = openmc.YPlane(boundary_type='reflective').rotate((0, 0, -5))
plane2 = openmc.YPlane(boundary_type='reflective').rotate((0, 0, 5))

wedge = +plane1 & -plane2

# Regions
plasma_reg = -cyl0 & wedge
fw_reg = +cyl0 & -cyl1 & wedge
vv1_reg = +cyl1 & -cyl2 & wedge
mult_reg = +cyl2 & -cyl3 & wedge
vv2_reg = +cyl3 & -cyl4 & wedge
blanket_reg = +cyl4 & -cyl5 & wedge
outside_reg = +cyl5 & wedge & -sph1

# Cells
plasma = openmc.Cell(region=plasma_reg, fill=plasma_mat, name='plasma')
first_wall = openmc.Cell(region=fw_reg, fill=fw_mat, name='first_wall')
vv1 = openmc.Cell(region=vv1_reg, fill=vv_mat, name='vv_inner_shell')
multiplier = openmc.Cell(region=mult_reg, fill=mult_mat, name='multiplier')
vv2 = openmc.Cell(region=vv2_reg, fill=vv_mat, name='vv_outer_shell')
blanket = openmc.Cell(region=blanket_reg, fill=blanket_mat, name='blanket')
outside = openmc.Cell(region=outside_reg, fill=outside_mat, name='outside')
cells = [plasma, first_wall, vv1, multiplier, vv2, blanket, outside]

univ = openmc.Universe(cells=cells)
univ.plot(origin=(370, 0, 0), width=(800, 800), pixels=(400,400), basis='xy')
plt.gca().set_xlabel('X (cm)')
plt.gca().set_ylabel('Y (cm)')
plt.show()
geometry = openmc.Geometry(univ)
geometry.remove_redundant_surfaces()

# Settings
settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.batches = 10
settings.inactive = 0
settings.particles = int(1E5)
phisrc = openmc.stats.Uniform(a=-5/np.pi/180, b=5*np.pi/180)
rsrc = openmc.stats.Discrete([370], [1.])
thetasrc = openmc.stats.Discrete([np.pi/2], [1.])
ring = openmc.stats.SphericalIndependent(rsrc, thetasrc, phisrc)
#phisrc = openmc.stats.Uniform(a=-5/np.pi/180, b=5*np.pi/180)
#rsrc = openmc.stats.Discrete([370], [1.])
#zsrc = openmc.stats.Discrete([0], [1.])
#ring = openmc.stats.CylindricalIndependent(rsrc, phisrc, zsrc)

src = openmc.Source(space=ring)
src.strength = 1
src.energy = openmc.stats.Discrete([14.1E6], [1.0])
settings.source = src
settings.photon_transport = False

# Build filters and tallies for simulation and export to xml
t = openmc.Tally(name='flux')
t1 = openmc.Tally(name='tbr')
t2 = openmc.Tally(name='heating')

par_filter = openmc.ParticleFilter(['neutron', 'photon', 'electron',
                                    'positron'])
par_filter2 = openmc.ParticleFilter(['neutron', 'photon'])
cell_filter = openmc.CellFilter(cells)

# Specify filters and scores for flux tally
t.filters = [cell_filter]
t.scores = ['flux']
t1.filters = [cell_filter]
t1.scores = ['(n,Xt)', '(n,2n)']
t1.nuclides = ['all']
t2.filters = [cell_filter]
t2.scores = ['heating-local']

tallies = openmc.Tallies([t, t1, t2])

materials.export_to_xml()
geometry.export_to_xml()
settings.export_to_xml()
tallies.export_to_xml()
openmc.run()

