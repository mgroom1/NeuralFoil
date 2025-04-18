import aerosandbox as asb
import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p


def draw(
    ax,
    airfoil,
    Re,
    delta_alpha,
    title="",
):
    plt.sca(ax)
    plt.fill(
        airfoil.x(),
        airfoil.y(),
        facecolor=(0, 0, 0, 0.2),
        linewidth=1,
        edgecolor=(0, 0, 0, 0.7),
    )
    plt.axis("equal")
    # plt.axis('off')
    plt.text(
        0.5,
        0.9,
        f"$\\mathrm{{Re}}_\\mathrm{{c}}$ = {Re:.0f}\n$\\Delta\\alpha$ = {delta_alpha:.1f}°",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=8,
        color="black",
        bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.2"),
    )
    plt.title(title, fontsize=10)


af0 = asb.Airfoil("naca0012").set_TE_thickness(0)
af1 = af0.add_control_surface(deflection=15, hinge_point_x=0.7)
d = af1.normalize(return_dict=True)
af2 = d["airfoil"].to_kulfan_airfoil()

fig, ax = plt.subplots(
    1,
    3,
    figsize=(6.5, 2.1),
    # sharey=True
)
Re0 = 1e6
draw(ax[0], af0, Re0, 0, title="Step 1:\nOriginal Airfoil")
draw(ax[1], af1, Re0, 0, title="Step 2:\nDeflected Airfoil")
draw(
    ax[2],
    af2,
    Re0 * d["scale_factor"],
    d["rotation_angle"],
    title="Step 3:\nNormalized Airfoil",
)

# Set all tick fontsizes
for a in ax:
    a.tick_params(labelsize=8)
    a.set_xlabel("x/c", fontsize=10)

ax[0].set_ylabel("y/c", fontsize=10)
for a in ax[1:]:
    a.set_yticklabels([])

plt.tight_layout()
# Arrows between adjacent axes
for i in range(2):
    # arrow1_2 = plt.annotate('', xy=(-0.1, 0.5), xycoords=ax2.transAxes, xytext=(1.1, 0.6), textcoords=ax1.transAxes,                            arrowprops=arrowprops)
    plt.annotate(
        "",
        xy=(-0.03, 0.5),
        xycoords=ax[i + 1].transAxes,
        xytext=(1.03, 0.5),
        textcoords=ax[i].transAxes,
        arrowprops=dict(arrowstyle="->", color="black", lw=1),
    )

plt.subplots_adjust(
    wspace=0.3,
)

p.show_plot(tight_layout=False, savefig="control_surface_decomposition.svg")
