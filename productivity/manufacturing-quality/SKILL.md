---
name: manufacturing-quality
description: "Use when a task concerns aerospace manufacturing and quality management: guide the router to the manufacturing-quality pack. AS9100 quality, nonconformance-control, supplier-control, counterfeit-prevention, calibration-control, corrective-action, document-control, and statistical-process-control cover QMS scoping, disposition, supplier risk, counterfeit scoring, calibration, CAPA closure, controlled documents, and SPC; first-article-inspection, delta-fai, and fai-revalidation cover AS9102 FAI; ndt-method-selection, ultrasonic-inspection, eddy-current-inspection, and radiographic-inspection cover NDT. Trigger: manufacturing quality, AS9100, AS9102, first article inspection, QMS, corrective action, CAPA, 8D, five whys, document control, FAI, revalidation, counterfeit prevention, nonconformance, disposition, MRB, supplier control, calibration, test accuracy ratio, statistical process control, SPC, Cpk, NDT, radiography, ultrasonic, eddy current, depth of penetration."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: as9100
    reference-only: true
  - id: as9102
    reference-only: true
gated: false
domain: manufacturing-quality
pack: manufacturing-quality
compatibility: "agentskills.io SKILL.md; router/entry point for the manufacturing-quality domain pack"
metadata:
  domain: manufacturing-quality
  tags: []
  version: 0.1.0
  author: Aero Agent Skills
---

# Manufacturing and quality domain pack (router)

Route here when the task is aerospace production and quality
management.

## Domain

Manufacturing and quality: aerospace quality management systems
(AS9100, ISO 9001:2015 plus aerospace clauses), audit evidence,
corrective action, nonconformance control, supplier control,
counterfeit prevention, calibration control, first article inspection
(AS9102 Forms 1-3, delta FAI), and non-destructive testing (method
selection and ultrasonic inspection).

## Sub-skills in this pack

| Path | Skill | When to route to it |
|---|---|---|
| manufacturing-quality/as9100/quality | AS9100 quality | QMS clause scoping, audit evidence, corrective-action closure |
| manufacturing-quality/as9100/nonconformance-control | Nonconformance control | disposition of nonconforming product, rework/repair/scrap/use-as-is, MRB routing |
| manufacturing-quality/as9100/supplier-control | Supplier control | supplier risk classification, required controls, delegated verification, external providers |
| manufacturing-quality/as9100/counterfeit-prevention | Counterfeit prevention | counterfeit parts risk scoring, prevention planning, procurement controls |
| manufacturing-quality/as9100/calibration-control | Calibration control | calibration system, traceability, intervals, TAR 4:1, out-of-tolerance handling, recall |
| manufacturing-quality/as9100/corrective-action | Corrective action | CAPA record, 8D workflow, five whys, root cause, containment, effectiveness verification |
| manufacturing-quality/as9100/document-control | Document control | master list, controlled documents, current revision, obsolete revision disposition |
| manufacturing-quality/as9102/first-article-inspection | First article inspection | FAI Forms 1-3, characteristic accountability, delta FAI |
| manufacturing-quality/as9102/delta-fai | AS9102 delta FAI | change classification, full vs delta FAI, forms scope |
| manufacturing-quality/as9102/fai-revalidation | FAI revalidation | revalidation due date, interval, change-driven revalidation, re-verification scope |
| manufacturing-quality/as9102/ballooning | Ballooning | balloon numbers, characteristic numbering, D-list, accountability matrix, verification method code |
| manufacturing-quality/ndt/ndt-method-selection | NDT method selection | defect class, ferromagnetic/conductive material, radiography, ultrasonic, eddy current, penetrant, magnetic particle |
| manufacturing-quality/ndt/ultrasonic-inspection | Ultrasonic inspection | pulse-echo, time of flight to depth, wavelength, near field, discontinuity sizing |
| manufacturing-quality/ndt/radiographic-inspection | Radiographic inspection | radiography, X-ray, gamma ray, geometric unsharpness, IQI, penetrameter, film density, porosity |
| manufacturing-quality/as9100/statistical-process-control | Statistical process control | X-bar chart, R chart, control limits, Cp/Cpk, process capability, Western Electric rules |
| manufacturing-quality/as9100/risk-management | Risk management | FMEA risk priority number, RPN band, mitigation planning, operational risk, risk matrix, residual risk, risk register |
| manufacturing-quality/ndt/eddy-current-inspection | Eddy current inspection | eddy current, depth of penetration, impedance plane, frequency selection, conductivity, subsurface flaw |
| manufacturing-quality/ndt/liquid-penetrant-inspection | Liquid penetrant inspection | penetrant testing, capillary rise, washburn penetration depth, dwell time, developer time, bleed-out, indication sizing |
| manufacturing-quality/ndt/magnetic-particle-inspection | Magnetic particle inspection | magnetization current, circular and longitudinal magnetization, field strength band, coverage overlap, particle sensitivity, indication acceptance |
| manufacturing-quality/ndt/visual-inspection | Visual inspection | aperture ratio, magnification, lighting requirements, surface indication acceptance, borescope, field of view, working distance |
| manufacturing-quality/special-processes/special-process-qualification | Special process qualification | special process, process qualification record, requalification trigger, parameter change, equipment change, NADCAP, process variables |
| manufacturing-quality/ndt/thermography | Infrared thermography | flash thermography, thermal contrast, disbond, delamination, lock-in, inspection parameters |
| manufacturing-quality/as9100/measurement-systems-analysis | Measurement systems analysis | gage R and R, repeatability, reproducibility, percent GRR, distinct categories |
| manufacturing-quality/additive/additive-manufacturing-qualification | Additive manufacturing qualification | volumetric energy density, laser power, scan speed, hatch spacing, layer height, witness coupon, material property verification, AM first article |
| manufacturing-quality/additive/lpbf-parameter-development | LPBF parameter development | LPBF, laser powder bed fusion, volumetric energy density, scan speed, hatch spacing, layer thickness, melt pool, keyhole mode, conduction mode, process window |
| manufacturing-quality/ndt/acoustic-emission-inspection | Acoustic emission inspection | acoustic emission, AE inspection, source location, Kaiser effect, Felicity ratio, hit, event, sensor |
| manufacturing-quality/composites/layup-cure | Layup Cure | composite layup, ply book, laminate, symmetric, balanced, cure cycle, autoclave, out-of-autoclave, OOA, degree of cure, epoxy, 350F, glass transition, Tg, C-scan, porosity. |
| manufacturing-quality/as9103/key-characteristic-management | Key characteristic management | key characteristic, AS9103, variation management, KC identification, Cpk target, revalidation trigger |
| manufacturing-quality/ndt/computed-tomography | Computed tomography (CT) | computed tomography, CT scan, voxel size, cone beam, CT number, porosity measurement, volumetric inspection, magnification, projection count, additive part porosity |
| manufacturing-quality/ndt/shearography-inspection | Laser shearography inspection | laser shearography, shearography inspection, phase map, shear distance, strain gradient, vacuum load step, disbond detection, fringe anomaly, minimum detectable strain |
| manufacturing-quality/ndt/leak-testing | Leak testing | leak testing, pressure decay, vacuum decay, helium mass spectrometer, sniffer test, bubble test, leak rate, helium to air conversion, gauge resolution, maximum allowable leak |
| manufacturing-quality/assembly/fastener-installation-quality | Fastener installation quality | fastener installation quality, grip length selection, thread protrusion, clamp load from torque, countersink flushness, collar engagement |
| manufacturing-quality/as9100/fod-control | FOD control | FOD prevention, foreign object debris, FOD zone classification, tool control count, FOD sweep interval, FOD audit |
| manufacturing-quality/special-processes/welding-qualification | Welding qualification | weld procedure qualification, WPS PQR heat input, kJ per mm, preheat and interpass verification, weld coupon test matrix |
| manufacturing-quality/assembly/ewis-installation-quality | EWIS installation quality | EWIS installation, wiring harness, bundle fill ratio, voltage drop check, bend radius check, separation clearance |
| manufacturing-quality/as9100/internal-quality-audit | Internal quality audit | internal audit program, audit schedule, auditor independence, audit sample size, finding classification, closure verification |

| manufacturing-quality/as9100/management-review | Management review | management review, top management, review interval, review inputs, action item tracking, review verdict, QMS review |
| manufacturing-quality/ndt/ndt-personnel-qualification | NDT personnel qualification | NDT personnel qualification, NAS 410, certification currency, recertification due, vision examination, level progression |
| manufacturing-quality/as9100/order-requirements-review | Order requirements review | purchase order review, special requirement classification, contract review, order acceptance verdict, feasibility gates |
| manufacturing-quality/as9100/cusum-ewma-monitoring | CUSUM EWMA monitoring | cusum ewma monitoring, cusum control chart, ewma control chart, cumulative sum monitoring, small shift detection, sequential process monitoring |
| manufacturing-quality/assembly/solid-rivet-installation-quality | Solid rivet installation quality | solid rivet installation quality, solid rivet installation, driven head formation, shop head dimension check, rivet squeeze force, hole fill verification |

| manufacturing-quality/as9100/attribute-control-charts | Attribute control charts | attribute control charts, p-chart, np-chart, c-chart, u-chart, fraction nonconforming, defects per unit |
| manufacturing-quality/as9100/attribute-agreement-analysis | Attribute agreement analysis | attribute agreement analysis, Cohen kappa, Fleiss kappa, inspector agreement, chance-corrected agreement |
| manufacturing-quality/as9100/individuals-and-moving-range-chart | Individuals and moving range chart | individuals and moving range chart, I-MR chart, single measurement per lot, moving range limits |
| manufacturing-quality/as9100/gage-linearity-bias-study | Gage linearity and bias study | gage linearity and bias study, measurement bias, gage linearity regression, bias significance, linearity percent band |
| manufacturing-quality/as9100/acceptance-sampling | Acceptance sampling | attribute acceptance sampling, lot size code letter, AQL accept and reject numbers, operating characteristic curve, lot accept reject decision |
| manufacturing-quality/as9100/gage-rr-anova | ANOVA gage R&R | ANOVA gage R and R, two-way variance component decomposition, operator part interaction, percent GRR verdict, distinct categories count |
| manufacturing-quality/as9100/variables-acceptance-sampling | Variables acceptance sampling | variables acceptance sampling, k method, acceptability constant, form Q statistic, estimated percent nonconforming, code letter lot size, AQL variables plan |


## Routing guidance

- Quality management questions (audits, clause scope, evidence,
  corrective action) route to the AS9100 sub-skill.
- Nonconforming product questions (disposition, rework, repair,
  scrap, use-as-is, MRB) route to the nonconformance-control
  sub-skill.
- Ext- Composite layup questions route to the composites layup-cure sub-skill.
ernal provider and supplier questions (classification, controls,
  delegated verification) route to the supplier-control sub-skill.
- Counterfeit risk and prevention questions route to the
  counterfeit-prevention sub-skill.
- Calibration questions (traceability, intervals, test accuracy
  ratio, out-of-tolerance) route to the calibration-control
  sub-skill.
- CAPA and root cause questions (8D, five whys, containment,
  effectiveness) route to the corrective-action sub-skill.
- Document questions (master list, current revision, obsolete
  disposition) route to the document-control sub-skill.
- First article and production-approval questions (forms,
  accountability, delta FAI) route to the AS9102 sub-skill.
- Change-classification and delta-FAI-scope questions (full vs delta
  after a production change) route to the as9102 delta-fai sub-skill.
- Revalidation and FAI currency questions (due date, interval,
  change-driven) route to the as9102 fai-revalidation sub-skill.
- Non-destructive testing method questions (defect class, material,
  method sensitivity) route to the ndt ndt-method-selection
  sub-skill; pulse-echo ultrasonic execution questions route to the
  ultrasonic-inspection sub-skill.
- Ballooning and characteristic-numbering questions (balloon numbers,
  D-list, accountability matrix, verification method codes) route to
  the as9102 ballooning sub-skill.
- Radiographic inspection questions (unsharpness, IQI sensitivity,
  film density, discontinuity interpretation) route to the ndt
  radiographic-inspection sub-skill.
- Design and certification questions route to the avionics or
  systems-engineering-safety packs.

- SPC, control chart, and process capability questions route to the AS9100 statistical-process-control sub-skill.
- Operational risk assessment and mitigation planning questions (FMEA risk priority number, RPN band, risk matrix, residual risk, risk register) route to the AS9100 risk-management sub-skill.
- Eddy current, depth of penetration, and frequency-selection questions route to the ndt eddy-current-inspection sub-skill.
- Liquid penetrant inspection questions (capillary action, washburn penetration, dwell time, developer time, bleed-out, indication sizing) route to the ndt liquid-penetrant-inspection sub-skill.
- Magnetic particle inspection questions (magnetization current, circular and longitudinal magnetization, field strength band, coverage overlap, particle sensitivity, indication acceptance, residual field) route to the ndt magnetic-particle-inspection sub-skill.
- Visual inspection questions (aperture ratio, magnification, lighting requirements, surface indication acceptance, borescope field of view, working distance) route to the ndt visual-inspection sub-skill.
- Special process qualification, process qualification records, requalification triggers (parameter, equipment, personnel, interval change), and NADCAP evidence questions route to the special-processes special-process-qualification sub-skill.
- Flash thermography, thermal contrast, disbond and delamination detection, and lock-in questions route to the ndt thermography sub-skill.
- Gage R and R, repeatability, reproducibility, percent GRR, and distinct category questions route to the AS9100 measurement-systems-analysis sub-skill.
- Additive manufacturing energy density, parameter set, witness coupons, material property verification, and AM first article questions route to the additive additive-manufacturing-qualification sub-skill.
- Laser powder bed fusion parameter development, volumetric energy density, process window classification, and qualification test matrix planning route to the additive lpbf-parameter-development sub-skill.
- Acoustic emission NDT, AE sources, sensors and frequency bands, hit and event definitions, Kaiser effect and Felicity ratio, and linear and planar source location questions route to the ndt acoustic-emission-inspection sub-skill.
- Computed tomography scan planning, voxel size and magnification, projection count, CT number, and volumetric porosity measurement questions route to the ndt computed-tomography sub-skill.
- Fastener installation quality questions (fastener installation quality, grip length selection, thread protrusion, clamp load from torque, countersink flushness, collar engagement) route to the fastener-installation-quality sub-skill.
- FOD control questions (fod prevention, foreign object debris, fod zone classification, tool control count, fod sweep interval, fod audit) route to the fod-control sub-skill.
- Welding qualification questions (weld procedure qualification, wps pqr heat input, kj per mm, preheat and interpass verification, weld coupon test matrix) route to the welding-qualification sub-skill.
- EWIS wiring installation questions (wiring harness, bundle fill ratio, voltage drop check, bend radius check, separation clearance) route to the assembly ewis-installation-quality sub-skill.

- Top management review questions (review interval, review input coverage, action item tracking, review verdict) route to the as9100 management-review sub-skill.
- NDT personnel qualification questions (certification currency, recertification due date, vision examination, level progression, NAS 410) route to the ndt ndt-personnel-qualification sub-skill.

- Incoming purchase-order requirements review questions (special requirement classification, feasibility gates, order acceptance verdict) route to the as9100 order-requirements-review sub-skill.

- Small-shift process monitoring questions (tabular CUSUM statistics and first signal, EWMA recursion with time-varying limits, small shift detection verdict) route to the as9100 cusum-ewma-monitoring sub-skill.

- Solid rivet installation quality questions (rivet length selection, driven shop head geometry bands, squeeze force, hole fill clearance) route to the assembly solid-rivet-installation-quality sub-skill.
- Attribute control chart questions (p-chart, np-chart, c-chart, u-chart, fraction nonconforming, defects per unit, binomial and Poisson limits) route to the as9100 attribute-control-charts sub-skill.
- Attribute gage agreement questions (Cohen kappa, Fleiss kappa, inspector agreement on go no-go judgments) route to the as9100 attribute-agreement-analysis sub-skill.
- Individuals chart questions (one measurement per lot, moving range, destructive test monitoring, no subgroups) route to the as9100 individuals-and-moving-range-chart sub-skill.


## Install

To install only this pack, copy or symlink each leaf folder above into
your host's skills directory (see README Install for per-host commands).
- Key characteristic identification and variation management questions route to the as9103 key-characteristic-management sub-skill.
- Laser shearography questions (setup sizing, phase to strain conversion, scan plan, disbond disposition) route to the ndt shearography-inspection sub-skill.
- Internal audit program questions (audit schedule, auditor independence, audit sample size, finding classification, closure verification) route to the as9100 internal-quality-audit sub-skill.
- Leak testing questions (pressure decay, vacuum decay, helium mass spectrometer, bubble test, leak rate acceptance) route to the ndt leak-testing sub-skill.
- Gage bias and linearity study questions (per-level bias, linearity regression, bias significance t test, percent of reference band) route to the as9100 gage-linearity-bias-study sub-skill.

- Lot acceptance questions (attribute sampling plan selection by lot size code letter and AQL, accept and reject numbers, operating-characteristic probability of acceptance) route to the as9100 acceptance-sampling sub-skill.
- ANOVA gage R and R questions (two-way variance component decomposition, operator by part interaction F test, percent GRR verdict and distinct categories for replicated studies) route to the as9100 gage-rr-anova sub-skill.
- Variables lot acceptance questions (measurement-based k-method plan by lot size code letter and AQL, form-Q statistic from the specification limit and sample statistics, acceptability-constant verdict, estimated percent nonconforming) route to the as9100 variables-acceptance-sampling sub-skill.
