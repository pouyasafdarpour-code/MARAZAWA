---
name: marazawa-scroll-choreography
description: Coordinate ScrollTrigger reveals, subtle image parallax and Persian heading motion across marketing pages and workspaces. Use for scroll-linked visual storytelling and responsive motion refinement.
---

# Choreograph a readable story

Choose targets from the actual page structure. Animate section headings, project images and cards; exclude fields, submit/payment buttons, consent rows, hidden panels and open dialogs. Dynamic results can be registered after insertion without resetting a form or duplicating listeners.

## Reference ranges

- Story entrance: 22px to 0, opacity 0.65 to 1, 0.75 seconds, `power2.out`.
- Workspace entrance: 6px to 0 over 0.4 seconds. Prefer stable controls to showy movement.
- Start near `top 94%`, once per element. Do not hide critical content awaiting JavaScript.
- Image parallax: about -1.5% to +1.5%, `scrub: 0.65`, only for appropriate desktop story images. Clip within the image frame and preserve its reserved dimensions.
- A thin noninteractive page-progress line may reflect native document position. It is not form progress and must not be labeled as completed form steps.

Use [official ScrollTrigger documentation](https://gsap.com/docs/v3/Plugins/ScrollTrigger/) for trigger, scrub, refresh and cleanup behavior. Preserve GSAP licensing notices and version pinning.

## Persian text and existing animations

Keep Persian text nodes and their ligatures intact. Reveal a heading as a unit; do not split RTL words into Latin-style letter spans. Use `translate` or isolated decoration for new feedback when an existing card already animates `transform`. Do not replace the existing `transform` blindly.

Make imagery carry relevant meaning. Keep documentary photos labeled separately from AI concepts. Decorative SVG contours must be hidden from accessibility APIs and must not imply a surveyed site or engineering result.

## Lifecycle and validation

Register owned triggers in a collection. On motion pause finish the readable state, then kill owned tweens/triggers and clear inline motion properties where needed. Re-enable without duplicates. Batch dynamic-content registration rather than rescanning on every frame.

Test narrow mobile, day/night, visible links on dark sections, dialog focus and reduced motion. Keep printing static. No scroll-jacking, forced navigation or blocking of native page scrolling.
