"""
Generate SVG minimap images for each LILA BLACK map.
These look like real extraction shooter minimaps: terrain, roads, buildings, POIs.
Image size: 1024x1024. World space: [-8192, 8192] on both axes.
Y-axis: world Y+ = up (north), image Y+ = down — so we flip Y.
"""

import os

def world_to_px(wx, wy, img_size=1024, world_range=16384):
    """Convert world coords to image pixel coords (with Y-flip)."""
    px = (wx + 8192) / world_range * img_size
    py = (1 - (wy + 8192) / world_range) * img_size  # Y-flip
    return round(px, 1), round(py, 1)


def ashveld_svg():
    """Industrial/urban extraction map with a central town, quarry, farmlands."""
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">']
    svg.append('<defs>')
    svg.append('<filter id="blur2"><feGaussianBlur stdDeviation="2"/></filter>')
    svg.append('</defs>')

    # Background terrain
    svg.append('<rect width="1024" height="1024" fill="#1a2010"/>')

    # Open fields (lighter green patches)
    fields = [
        (200, 300, 150, 100), (600, 150, 120, 80), (700, 500, 100, 90),
        (100, 650, 200, 120), (400, 750, 180, 80), (800, 300, 100, 60),
    ]
    for x, y, w, h in fields:
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#243015" rx="10"/>')

    # Roads / paths (tan/beige lines)
    road_color = "#3d3520"
    svg.append(f'<line x1="512" y1="0" x2="512" y2="1024" stroke="{road_color}" stroke-width="8" opacity="0.7"/>')
    svg.append(f'<line x1="0" y1="512" x2="1024" y2="512" stroke="{road_color}" stroke-width="8" opacity="0.7"/>')
    svg.append(f'<line x1="100" y1="200" x2="700" y2="600" stroke="{road_color}" stroke-width="6" opacity="0.5"/>')
    svg.append(f'<line x1="800" y1="100" x2="300" y2="800" stroke="{road_color}" stroke-width="5" opacity="0.4"/>')
    svg.append(f'<line x1="200" y1="400" x2="850" y2="400" stroke="{road_color}" stroke-width="5" opacity="0.4"/>')

    # River
    svg.append('<path d="M 50 300 Q 200 350 300 400 Q 400 450 350 550 Q 300 620 200 680 Q 100 720 50 800" fill="none" stroke="#1a3a4a" stroke-width="18" opacity="0.8"/>')

    # Irongate (town center) at world (-2000, 1500) -> px
    ix, iy = world_to_px(-2000, 1500)
    svg.append(f'<rect x="{ix-30}" y="{iy-30}" width="60" height="60" fill="#2a2520" rx="4"/>')
    svg.append(f'<rect x="{ix-20}" y="{iy-20}" width="15" height="15" fill="#3a3028"/>')
    svg.append(f'<rect x="{ix}" y="{iy-20}" width="15" height="15" fill="#3a3028"/>')
    svg.append(f'<rect x="{ix-20}" y="{iy}" width="15" height="15" fill="#3a3028"/>')
    svg.append(f'<rect x="{ix}" y="{iy}" width="15" height="15" fill="#3a3028"/>')
    svg.append(f'<circle cx="{ix}" cy="{iy}" r="35" fill="none" stroke="#5a5040" stroke-width="2" opacity="0.6"/>')

    # Clocktower at (500, 800)
    cx, cy = world_to_px(500, 800)
    svg.append(f'<rect x="{cx-8}" y="{cy-20}" width="16" height="30" fill="#333028"/>')
    svg.append(f'<rect x="{cx-12}" y="{cy-5}" width="24" height="15" fill="#2a2820"/>')
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="20" fill="none" stroke="#4a4535" stroke-width="1.5" opacity="0.6"/>')

    # Old Mill at (3500, -2000)
    mx, my = world_to_px(3500, -2000)
    svg.append(f'<rect x="{mx-18}" y="{my-18}" width="36" height="36" fill="#2e2a1a"/>')
    svg.append(f'<line x1="{mx}" y1="{my-30}" x2="{mx}" y2="{my+30}" stroke="#3d3825" stroke-width="3"/>')
    svg.append(f'<line x1="{mx-30}" y1="{my}" x2="{mx+30}" y2="{my}" stroke="#3d3825" stroke-width="3"/>')
    svg.append(f'<circle cx="{mx}" cy="{my}" r="22" fill="none" stroke="#4a4030" stroke-width="1.5" opacity="0.5"/>')

    # Quarry at (-5000, -3500)
    qx, qy = world_to_px(-5000, -3500)
    svg.append(f'<ellipse cx="{qx}" cy="{qy}" rx="50" ry="35" fill="#222018" stroke="#3a3520" stroke-width="2"/>')
    svg.append(f'<ellipse cx="{qx}" cy="{qy}" rx="35" ry="22" fill="#1a1a14" stroke="#302e20" stroke-width="1.5"/>')
    svg.append(f'<ellipse cx="{qx}" cy="{qy}" rx="18" ry="10" fill="#151510"/>')

    # Farmstead at (2000, 4000)
    fx, fy = world_to_px(2000, 4000)
    svg.append(f'<rect x="{fx-25}" y="{fy-20}" width="50" height="40" fill="#1e2510"/>')
    for i in range(3):
        svg.append(f'<rect x="{fx-20+i*15}" y="{fy-15}" width="10" height="25" fill="#252d14"/>')
    svg.append(f'<circle cx="{fx}" cy="{fy}" r="30" fill="none" stroke="#3a4020" stroke-width="1.5" opacity="0.5"/>')

    # Bridge at (-500, -1000)
    bx, by = world_to_px(-500, -1000)
    svg.append(f'<rect x="{bx-20}" y="{by-5}" width="40" height="10" fill="#3a3525"/>')
    svg.append(f'<line x1="{bx-20}" y1="{by}" x2="{bx+20}" y2="{by}" stroke="#4a4530" stroke-width="2"/>')

    # Grid overlay (subtle)
    for i in range(0, 1024, 128):
        svg.append(f'<line x1="{i}" y1="0" x2="{i}" y2="1024" stroke="#ffffff" stroke-width="0.5" opacity="0.04"/>')
        svg.append(f'<line x1="0" y1="{i}" x2="1024" y2="{i}" stroke="#ffffff" stroke-width="0.5" opacity="0.04"/>')

    # Map label
    svg.append('<text x="512" y="30" text-anchor="middle" fill="#4a4535" font-size="14" font-family="monospace" opacity="0.6">ASHVELD</text>')
    svg.append('</svg>')
    return '\n'.join(svg)


def craters_edge_svg():
    """Volcanic/industrial map centered on a large crater."""
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">']
    svg.append('<defs>')
    svg.append('<radialGradient id="craterGrad" cx="50%" cy="50%" r="50%">')
    svg.append('<stop offset="0%" stop-color="#0d0808"/>')
    svg.append('<stop offset="40%" stop-color="#1a0e0e"/>')
    svg.append('<stop offset="100%" stop-color="#121520"/>')
    svg.append('</radialGradient>')
    svg.append('</defs>')

    svg.append('<rect width="1024" height="1024" fill="url(#craterGrad)"/>')

    # Lava flows (dark red paths)
    lava_paths = [
        "M 512 512 Q 600 450 700 380 Q 780 320 850 200",
        "M 512 512 Q 420 580 350 650 Q 280 720 200 820",
        "M 512 512 Q 550 600 600 700 Q 640 780 700 900",
        "M 512 512 Q 440 440 360 380 Q 290 320 180 250",
    ]
    for path in lava_paths:
        svg.append(f'<path d="{path}" fill="none" stroke="#3d1010" stroke-width="12" opacity="0.5"/>')
        svg.append(f'<path d="{path}" fill="none" stroke="#5a1a0a" stroke-width="4" opacity="0.3"/>')

    # The Crater (center)
    svg.append('<circle cx="512" cy="512" r="90" fill="#0a0808" stroke="#2a1818" stroke-width="3"/>')
    svg.append('<circle cx="512" cy="512" r="60" fill="#080606" stroke="#1a1010" stroke-width="2"/>')
    svg.append('<circle cx="512" cy="512" r="35" fill="#060404"/>')
    # Crater label ring
    svg.append('<circle cx="512" cy="512" r="100" fill="none" stroke="#3a2020" stroke-width="1.5" stroke-dasharray="6,4" opacity="0.6"/>')

    # Rocky terrain patches
    for (rx, ry, rw, rh) in [(200,200,80,60),(700,250,60,50),(150,700,90,60),(750,700,70,50),(300,850,60,40)]:
        svg.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" fill="#1a1410" rx="8" opacity="0.8"/>')

    # Research Station at (-3500, 2500)
    rsx, rsy = world_to_px(-3500, 2500)
    svg.append(f'<rect x="{rsx-20}" y="{rsy-15}" width="40" height="30" fill="#1a1e28"/>')
    svg.append(f'<rect x="{rsx-5}" y="{rsy-25}" width="10" height="15" fill="#151a20"/>')
    svg.append(f'<circle cx="{rsx}" cy="{rsy}" r="28" fill="none" stroke="#2a3040" stroke-width="1.5" opacity="0.6"/>')

    # Lava Tubes at (4000, -1000)
    ltx, lty = world_to_px(4000, -1000)
    svg.append(f'<ellipse cx="{ltx}" cy="{lty}" rx="40" ry="25" fill="#1a0e0e" stroke="#2a1818" stroke-width="2"/>')
    svg.append(f'<ellipse cx="{ltx}" cy="{lty}" rx="25" ry="15" fill="#100808"/>')
    svg.append(f'<circle cx="{ltx}" cy="{lty}" r="35" fill="none" stroke="#3a2020" stroke-width="1.5" opacity="0.5"/>')

    # Supply Depot at (1500, -4500)
    sdx, sdy = world_to_px(1500, -4500)
    svg.append(f'<rect x="{sdx-22}" y="{sdy-15}" width="44" height="30" fill="#1c1c20"/>')
    for i in range(4):
        svg.append(f'<rect x="{sdx-18+i*10}" y="{sdy-8}" width="7" height="16" fill="#252528"/>')
    svg.append(f'<circle cx="{sdx}" cy="{sdy}" r="30" fill="none" stroke="#303035" stroke-width="1.5" opacity="0.5"/>')

    # Observation Post at (-2000, -2500)
    opx, opy = world_to_px(-2000, -2500)
    svg.append(f'<polygon points="{opx},{opy-20} {opx-15},{opy+15} {opx+15},{opy+15}" fill="#1e1a10"/>')
    svg.append(f'<circle cx="{opx}" cy="{opy}" r="25" fill="none" stroke="#3a3025" stroke-width="1.5" opacity="0.5"/>')

    # Roads (ash-colored)
    svg.append('<line x1="512" y1="0" x2="512" y2="512" stroke="#252020" stroke-width="7" opacity="0.6"/>')
    svg.append('<line x1="512" y1="512" x2="1024" y2="512" stroke="#252020" stroke-width="7" opacity="0.6"/>')
    svg.append('<line x1="0" y1="512" x2="512" y2="512" stroke="#202020" stroke-width="5" opacity="0.4"/>')
    svg.append('<line x1="512" y1="512" x2="512" y2="1024" stroke="#202020" stroke-width="5" opacity="0.4"/>')

    # Grid
    for i in range(0, 1024, 128):
        svg.append(f'<line x1="{i}" y1="0" x2="{i}" y2="1024" stroke="#ffffff" stroke-width="0.5" opacity="0.03"/>')
        svg.append(f'<line x1="0" y1="{i}" x2="1024" y2="{i}" stroke="#ffffff" stroke-width="0.5" opacity="0.03"/>')

    svg.append('<text x="512" y="30" text-anchor="middle" fill="#3a2525" font-size="14" font-family="monospace" opacity="0.6">CRATER\'S EDGE</text>')
    svg.append('</svg>')
    return '\n'.join(svg)


def sundarbans_svg():
    """Tropical delta/mangrove map with waterways and ruins."""
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">']
    svg.append('<defs>')
    svg.append('<filter id="blur3"><feGaussianBlur stdDeviation="3"/></filter>')
    svg.append('</defs>')

    # Water background
    svg.append('<rect width="1024" height="1024" fill="#0e1a1c"/>')

    # Land masses
    svg.append('<ellipse cx="350" cy="400" rx="280" ry="200" fill="#142016" opacity="0.9"/>')
    svg.append('<ellipse cx="700" cy="600" rx="220" ry="180" fill="#142016" opacity="0.9"/>')
    svg.append('<ellipse cx="200" cy="700" rx="150" ry="130" fill="#142016" opacity="0.9"/>')
    svg.append('<ellipse cx="750" cy="250" rx="130" ry="100" fill="#142016" opacity="0.8"/>')
    svg.append('<ellipse cx="500" cy="550" rx="80" ry="60" fill="#122015" opacity="0.7"/>')
    svg.append('<ellipse cx="850" cy="800" rx="120" ry="90" fill="#142016" opacity="0.8"/>')

    # Water channels (darker blue paths)
    channels = [
        "M 0 512 Q 200 480 350 500 Q 500 520 650 510 Q 800 500 1024 520",
        "M 512 0 Q 530 200 510 350 Q 490 500 512 650 Q 530 800 512 1024",
        "M 100 100 Q 200 200 300 350 Q 380 450 450 550",
        "M 900 100 Q 800 250 750 400 Q 700 500 650 600",
    ]
    for ch in channels:
        svg.append(f'<path d="{ch}" fill="none" stroke="#0a1520" stroke-width="20" opacity="0.6"/>')
        svg.append(f'<path d="{ch}" fill="none" stroke="#0e1e28" stroke-width="10" opacity="0.4"/>')

    # Mangrove clusters (dark green blobs)
    mangroves = [(120,180,25),(340,250,30),(600,180,20),(180,550,28),(450,700,22),(680,450,25),(830,350,20)]
    for (mx, my, mr) in mangroves:
        svg.append(f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="#1a2a18" opacity="0.8"/>')
        svg.append(f'<circle cx="{mx+5}" cy="{my-5}" r="{mr*0.6:.0f}" fill="#162416" opacity="0.6"/>')

    # Mangrove Bay at (-4000, 3000)
    mbx, mby = world_to_px(-4000, 3000)
    svg.append(f'<circle cx="{mbx}" cy="{mby}" r="35" fill="#142818" stroke="#1e3520" stroke-width="2"/>')
    svg.append(f'<circle cx="{mbx}" cy="{mby}" r="22" fill="#102010"/>')
    svg.append(f'<circle cx="{mbx}" cy="{mby}" r="40" fill="none" stroke="#2a4028" stroke-width="1.5" opacity="0.6"/>')

    # Floating Market at (1000, 2000)
    fmx, fmy = world_to_px(1000, 2000)
    svg.append(f'<rect x="{fmx-25}" y="{fmy-15}" width="50" height="30" fill="#1e2018" rx="3"/>')
    for i in range(5):
        svg.append(f'<rect x="{fmx-20+i*9}" y="{fmy-20}" width="6" height="10" fill="#252818"/>')
    svg.append(f'<circle cx="{fmx}" cy="{fmy}" r="30" fill="none" stroke="#303520" stroke-width="1.5" opacity="0.6"/>')

    # Tide Gate at (3500, 500)
    tgx, tgy = world_to_px(3500, 500)
    svg.append(f'<rect x="{tgx-15}" y="{tgy-25}" width="30" height="50" fill="#1c1e20"/>')
    svg.append(f'<rect x="{tgx-25}" y="{tgy-8}" width="50" height="16" fill="#181a1c"/>')
    svg.append(f'<circle cx="{tgx}" cy="{tgy}" r="30" fill="none" stroke="#282c30" stroke-width="1.5" opacity="0.6"/>')

    # Ruins at (-1000, -3500)
    rx, ry = world_to_px(-1000, -3500)
    for col in range(3):
        for row in range(2):
            svg.append(f'<rect x="{rx-18+col*14}" y="{ry-15+row*14}" width="10" height="10" fill="#201e14" opacity="{0.5+col*0.1:.1f}"/>')
    svg.append(f'<circle cx="{rx}" cy="{ry}" r="28" fill="none" stroke="#2a2818" stroke-width="1.5" opacity="0.5"/>')

    # Canal Junction at (-2500, 500)
    cjx, cjy = world_to_px(-2500, 500)
    svg.append(f'<circle cx="{cjx}" cy="{cjy}" r="18" fill="#0e1820" stroke="#1a2830" stroke-width="2"/>')
    for angle in [0, 90, 180, 270]:
        import math
        ex = cjx + math.cos(math.radians(angle)) * 35
        ey = cjy + math.sin(math.radians(angle)) * 35
        svg.append(f'<line x1="{cjx}" y1="{cjy}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="#1a2830" stroke-width="8" opacity="0.6"/>')

    # Grid
    for i in range(0, 1024, 128):
        svg.append(f'<line x1="{i}" y1="0" x2="{i}" y2="1024" stroke="#ffffff" stroke-width="0.5" opacity="0.04"/>')
        svg.append(f'<line x1="0" y1="{i}" x2="1024" y2="{i}" stroke="#ffffff" stroke-width="0.5" opacity="0.04"/>')

    svg.append('<text x="512" y="30" text-anchor="middle" fill="#2a3828" font-size="14" font-family="monospace" opacity="0.6">SUNDARBANS DELTA</text>')
    svg.append('</svg>')
    return '\n'.join(svg)


def main():
    os.makedirs("public/minimaps", exist_ok=True)
    maps = [
        ("ashveld.svg", ashveld_svg()),
        ("craters_edge.svg", craters_edge_svg()),
        ("sundarbans.svg", sundarbans_svg()),
    ]
    for fname, content in maps:
        path = f"public/minimaps/{fname}"
        with open(path, "w") as f:
            f.write(content)
        print(f"  Written {path}")
    print("Minimaps done.")


if __name__ == "__main__":
    main()
