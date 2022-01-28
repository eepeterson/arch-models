import numpy as np
import openmc
import matplotlib.pyplot as plt

def three_circleD(R0, R1, alpha=0.5):
    """Three "D" parametric model of a torus

    Parameters
    ----------
    R0: float
        inboard limit of D
    R1: float
        outboard limit of D
    alpha: float [0,1]
        ratio of radii r/R alpha=1 is circular, alpha=0 is no radius on top of D

    """
    print(R0, R1)
    r = alpha*(R1 - R0)/(1 + alpha)
    R = (R1 - R0)/(1 + alpha)
    x0 = R0 + r
    z0 = R - r
    small_cyl_top = openmc.YCylinder(x0=x0, z0=z0, r=r)
    small_cyl_bot = openmc.YCylinder(x0=x0, z0=-z0, r=r)
    big_cyl = openmc.YCylinder(x0=x0, z0=0, r=R)
    xplane0 = openmc.XPlane(R0)
    xplane1 = openmc.XPlane(x0)
    zplane0 = openmc.ZPlane(-z0) 
    zplane1 = openmc.ZPlane(z0) 
    post = +xplane0 & -xplane1 & +zplane0 & -zplane1
    bigD = +xplane1 & -big_cyl
    insideD = -small_cyl_top | -small_cyl_bot | post | bigD

    return insideD

def nested_Ds(R0_list, deltaR, alpha=0.5):
    R0_list_rev = np.array(R0_list[::-1])
    print(R0_list_rev)
    R1_list_rev = 2*R0_list_rev[0] - R0_list_rev + deltaR
    print(R1_list_rev)
    D_regions = [three_circleD(R0, R1, alpha=alpha)
                 for R0, R1 in zip(R0_list_rev, R1_list_rev)]
    nested_regions = []
    for i, reg in enumerate(D_regions):
        if i == 0:
            nested_regions.append(reg)
        else:
            nested_regions.append(reg & ~nested_regions[i-1])

    nested_regions.append(~D_regions[-1])

    return nested_regions

# Region names: air core, CS, TF, shield, blanket tank, blanket, LSVV, plasma
Rinboard = [65, 145, 195, 265, 275, 285, 295]
deltaR = 115*2 + 217
alpha = 0.5

plasma, lsvv, blanket, tank, shield, tf, cs, outside = nested_Ds(Rinboard,
                                                                 deltaR,
                                                                 alpha=alpha)

plasmacell = openmc.Cell(region=plasma, fill=None)
lsvvcell = openmc.Cell(region=lsvv, fill=None)
blanketcell = openmc.Cell(region=blanket, fill=None)
tankcell = openmc.Cell(region=tank, fill=None)
shieldcell = openmc.Cell(region=shield, fill=None)
tfcell = openmc.Cell(region=tf, fill=None)
cscell = openmc.Cell(region=cs, fill=None)
outsidecell = openmc.Cell(region=outside, fill=None)

cells = [plasmacell, lsvvcell, blanketcell, tankcell, shieldcell, tfcell,
         cscell, outsidecell]

univ = openmc.Universe(cells=cells)
geom = openmc.Geometry(univ)

univ.plot(origin=(600,0,0), width=(1200, 1200), basis='xz')
plt.show()



