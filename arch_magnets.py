import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc, Ellipse, PathPatch


tf_r0 = 194
tf_b = 160
tf_x0 = tf_r0 + tf_b
tf_y0 = 272
tf_a = 388
tf_w = 50

a = 115
R0 = 410

lsvvw = 2

csh = 570
csir = 80

# EF coil centroids, heights, widths
ef1lr, ef1lz, ef1lw, ef1lh = 235, -285, 42, 42
ef1ur, ef1uz, ef1uw, ef1uh = 235, 285, 42, 42
ef2lr, ef2lz, ef2lw, ef2lh = 380, -355, 32, 32
ef2ur, ef2uz, ef2uw, ef2uh = 380, 355, 32, 32
ef3lr, ef3lz, ef3lw, ef3lh = 440, -355, 32, 32
ef3ur, ef3uz, ef3uw, ef3uh = 440, 355, 32, 32
ef4lr, ef4lz, ef4lw, ef4lh = 585, -285, 45, 45
ef4ur, ef4uz, ef4uw, ef4uh = 585, 285, 45, 45
ef5lr, ef5lz, ef5lw, ef5lh = 685, -67.5, 18, 18
ef5ur, ef5uz, ef5uw, ef5uh = 685, 67.5, 18, 18

tank_rz = [(280, 250), (350, 305), (510, 305), (575, 235), (635, 235),
           (635, -235), (575, -235), (510, -305), (350, -305), (280, -250),
           (280, 250)]

tank = PathPatch(mpl.path.Path(tank_rz, closed=True), fill=False, zorder=2)

arc_u = Arc((tf_x0, tf_y0), 2*tf_b, 2*tf_b, theta1=90., theta2=180.)
arc_l = Arc((tf_x0, -tf_y0), 2*tf_b, 2*tf_b, theta1=180., theta2=270.)
arc_o = Arc((tf_x0, 0.), 2*tf_a, 2*(tf_b+tf_y0), theta1=270., theta2=90.)
arc_uo = Arc((tf_x0, tf_y0), 2*(tf_b+tf_w), 2*(tf_b+tf_w), theta1=90., theta2=180.)
arc_lo = Arc((tf_x0, -tf_y0), 2*(tf_b+tf_w), 2*(tf_b+tf_w), theta1=180., theta2=270.)
arc_oo = Arc((tf_x0, 0.), 2*(tf_a+tf_w), 2*(tf_b+tf_y0+tf_w), theta1=270., theta2=90.)

ef1l = Rectangle((ef1lr-ef1lw/2, ef1lz-ef1lh/2), ef1lw, ef1lh)
ef1u = Rectangle((ef1ur-ef1uw/2, ef1uz-ef1uh/2), ef1uw, ef1uh)
ef2l = Rectangle((ef2lr-ef2lw/2, ef2lz-ef2lh/2), ef2lw, ef2lh)
ef2u = Rectangle((ef2ur-ef2uw/2, ef2uz-ef2uh/2), ef2uw, ef2uh)
ef3l = Rectangle((ef3lr-ef3lw/2, ef3lz-ef3lh/2), ef3lw, ef3lh)
ef3u = Rectangle((ef3ur-ef3uw/2, ef3uz-ef3uh/2), ef3uw, ef3uh)
ef4l = Rectangle((ef4lr-ef4lw/2, ef4lz-ef4lh/2), ef4lw, ef4lh)
ef4u = Rectangle((ef4ur-ef4uw/2, ef4uz-ef4uh/2), ef4uw, ef4uh)
ef5l = Rectangle((ef5lr-ef5lw/2, ef5lz-ef5lh/2), ef5lw, ef5lh)
ef5u = Rectangle((ef5ur-ef5uw/2, ef5uz-ef5uh/2), ef5uw, ef5uh)

lsvv = Ellipse((R0, 0), 2*(a+lsvvw), 4*a+2*lsvvw, color='k', zorder=1)
plasma = Ellipse((R0, 0), 2*a, 4*a, color='m', zorder=2)

cs = Rectangle((csir, -csh/2), tf_r0-tf_w-csir, csh)
hx = Rectangle((600, -235), 35, 470, color='C1', zorder=1)

patches = [arc_u, arc_l, arc_o, ef1l, ef1u, ef2l, ef2u, ef3l, ef3u, ef4l, ef4u,
           ef5l, ef5u, lsvv, plasma, tank, arc_uo, arc_lo, arc_oo, cs, hx]

fig, ax = plt.subplots()
ax.set_xlim(0, 800)
ax.set_ylim(-500, 500)
ax.set_aspect(1)
for p in patches:
    ax.add_patch(p)
ax.axvline(x=tf_r0, ymin=-tf_y0/1000+0.5, ymax=tf_y0/1000+0.5, color='k')
ax.axvline(x=tf_r0-tf_w, ymin=-tf_y0/1000+0.5, ymax=tf_y0/1000+0.5, color='k')
ax.set_xlabel('R (cm)')
ax.set_ylabel('Z (cm)')
plt.show()


