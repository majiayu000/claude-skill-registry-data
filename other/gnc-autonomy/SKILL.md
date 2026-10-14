---
name: gnc-autonomy
description: "Use when a task concerns guidance, navigation, and control for aerospace vehicles: guide the router to the gnc-autonomy pack: orbit-dynamics Hohmann and J2 drift, rendezvous-phasing phasing maneuvers, attitude-dynamics quaternion kinematics, navigation-frames ECEF/NED/WGS-84, inertial-navigation INS drift and Schuler, dilution-of-precision GDOP/PDOP, python-control-design PID margins, root-locus-design closed-loop poles, state-space-analysis controllability, pid-control-design Ziegler-Nichols, lqr-design Riccati gains, dymos-trajectory pseudospectral optimization, proportional-navigation the PN law, command-to-line-of-sight CLOS guidance, pursuit-guidance capture conditions, kalman-filter-design state estimation. Trigger: GNC, navigation, control, orbit dynamics, Hohmann, rendezvous, attitude dynamics, quaternion, ECEF/NED/WGS-84, INS, Schuler, dilution of precision, GDOP, PID, root locus, controllability, proportional navigation, command to line of sight, pursuit guidance, kalman filter, state estimation."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: arp4754a
    reference-only: true
  - id: ecss
    reference-only: true
gated: false
domain: gnc-autonomy
pack: gnc-autonomy
compatibility: "agentskills.io SKILL.md; router/entry point for the gnc-autonomy domain pack"
metadata:
  domain: gnc-autonomy
  tags: []
  version: 0.1.0
  author: Aero Agent Skills
---

# GNC and autonomy domain pack (router)

Route here when the task is guidance, navigation, and control:
orbital mechanics, control system design, trajectory optimization,
or guidance laws.

## Domain

GNC and autonomy: space orbit dynamics (propagation, maneuvers, J2),
rendezvous phasing, navigation frames (ECEF/NED/geodetic), inertial
navigation, classical control design (margins, tuning), state-space
control (root locus, LQR), pseudospectral trajectory optimization,
and guidance laws (proportional navigation, pursuit).

## Sub-skills in this pack

| Path | Skill | When to route to it |
|---|---|---|
| gnc-autonomy/space/orbit-dynamics | Orbit dynamics | Hohmann delta-v, vis-viva, J2 drift, transfer time |
| gnc-autonomy/space/rendezvous-phasing | Rendezvous phasing | phasing orbit, catch-up maneuver, drift time, rendezvous planning |
| gnc-autonomy/space/attitude-dynamics | Attitude dynamics | quaternion kinematics, Euler equations, inertia tensor, nutation, gravity-gradient torque, momentum wheel |
| gnc-autonomy/navigation/navigation-frames | Navigation frames | ECEF, NED, geodetic conversion, Earth rotation, WGS-84 |
| gnc-autonomy/navigation/inertial-navigation | Inertial navigation | INS mechanization, strapdown, gyro drift, accelerometer bias, Schuler period, alignment, INS/GPS integration |
| gnc-autonomy/navigation/dilution-of-precision | Dilution of precision | GDOP, PDOP, HDOP, VDOP, TDOP, satellite geometry, elevation mask, UERE, subset selection |
| gnc-autonomy/control/python-control-design | Control design | PID tuning, gain/phase margins, stability checks |
| gnc-autonomy/control/root-locus-design | Root locus design | closed-loop poles vs gain, gain for damping ratio, stability from root locus |
| gnc-autonomy/control/state-space-analysis | State space analysis | controllability, observability, state transition matrix, eigenvalues, canonical forms |
| gnc-autonomy/control/pid-control-design | PID control design | Ziegler-Nichols gains, ultimate gain/period, anti-windup, pole placement |
| gnc-autonomy/optimal-control/lqr-design | LQR design | Riccati gain, quadratic cost weights, closed-loop stability |
| gnc-autonomy/optimal-control/dymos-trajectory | Trajectory optimization | dymos phases, convergence, launch/ascent delta-v bands |
| gnc-autonomy/guidance/proportional-navigation | Proportional navigation | closing velocity, line of sight rate, navigation constant, commanded acceleration |
| gnc-autonomy/guidance/pursuit-guidance | Pursuit guidance | pure pursuit aim heading, wrapped guidance error, lead pursuit lead angle, capture condition, intercept time |
| gnc-autonomy/navigation/kalman-filter-design | Kalman filter design | kalman gain, innovation variance, error covariance, process noise, measurement noise, state estimation |
| gnc-autonomy/navigation/gnss-pseudorange-positioning | GNSS pseudorange positioning | pseudorange positioning, GNSS position fix, receiver clock bias, iterated least squares fix, ECEF position solution, satellite pseudorange residual, snapshot navigation solution |
| gnc-autonomy/navigation/gnss-doppler-velocity-positioning | GNSS doppler velocity positioning | gnss doppler velocity positioning, receiver velocity fix, doppler positioning, clock drift estimate, delta range rate |
| gnc-autonomy/guidance/command-to-line-of-sight | Command to line of sight | CLOS guidance, line of sight angle, steering command, LOS error |
| gnc-autonomy/guidance/impact-point-prediction | Impact point prediction | ballistic range equation, time of flight, impact coordinates, launch speed and angle sensitivity |
| gnc-autonomy/guidance/midcourse-guidance | Midcourse guidance | midcourse guidance, waypoint steering, trajectory shaping, velocity to be gained, zero effort miss, handover, turn rate limit |
| gnc-autonomy/guidance/dubins-path-planning | Dubins path planning | dubins path, minimum turn radius path, shortest path with heading constraints, CSC and CCC path families, arc tangent path, path length between poses |
| gnc-autonomy/control/lead-lag-compensation | Lead lag compensation | phase lead/lag compensator design, phase margin boost, gain crossover frequency, steady state error constant |
| gnc-autonomy/control/frequency-response-design | Frequency response design | bode magnitude and phase, gain/phase crossover frequencies, gain margin, phase margin, stability from the margins |
| gnc-autonomy/control/gain-scheduling | Gain scheduling | gain schedule breakpoints, scheduling variable, dynamic pressure and Mach scheduling, gain interpolation |
| gnc-autonomy/control/observer-design | Observer design | Luenberger observer, observability matrix, estimator gain, pole placement, separation principle |
| gnc-autonomy/estimation-filtering/alpha-beta-filter | Alpha-beta filter | alpha beta filter, constant velocity target, tracking update, smoothing factor, steady state gain, position and velocity tracking |
| gnc-autonomy/estimation-filtering/unscented-kalman-filter | Unscented Kalman filter | unscented Kalman filter, sigma points, scaled unscented transform, nonlinear state estimation, state prediction, measurement update, innovation covariance, NEES, bearing-range tracking |
| gnc-autonomy/estimation-filtering/process-noise-discretization | Process noise discretization | process noise discretization, van loan, continuous spectral density, discrete noise covariance |
| gnc-autonomy/estimation-filtering/imu-static-calibration | IMU static calibration | imu static calibration, six position test, rate table calibration, accelerometer bias scale |
| gnc-autonomy/estimation-filtering/extended-kalman-filter | Extended Kalman filter | extended kalman filter, EKF, Jacobian linearization, predict update, innovation covariance, kalman gain, nonlinear estimation |
| gnc-autonomy/optimal-control/model-predictive-control | Model Predictive Control | mpc, model predictive control, receding horizon, quadratic cost, prediction horizon, control horizon, input constraints, state constraints, terminal cost, double integrator, constrained control, closed loop simulation, kkt system, active set. |
| gnc-autonomy/estimation-filtering/particle-filter | Particle filter | particle filter, bootstrap filter, sequential Monte Carlo, SIR resampling, non-Gaussian estimation, effective sample size |
| gnc-autonomy/estimation-filtering/complementary-filter | Complementary filter | complementary filter, Mahony, gyro bias estimation, vector measurement fusion, SO(3) attitude observer |
| gnc-autonomy/space/orbit-determination | Orbit determination | orbit determination, Gibbs method, Herrick-Gibbs, three position vectors, rv to elements, initial orbit determination |
| gnc-autonomy/control/control-allocation | Control allocation | control allocation, effector allocation, control effectiveness matrix, pseudoinverse allocation, weighted least squares, daisy chain, redistributed pseudoinverse, actuator limits, saturation, moment command distribution, redundant effectors |
| gnc-autonomy/navigation/gnss-raim-fde | GNSS RAIM FDE | RAIM, receiver autonomous integrity monitoring, fault detection and exclusion, horizontal protection level, chi-square threshold, normalized residual, GNSS integrity |
| gnc-autonomy/estimation-filtering/rts-smoother | RTS smoother | RTS smoother, Rauch-Tung-Striebel, fixed-interval smoothing, backward pass, smoothed state, offline trajectory reconstruction |
| gnc-autonomy/guidance/coverage-path-planning | Coverage path planning | coverage path planning, boustrophedon, lawnmower pattern, aerial survey flight lines, swath width, side overlap, track spacing, area search |
| gnc-autonomy/control/adaptive-control | Adaptive control | adaptive control, MRAC, model reference adaptive, adaptation law, tracking error, unknown plant, gain adaptation |
| gnc-autonomy/guidance/augmented-proportional-navigation | Augmented proportional navigation | augmented proportional navigation, target lateral acceleration, maneuvering target intercept, APN command |
| gnc-autonomy/guidance/collision-course-guidance | Collision-course guidance | collision course, lead angle, constant bearing, collision triangle, predicted intercept point |

| gnc-autonomy/estimation-filtering/interacting-multiple-model-filter | Interacting multiple model filter | IMM filter, mode probability, Markov mode switching, maneuvering target tracking, CV CA filter bank, model likelihood update, mixed state estimate |
| gnc-autonomy/control/digital-control-design | Digital control design | z transform, Tustin bilinear emulation, frequency prewarping, zero order hold, discrete PID, sample rate selection, unit circle stability, sampled data control |
| gnc-autonomy/optimal-control/bang-bang-control | Bang-bang control | bang bang control, time optimal control, switching curve, minimum time maneuver, double integrator, rest to rest slew |
| gnc-autonomy/navigation/ins-gnss-integrated-filter | INS GNSS integrated filter | ins gnss integrated filter, error state filter, loosely coupled integration, GNSS position update, INS drift correction |
| gnc-autonomy/navigation/tightly-coupled-ins-gnss | Tightly coupled INS GNSS | tightly coupled ins gnss, raw pseudorange update, ins gnss tight coupling, clock state filter |
| gnc-autonomy/navigation/gnss-carrier-smoothing | GNSS carrier smoothing | code-carrier Hatch smoothing time constant, carrier delta range, code-carrier ionospheric divergence, smoothed range noise reduction |
| gnc-autonomy/optimal-control/lqg-design | LQG design | linear-quadratic-Gaussian output-feedback compensator, regulator and filter Riccati gains, separation principle |
| gnc-autonomy/navigation/bearing-only-localization | Bearing only localization | passive angle-of-arrival bearing lines, Stansfield weighted least squares emitter fix, bearing-line error ellipse |

| gnc-autonomy/optimal-control/ilqr-ddp | Iterative LQR DDP | ilqr ddp, iterative LQR, differential dynamic programming, backward Riccati pass, nonlinear trajectory optimization, finite horizon optimal control |
| gnc-autonomy/navigation/terrain-referenced-navigation | Terrain referenced navigation | terrain referenced navigation, TERCOM correlation, digital elevation model matching, SITAN terrain slope update, radar altimeter profile matching |
| gnc-autonomy/navigation/gnss-rtk-positioning | GNSS RTK positioning | GNSS RTK positioning, carrier phase differential, double difference baseline, integer ambiguity resolution, real time kinematic |

| gnc-autonomy/optimal-control/loop-transfer-recovery | Loop Transfer Recovery | loop-transfer-recovery, full-state-loop-recovery, lqg-loop-shaping, recovery-gain-tuning, target-feedback-loop |
| gnc-autonomy/control/l1-adaptive-control | L1 Adaptive Control | l1-adaptive-control, state-predictor, low-pass-filtered-adaptation, projection-based-adaptation-law, guaranteed-transient-response |
| gnc-autonomy/estimation-filtering/cramer-rao-lower-bound | Cramer Rao Lower Bound | cramer-rao-lower-bound, fisher-information-matrix, estimator-efficiency, best-achievable-variance, bound-achieving-estimator |
| gnc-autonomy/navigation/ionospheric-delay-correction | Ionospheric Delay Correction | ionospheric-delay-correction, klobuchar-broadcast-model, slant-delay-correction, pierce-point-geometry, broadcast-alpha-beta-coefficients |
| gnc-autonomy/guidance/impact-time-control-guidance | Impact Time Control Guidance | impact-time-control-guidance, salvo-attack-guidance, commanded-impact-time, time-to-go-error-feedback, simultaneous-impact-guidance |
| gnc-autonomy/control/deadbeat-control | Deadbeat Control | deadbeat-control, finite-settling-time, pole-placement-at-origin, minimum-settling-time, z-domain-deadbeat |
| gnc-autonomy/navigation/tropospheric-delay-correction | Tropospheric Delay Correction | tropospheric-delay-correction, saastamoinen-model, zenith-wet-delay, dry-delay-mapping, elevation-angle-mapping |
| gnc-autonomy/guidance/impact-angle-control-guidance | Impact Angle Control Guidance | impact-angle-control-guidance, impact-angle-constraint, terminal-flight-path-angle, biased-proportional-navigation, trajectory-shaping-guidance |
| gnc-autonomy/control/smith-predictor | Smith Predictor | smith-predictor, dead-time-compensation, time-delay-compensator, predictor-controller, process-dead-time |
| gnc-autonomy/control/h-infinity-control | H-infinity Control | h-infinity-control, mixed-sensitivity-design, s-ks-weighting, h-infinity-norm, loop-shaping-robustness |
| gnc-autonomy/control/h-infinity-synthesis | H-infinity Synthesis | h-infinity-synthesis, dgkf-two-riccati, gamma-iteration, spectral-radius-coupling, central-controller, generalized-plant-weighting |
| gnc-autonomy/control/sliding-mode-control | Sliding Mode Control | sliding-mode-control, sliding-surface, equivalent-control, reaching-law, chattering-suppression, variable-structure-control |
| gnc-autonomy/control/feedback-linearization | Feedback Linearization | feedback-linearization, input-output-linearization, relative-degree, lie-derivative, zero-dynamics, nonlinearity-cancelling-control |
| gnc-autonomy/control/backstepping-control | Backstepping Control | backstepping-control, integrator-backstepping, strict-feedback, virtual-control, control-lyapunov-function, recursive-control-design, backstepping-control-law, error-variable-recursion |
| gnc-autonomy/control/active-disturbance-rejection-control | Active Disturbance Rejection Control | active-disturbance-rejection-control, linear-extended-state-observer, adrc, bandwidth-parameterization, total-disturbance-estimate, disturbance-rejection-term, observer-gain-parameterization |
| gnc-autonomy/control/adaptive-backstepping | Adaptive Backstepping | adaptive-backstepping, tuning-function, parameter-estimate, strict-feedback, adaptive-virtual-control, augmented-lyapunov-function, parameter-error-convergence, no-over-parameterization |
## Routing guidance

- Orbit and maneuver questions route to the orbit-dynamics sub-skill.
- Phasing and rendezvous planning questions route to the
  rendezvous-phasing sub-skill.
- Attitude dynamics, quaternion kinematics, and momentum questions
  route to the space attitude-dyn- Mpc questions route to the optimal-control model-predictive-control sub-skill.
amics sub-skill.
- Coordinate-frame and navigation-solution questions (ECEF/NED/geodetic,
  WGS-84) route to the navigation navigation-frames sub-skill.
- Inertial navigation, drift, and Schuler questions route to the
  navigation inertial-navigation sub-skill.
- DOP, satellite geometry, and subset-selection questions route to the
  navigation dilution-of-precision sub-skill.
- Controller design and margin questions route to the
  python-control-design sub-skill.
- Root-locus questions (pole trajectories, gain for target damping)
  route to the control root-locus-design sub-skill.
- State-space controllability, observability, transition-matrix, and
  canonical-form questions route to the control state-space-analysis
  sub-skill.
- PID gain tuning, Ziegler-Nichols, and anti-windup questions route to
  the control pid-control-design sub-skill.
- LQR and Riccati-gain questions route to the optimal-control
  lqr-design sub-skill.
- Optimal control and trajectory questions route to the
  dymos-trajectory sub-skill.
- Proportional navigation and intercept guidance questions route to
  the guidance proportional-navigation sub-skill.
- Pure pursuit, lead pursuit, and capture-condition questions route
  to the guidance pursuit-guidance sub-skill.
- Ballistic impact point, range equation, time of flight, and launch
  speed and angle sensitivity questions route to the guidance
  impact-point-prediction sub-skill.
- Midcourse waypoint steering, trajectory shaping, velocity-to-be-gained,
  zero-effort-miss, and terminal handover questions route to the guidance
  midcourse-guidance sub-skill.
- Certification and item-level assurance questions route to the
  avionics or systems-engineering-safety packs.

- Kalman filtering, state estimation, and sensor fusion questions route to the navigation kalman-filter-design sub-skill.
- Command-to-line-of-sight and LOS error steering questions route to the guidance command-to-line-of-sight sub-skill.
- Phase lead/lag compensator, phase margin boost, crossover placement, and steady state error constant questions route to the control lead-lag-compensation sub-skill.
- Bode frequency response, gain crossover, phase crossover, gain margin, and phase margin questions route to the control frequency-response-design sub-skill.
- Gain schedule breakpoint tables, scheduling variables (dynamic pressure, Mach), and gain interpolation questions route to the control gain-scheduling sub-skill.
- Full-order state observer design, observability checks, estimator gain pole placement, and separation principle questions route to the control observer-design sub-skill.
- Alpha-beta tracking, constant velocity target, smoothing factor, steady state gain, and position and velocity tracking questions route to the estimation-filtering alpha-beta-filter sub-skill.
- Sigma-point nonlinear state estimation, scaled unscented transform, UKF predict and update, and innovation covariance checks route to the estimation-filtering unscented-kalman-filter sub-skill.
- Estimation-bound questions (Fisher information, Cramer-Rao lower bound for scalar and vector estimators, DC level in Gaussian noise, estimator efficiency against the bound) route to the estimation-filtering cramer-rao-lower-bound sub-skill.
- Extended Kalman filter design for nonlinear systems with Jacobian linearization, predict and update recursion, innovation covariance, and Kalman gain computation routes to the estimation-filtering extended-kalman-filter sub-skill.
- Control allocation across redundant effectors, pseudoinverse and weighted least squares, daisy chain, and actuator saturation redistribution questions route to the control control-allocation sub-skill.
- RAIM integrity questions (fault detection and exclusion, horizontal protection level, chi-square threshold, normalized residual) route to the navigation gnss-raim-fde sub-skill.
- Rauch-Tung-Striebel fixed-interval smoothing and backward-pass post-processing questions route to the estimation-filtering rts-smoother sub-skill.
- Coverage path planning, boustrophedon, and lawnmower aerial survey pattern questions route to the guidance coverage-path-planning sub-skill.
- Model-reference adaptive control questions (MRAC, adaptation law, tracking error convergence, unknown plant coefficient) route to the control adaptive-control sub-skill.
- L1 adaptive control questions (state predictor, projection-based adaptation law, low-pass-filtered adaptive signal, guaranteed transient response of the first-order uncertain plant) route to the control l1-adaptive-control sub-skill; first-order MRAC stays with adaptive-control.

- Interacting multiple model filter questions (IMM filter bank, mode probability, Markov mode switching, maneuvering target tracking, CV CA modes) route to the estimation-filtering interacting-multiple-model-filter sub-skill.
- Sampled-data digital control questions (z transform, Tustin bilinear emulation, frequency prewarping, zero order hold, discrete PID, unit circle stability) route to the control digital-control-design sub-skill.

- Time-optimal bang-bang control questions (switching curve, minimum-time rest-to-rest slew, double integrator) route to the optimal-control bang-bang-control sub-skill.
- code-carrier Hatch smoothing time constant, carrier delta range, code-carrier ionospheric divergence, smoothed range noise reduction questions route to the navigation gnss-carrier-smoothing sub-skill.
- linear-quadratic-Gaussian output-feedback compensator, regulator and filter Riccati gains, separation principle questions route to the optimal-control lqg-design sub-skill.
- Loop-transfer-recovery questions (LQG output loop recovery by filter noise weight inflation, full-state-loop matching, recovery-gain tuning, target feedback loop) route to the optimal-control loop-transfer-recovery sub-skill.
- Ionospheric delay correction questions (Klobuchar broadcast model slant delay, alpha and beta coefficient polynomials, pierce-point geometry, L1 pseudorange delay removal) route to the navigation ionospheric-delay-correction sub-skill; carrier-smoothed code divergence stays with gnss-carrier-smoothing.
- Impact-time-control questions (salvo and simultaneous-impact guidance, commanded impact time, time-to-go error feedback, simultaneous-impact-guidance law) route to the guidance impact-time-control-guidance sub-skill.
- Tropospheric delay correction questions (Saastamoinen zenith dry and wet delay, elevation-angle mapping to slant delay, pressure temperature humidity inputs) route to the navigation tropospheric-delay-correction sub-skill; ionospheric Klobuchar delay stays with ionospheric-delay-correction.
- Impact-angle-constrained guidance questions (terminal flight-path-angle control, biased proportional navigation, trajectory-shaping guidance laws) route to the guidance impact-angle-control-guidance sub-skill; impact-time control stays with impact-time-control-guidance.
- Smith predictor questions (dead-time compensation, predictor structure for time-delayed plants, delay-free characteristic equation) route to the control smith-predictor sub-skill; PID tuning and digital emulation stay with pid-control-design and digital-control-design.
- H-infinity control questions (mixed-sensitivity S/KS loop shaping, H-infinity norm computation, robustness weights) route to the control h-infinity-control sub-skill; LQR and LQG synthesis stay with lqr-design and lqg-design.
- passive angle-of-arrival bearing lines, Stansfield weighted least squares emitter fix, bearing-line error ellipse questions route to the navigation bearing-only-localization sub-skill.
- H-infinity synthesis questions (DGKF two-Riccati state-space synthesis, gamma iteration, spectral-radius coupling condition, central controller) route to the control h-infinity-synthesis sub-skill; mixed-sensitivity S/KS norm analysis of a given pair stays with h-infinity-control.
- Sliding-mode control questions (sliding surface design, equivalent control, reaching law, chattering suppression) route to the control sliding-mode-control sub-skill; model-reference and L1 adaptation stay with adaptive-control and l1-adaptive-control.
- Feedback-linearization questions (input-output linearization, relative degree, zero-dynamics stability, nonlinearity-cancelling control law) route to the control feedback-linearization sub-skill; variable-structure control stays with sliding-mode-control.

## Install

To install only this pack, copy or symlink each leaf folder above into
your host's skills directory (see README Install for per-host commands).
- Particle filter and non-Gaussian nonlinear estimation questions route to the estimation-filtering particle-filter sub-skill.
- Mahony complementary-filter attitude estimation and gyro-bias questions route to the estimation-filtering complementary-filter sub-skill.
- Dubins minimum-turn path generation between heading-constrained poses and CSC/CCC path family questions route to the guidance dubins-path-planning sub-skill.
- Single-epoch GNSS pseudorange position and clock-bias fixes route to the navigation gnss-pseudorange-positioning sub-skill.
- Collision-course intercept questions (lead angle, constant bearing, collision triangle, predicted intercept point) route to the guidance collision-course-guidance sub-skill.
- Augmented proportional navigation questions (target lateral acceleration term, maneuvering target intercept, APN command) route to the guidance augmented-proportional-navigation sub-skill.
- Gibbs and Herrick-Gibbs initial orbit determination from three position vectors routes to the space orbit-determination sub-skill.

- Loosely coupled INS/GNSS integration questions (error-state filter propagation with the psi-angle model, GNSS position updates, INS drift correction) route to the navigation ins-gnss-integrated-filter sub-skill.
- Tightly coupled INS/GNSS questions (raw-pseudorange measurement updates, clock bias and drift states, INS error-state filter on the raw observables) route to the navigation tightly-coupled-ins-gnss sub-skill.
- GNSS receiver-velocity questions (carrier delta-range-rate doppler observables, iterated least-squares velocity and clock-drift fix) route to the navigation gnss-doppler-velocity-positioning sub-skill.
- Process-noise discretization questions (van Loan method, continuous spectral density to discrete covariance, filter Q design) route to the estimation-filtering process-noise-discretization sub-skill.
- Nonlinear finite-horizon trajectory optimization questions (iterative LQR, differential dynamic programming, backward Riccati pass) route to optimal-control ilqr-ddp; terrain/map-aided INS questions (TERCOM correlation, DEM matching, SITAN terrain-slope update) route to navigation terrain-referenced-navigation; carrier-phase differential positioning (double differences, integer ambiguity resolution) routes to navigation gnss-rtk-positioning.
- IMU static calibration questions (six-position accelerometer test, rate-table gyro calibration, bias and scale factor estimation) route to the estimation-filtering imu-static-calibration sub-skill.
- Backstepping questions (strict-feedback recursive design, error-variable recursion, virtual control, analytic virtual-control derivative, control-Lyapunov decay audit) route to the control backstepping-control sub-skill; model-reference and L1 adaptation stay with adaptive-control and l1-adaptive-control; switching laws stay with sliding-mode-control.
- Active-disturbance-rejection questions (linear-extended-state-observer bandwidth parameterization, total-disturbance estimation, disturbance-rejection term) route to the control active-disturbance-rejection-control sub-skill; classical PID tuning stays with pid-control-design; model-reference and L1 adaptation stay with adaptive-control and l1-adaptive-control.
- Adaptive-backstepping questions (tuning-function design, parameter estimate updated by the second tuning function carried through the z1 z2 error recursion, theta-hat virtual control, augmented Lyapunov function with the parameter-error term, parameter-error convergence) route to the control adaptive-backstepping sub-skill; exact-model strict-feedback recursion stays with backstepping-control; model-reference and L1 adaptation stay with adaptive-control and l1-adaptive-control.
