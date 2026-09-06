import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import FancyBboxPatch

VIEWS = [
    ("contender_quadrant.png", "Full Season  (all opponents)"),
    ("form_window.png",        "Last 10 Rounds  (all opponents)"),
    ("form_window_5.png",      "Last 5 Rounds  (all opponents)"),
    ("form_vs_top10.png",      "Last 10 Rounds  (vs Top 10 only)"),
    ("form_vs_top10_5.png",    "Last 5 Rounds  (vs Top 10 only)"),
]

present = [(f, c) for f, c in VIEWS if os.path.exists(f)]
n = len(present)
print("Found", n, "images:", [f for f, _ in present])
if n == 0:
    raise SystemExit("No images found - run the individual scripts first.")

BG = "#0E1117"
ncols = 3
nrows = (n + 1 + ncols - 1) // ncols  # +1 leaves room for the analysis panel

fig, axes = plt.subplots(nrows, ncols, figsize=(ncols*6, nrows*4.6))
fig.patch.set_facecolor(BG)
axes = axes.flatten()
for ax in axes:
    ax.axis("off")

for ax, (fname, caption) in zip(axes, present):
    ax.imshow(mpimg.imread(fname))
    ax.set_title(caption, color="#FFFFFF", fontsize=12, fontweight="bold", pad=8)

# --- Analysis panel in the next empty cell ---
panel = axes[n]
panel.set_facecolor(BG)
panel.add_patch(FancyBboxPatch((0.03, 0.03), 0.94, 0.94,
                boxstyle="round,pad=0.02,rounding_size=0.03",
                facecolor="#141A24", edgecolor="#2A2F3A", lw=1,
                transform=panel.transAxes, zorder=0))

panel.text(0.5, 0.93, "Reading the five lenses", transform=panel.transAxes,
           color="#FFFFFF", fontsize=15, fontweight="bold", ha="center", va="top")

lines = [
    ("As the lens tightens (fewer rounds,", "#AEB4C0", False),
    ("tougher opponents) the contender zone", "#AEB4C0", False),
    ("shifts. That movement is the story:", "#AEB4C0", False),
    ("", "#AEB4C0", False),
    ("Carlton & Brisbane", "#1DB954", True),
    ("Outside the season zone, inside every form", "#AEB4C0", False),
    ("view. The clearest 'peaking now' signal.", "#AEB4C0", False),
    ("", "#AEB4C0", False),
    ("Sydney", "#ED4040", True),
    ("#1 all season, but slides out once you count", "#AEB4C0", False),
    ("only top-10 opponents. Padded on weak sides.", "#AEB4C0", False),
    ("", "#AEB4C0", False),
    ("Collingwood", "#FFFFFF", True),
    ("The reverse: absent from the raw form zone,", "#AEB4C0", False),
    ("but turns up against top-10 teams. Big-game.", "#AEB4C0", False),
    ("", "#AEB4C0", False),
    ("The constants: Fremantle, Geelong, Carlton", "#FBBF15", True),
    ("Hold the zone in nearly every lens.", "#AEB4C0", False),
    ("", "#AEB4C0", False),
    ("Small samples in the last-5 / top-10 views:", "#6A707C", False),
    ("read as signal, not gospel.", "#6A707C", False),
]

y = 0.83
for text, colour, bold in lines:
    panel.text(0.08, y, text, transform=panel.transAxes, color=colour,
               fontsize=10.5, fontweight="bold" if bold else "normal", va="top", ha="left")
    y -= 0.041

for ax in axes[n+1:]:
    ax.axis("off")

fig.suptitle("2026 AFL Contender Views  \u2014  Season to Finals Form",
             color="#FFFFFF", fontsize=20, fontweight="bold", y=0.995)
fig.text(0.5, 0.008,
         "The zone tightens as the lens does: who holds up late, and against the good sides.  \u00b7  Built by Sai Surapaneni",
         color="#8A909C", fontsize=11, ha="center")

plt.tight_layout(rect=[0, 0.02, 1, 0.97])
plt.savefig("comparison.png", dpi=150, facecolor=BG, bbox_inches="tight")
print("Saved comparison.png")