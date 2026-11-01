---
name: marazawa-architectural-particles
description: Create a lightweight Canvas particle field that morphs from scattered points into architectural networks and conceptual contours. Use for decorative brand atmospheres with mobile and accessibility constraints.
---

# A field of relationships

Let the geometry refer to the product: individual points become relationships and a shared space. Use a small deterministic point set, not customer records, names, locations or tracking data. The animation is conceptual; do not label it as a real village plan, GIS analysis or terrain model.

## Reference construction

Use one pointer-transparent, `aria-hidden` canvas with fixed viewport dimensions. Keep the layer subtle enough that text and inputs remain readable.

1. Generate 46 points for a desktop story, 22 for mobile/workspaces.
2. Position scattered points near the side margins initially.
3. Interpolate toward a loose grid as document scroll progress increases. Add a small sinusoidal drift.
4. Connect only pairs nearer than `min(135px, viewportWidth * 0.32)` with distance-weighted alpha. Avoid a dense full mesh.
5. Add a few sinusoidal contour lines on story pages. Suppress these behind detailed workspaces.

Cap device-pixel ratio at 1.5. Target roughly 30fps desktop and 20fps mobile, reduce count before increasing detail, and clear the canvas on stop. Never alter content layout to position particles.

## Interaction and accessibility

Mouse response should be a tiny offset; touch must not drag the particle field instead of scrolling. Set `pointer-events: none`. Stop animation in hidden tabs, on pagehide, by the user's motion control and for reduced-motion preference. Match day/night contrast without using a glow over body text. Static empty background is the valid fallback if Canvas fails.

The reference implementation uses custom Canvas rather than tsParticles or Three.js. [tsParticles documentation](https://particles.js.org/) is an optional source for a later richer engine; do not claim it is installed when it is not.

## Verify

Check frame cost, a slow phone, readable fields, dark backgrounds, resize, device rotation and return from a background tab. A screenshot documents appearance; behavioral pause and rendering checks are also required.
