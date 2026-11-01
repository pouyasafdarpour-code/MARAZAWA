---
name: marazawa-inertial-scroll
description: Add Lenis inertial scrolling to an existing website while preserving native forms, keyboard navigation, dialogs and mobile touch scrolling. Use for scroll smoothing and Lenis/GSAP integration, not backend changes.
---

# Inertial scroll without disrupting the task

Read the current scroll and modal implementation before adding a second controller. Keep the native document as the scroll surface: do not translate a wrapper around sticky headers, dialogs or form fields.

Use a pinned, locally served Lenis build. Keep its MIT notice. The reference uses 1.3.27 and GSAP/ScrollTrigger 3.15.0; see [official Lenis documentation](https://github.com/darkroomengineering/lenis) for the exact version's API.

## Integration

On a fine pointer, initialize Lenis with `lerp: 0.11`, `smoothWheel: true`, `syncTouch: false`, `anchors: false`. Preserve native anchor/focus behavior unless explicit anchor handling is tested. On coarse pointers, retain native touch scroll. Keep authentication and payment routes native.

Prevent Lenis from handling wheel input inside `textarea`, `input`, `select`, contenteditable regions, dialogs, drawer menus and explicit `data-lenis-prevent` containers. Do not set wheel listeners on these fields yourself.

When GSAP is available:

```js
lenis.on('scroll', ScrollTrigger.update);
const tick = seconds => lenis.raf(seconds * 1000);
gsap.ticker.add(tick);
// Cleanup must remove tick and destroy this Lenis instance.
```

Do not run a competing `autoRaf` loop. Include the recommended Lenis CSS for the pinned version. Apply iframe pointer suppression only while scrolling, never throughout the whole enabled session.

## User control and lifecycle

Offer one persistent display preference, separate from security/account preferences. Honor `prefers-reduced-motion` before initialization and when it changes. On pause, destroy smoothing and leave native scroll usable. On hidden-tab/pagehide, stop the owned ticker; restore only if the user still permits movement. Stop only animation instances owned by this integration.

## Verify

Test keyboard PageDown, anchor navigation, browser Back, textarea overflow, open drawer scroll and at least one long form. Confirm the page remains usable when Lenis is unavailable. Never invoke purchases or submit customer forms merely to test smoothing.
