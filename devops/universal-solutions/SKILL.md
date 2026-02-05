---
name: universal-solutions
description: Use when facing any animation problem as a comprehensive diagnostic framework
---

# Universal Animation Solutions

A complete diagnostic framework using all 12 Disney principles.

## The 12 Principles Checklist

Run through each principle to diagnose any animation problem:

### 1. Squash and Stretch
**Check**: Is there appropriate flexibility?
**Problem sign**: Rigid, lifeless motion
**Fix**: Add subtle scale changes on impact/acceleration

### 2. Anticipation
**Check**: Is there buildup before action?
**Problem sign**: Actions feel sudden or surprising
**Fix**: Add small reverse movement or wind-up

### 3. Staging
**Check**: Is the important thing clear?
**Problem sign**: Users miss key information
**Fix**: Isolate animated element, reduce competing motion

### 4. Straight Ahead vs Pose-to-Pose
**Check**: Is the approach right for the effect?
**Problem sign**: Uncontrolled or too rigid motion
**Fix**: Use keyframes for UI; frame-by-frame for organic

### 5. Follow Through
**Check**: Do things settle naturally?
**Problem sign**: Abrupt, mechanical endings
**Fix**: Add overshoot and settle, or soft deceleration

### 6. Slow In and Slow Out
**Check**: Is there proper easing?
**Problem sign**: Robotic, linear motion
**Fix**: Apply ease-out for entrances, ease-in for exits

### 7. Arcs
**Check**: Is the motion path natural?
**Problem sign**: Unnatural straight-line movement
**Fix**: Add curved paths for organic motion

### 8. Secondary Action
**Check**: Do supporting elements enhance?
**Problem sign**: Flat, one-dimensional animation
**Fix**: Add subtle complementary movements

### 9. Timing
**Check**: Is the speed appropriate?
**Problem sign**: Too fast or too slow
**Fix**: Micro: 100-200ms, Transitions: 200-400ms

### 10. Exaggeration
**Check**: Is the drama level right?
**Problem sign**: Too subtle or too dramatic
**Fix**: Match exaggeration to context importance

### 11. Solid Drawing
**Check**: Is rendering correct?
**Problem sign**: Visual glitches, distortion
**Fix**: Use transform/opacity only, check GPU layers

### 12. Appeal
**Check**: Does it feel right?
**Problem sign**: Hard to articulate wrongness
**Fix**: Align motion with brand/emotional intent

## Quick Diagnostic

1. **Describe the problem** in one sentence
2. **Identify which principle** relates most directly
3. **Check adjacent principles** (problems cluster)
4. **Apply targeted fix** from that principle

## Master Troubleshooting Checklist

- [ ] Does animation serve a purpose?
- [ ] Is timing appropriate (usually 150-300ms)?
- [ ] Is easing applied (not linear)?
- [ ] Does it respect `prefers-reduced-motion`?
- [ ] Is only transform/opacity being animated?
- [ ] Is motion guiding attention correctly?
- [ ] Does it match brand/emotional context?
- [ ] Can users complete tasks without it?
- [ ] Test on slowest target device
- [ ] Get user feedback with emotional vocabulary

## When to Remove Animation

Remove animation entirely if:
- It doesn't serve clear purpose
- Users complain or skip it
- It delays task completion
- It causes accessibility issues
- Performance is unacceptable
- You can't articulate why it exists
