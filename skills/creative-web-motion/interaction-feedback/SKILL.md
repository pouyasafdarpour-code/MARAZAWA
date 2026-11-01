---
name: marazawa-motion-feedback
description: Add restrained magnetic and depth feedback to navigation and service cards with a consistent accessible motion toggle. Use for pointer feedback and motion preference behavior, not transactional controls.
---

# Respond to intent

Use movement to show that a service or navigation card responds to the person. Keep click targets stable and predictable.

## Magnetic navigation

Apply only on fine pointers. Normalize pointer position within the target rectangle and move about -2.5px to +2.5px on either axis. Ease toward the offset over 0.35 seconds; return to zero over 0.45 seconds on pointerleave. Preserve keyboard focus styling. Do not replace the system cursor.

Store offsets in dedicated CSS variables and apply with `translate`, so an existing scale/breathing `transform` is not discarded. Avoid competing transform authors. Add subtle shadow depth through an isolated pseudo-element.

Exclude payment, submission, consent, deletion and password controls. No click handler should be delayed, redirected, auto-triggered or duplicated by visual feedback. On a touch device keep controls still.

## One motion preference

Provide a labeled control in the navigation drawer with at least a 44px touch target and meaningful `aria-pressed`. Persist only on/off preference in local storage, with storage failure handled gracefully. Honor the operating system's reduced-motion preference even if the page setting is on.

Keep existing per-page pause controls compatible: either control must stop the new engine. Turning movement off must leave content in its readable final state, not freeze an entrance at opacity zero. Reflect state in the visible label and keep menu focus behavior intact.

## Verify

Exercise on/off/on, reload, private browsing storage failure, keyboard-only menu navigation, coarse pointer and an existing animated card. Remove transient offsets on stop. Never treat this presentation preference as permission to change account or privacy settings.
