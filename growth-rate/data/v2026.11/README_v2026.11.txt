GRESO WHOLE-ATMOSPHERE (COLUMN) CO2 GROWTH RATE FROM OCO-2 -- RELEASE v2026.11
==============================================================================
OCO Science Applications and Partnerships Center (OCO-SAC), Caltech
Authors: Sudhanshu Pandey (Caltech), Christopher W. O'Dell (CIRA, Colorado State
  University), Christian Frankenberg (Caltech), Junjie Liu (Jet Propulsion
  Laboratory, Caltech), Vivienne H. Payne (Jet Propulsion Laboratory, Caltech)
  and Paul O. Wennberg (Caltech).
Contact: [contact e-mail]
Built: 2026-11-11T03:57:16Z   Data end (OCO-2): 2026-10-31

DRAFT -- placeholders are in [brackets].

--------------------------------------------------------------------------------
USE OF THESE DATA
--------------------------------------------------------------------------------
Licence: [Licence: CC BY 4.0 proposed — confirm]
  (applies to the GRESO values; third-party values keep their own terms, see
  THIRD-PARTY VALUES INCLUDED below)
Please cite:
  Pandey, S., O'Dell, C. W., Frankenberg, C., Liu, J., Payne, V. H., & Wennberg, P. O. (2026). GRESO OCO-2 whole-atmosphere CO₂ growth rates, release v2026.11. OCO Science Applications and Partnerships Center, Caltech. [dashboard base URL]. [data DOI].
and the method:
  Pandey, S., Miller, J. B., Basu, S., Liu, J., Weir, B., Byrne, B., Chevallier, F., Bowman, K. W., Liu, Z., Deng, F., O'Dell, C. W., & Chatterjee, A. (2024). Toward low-latency estimation of atmospheric CO2 growth rates using satellite observations: Evaluating sampling errors of satellite and in situ observing approaches. AGU Advances, 5, e2023AV001145. https://doi.org/10.1029/2023AV001145
Please also acknowledge the input data:
  OCO-2 Lite v11.2r, doi:10.5067/70K2B2W8MNGY; OCO-2 Lite v11.3r, doi:10.5067/C4OENLFCYVSA;
  ACOS GOSAT v11, doi:10.5067/UAY6VJYTS8OD (NASA GES DISC).
  OCO-2 for 1–31 Oct 2026: preliminary forward-processing data from the OCO-2
  team (product FwDaily_B11301_r01), to be replaced by the public data.
Disclaimer: [OCO-SAC disclaimer wording — from Kim]

--------------------------------------------------------------------------------
WHAT THIS IS
--------------------------------------------------------------------------------
The rate at which CO2 accumulates in the whole atmosphere, measured from the
column-average dry-air CO2 mole fraction (XCO2) retrieved by NASA's Orbiting
Carbon Observatory-2 (OCO-2), using the GRESO method (Growth Rate from Satellite
Observations; Pandey et al. 2024). GOSAT values computed with the same chain are
included as an optional cross-check layer. This is the whole-atmosphere (column) CO2 growth rate
from OCO-2 (GRESO); it complements, and is anchored by comparison with, the NOAA
GML surface marine boundary-layer (MBL) record.

GRESO averages OCO-2 data between 50S and 50N, where coverage is good all year;
CO2 added or removed further poleward mixes into this band within weeks to months,
so the result tracks the whole atmosphere.

--------------------------------------------------------------------------------
METHOD (as the code runs)
--------------------------------------------------------------------------------
GRESO (Pandey et al. 2024, doi:10.1029/2023AV001145), method version GRESO 1.x (baseline 2026-01-12, 16-day bins dated at their effective time, seasonal fit solved exactly). Input: OCO-2 v11 10-s XCO₂ (v11.2r through 2023, v11.3r from 2024, preliminary forward-processing data for 1–31 Oct 2026), land + ocean (target mode excluded), retrieval uncertainty < 2 ppm. Each 16-day repeat cycle is binned to 5°×5° cells (median), averaged along each latitude row and area-weighted across rows. Each 16-day bin is dated at its effective time, the area-weighted mean time of the soundings it uses (the same weights as the XCO₂ mean), not at the window's midpoint. Seasonal cycle: least-squares fit (solved exactly) of a cubic polynomial plus four annual harmonics over the whole record; the harmonics are subtracted. The deseasonalized series is gap-filled linearly and smoothed with a 7-window (7×16-day ≈ 112-day) running mean. Monthly growth = trend(1st of next month) − trend(1st of month), ×12 for ppm/yr, displayed with a 5-month running mean. Annual growth = trend(1 Jan Y+1) − trend(1 Jan Y), not the mean of the displayed monthly values. Annual 1σ = √(retrieval² + smoothing² + 0.04²): retrieval = spread over 40 decile subsets of four retrieval parameters, smoothing = spread over 6 smoothing widths, 0.04 ppm/yr = OSSE sampling error.

--------------------------------------------------------------------------------
DEFINITIONS AND UNITS
--------------------------------------------------------------------------------
Annual growth rate G_Y = trend(00:00 1 Jan Y+1) - trend(00:00 1 Jan Y)   [ppm/yr]
  (the same calendar-year concept as NOAA's Dec/Jan-based annual increase).
  It is NOT the mean of the displayed monthly values (those are smoothed across
  year boundaries; e.g. 2015 monthly mean 2.93 vs annual 2.99).
Monthly increment g_m = trend(1st of month m+1) - trend(1st of month m) [ppm/month].
  Twelve increments sum to the annual value (exactly, before rounding).
Displayed monthly growth = 5-month running mean of 12 x g_m             [ppm/yr].
ppm = micromol/mol of dry air (column average for OCO-2/GOSAT).
Mass units: 1 ppm = 2.124 PgC (Global Carbon Budget convention);
  1 PgC = 3.664 GtCO2; so 1 ppm/yr = 2.124 PgC/yr = 7.78 GtCO2/yr,
  and 1 ppm/month = 25.49 PgC/yr.
Airborne fraction AF = 2.124 x G / (E_FF + E_LUC), annual only (monthly AF is
  not meaningful). E_FF excludes the cement-carbonation sink (GCB definition).

--------------------------------------------------------------------------------
UNCERTAINTY
--------------------------------------------------------------------------------
Annual 1-sigma (OCO-2) = sqrt(retrieval^2 + smoothing^2 + 0.04^2), typically
0.07-0.11 ppm/yr (mean 0.088 ppm/yr = 0.19 PgC/yr).
  retrieval: SD over 40 reruns, each on one decile of one of four retrieval
             parameters (co2_grad_del, dpfrac, albedo_wco2, dp_sco2);
  smoothing: SD over 6 trend-smoothing widths;
  0.04 ppm/yr: whole-atmosphere sampling error of GRESO from the OSSE in
             Pandey et al. (2024) (surface MBL network: 0.12 ppm/yr).
Constant retrieval biases cancel in the differencing; only biases that drift in
time matter. Adjacent-year errors are anticorrelated (shared 1 Jan anchor).
GOSAT: smoothing spread + 0.08 ppm/yr floor only (no retrieval term).
OCO-2 + GOSAT (columns oco2_gosat_mean_*, years with both): the satellite series
the annual chart shows by default (GOSAT on; GOSAT alone before 2015) is the
mean of the two, with 1-sigma = sqrt((s_OCO2^2 + s_GOSAT^2)/2 + ((OCO2 - GOSAT)/2)^2):
the products' own errors plus half their difference. Headline numbers stay OCO-2.
Monthly values: no per-month uncertainty is published; the error is of order
0.7 ppm/yr (0.06 ppm/month), and recent months are revised (see STATUS).

--------------------------------------------------------------------------------
STATUS FLAGS
--------------------------------------------------------------------------------
Each monthly value gets a status from its age: the number of whole months between the end of that month and the data end (31 Oct 2026). Age 0–2 = early estimate (dashed; revised most as data arrive); 3–5 = provisional (still revised; about 0.7 ppm/yr RMS at 3 months, falling to 0.24 ppm/yr at 5 [revision sizes from an earlier pipeline run; recompute on this release]); 6 or more = final. In this release April 2026 and earlier are final, May–July 2026 provisional and August–September 2026 early. A calendar-year value is provisional until data through the end of February of the following year are in (normally released about April), then final. No partial-year annual values are published. The same rule applies to every chart and file.
Typical latency: first estimate about 6-8 weeks after the month ends; stable
after about 4-6 months; annual value final once data through February of the
next year are released (normally about April).
Headline "last 12 months" value: Change of the deseasonalized OCO-2 XCO₂ trend between 00:00 UTC on 2025-10-01 and 2026-10-01: the same definition as the annual value (1 Jan → 1 Jan), shifted so that the window ends with September 2026, the newest month with observations (August–September 2026 are early estimates, so the value will still be revised). The trend is used as published (it is already smoothed and is not smoothed again). No NOAA value for these dates: its monthly trend (co2_mm_gl.txt, file created 2026-10-09) ends in mid-July 2026, before the window ends.

--------------------------------------------------------------------------------
INPUT VERSIONS
--------------------------------------------------------------------------------
Provenance: OCO-2 Lite v11.2r through 2023, v11.3r from 2024.
OCO-2:     OCO-2 Lite 10-s XCO₂: v11.2r (doi:10.5067/70K2B2W8MNGY) through 2023-12-31 and v11.3r (doi:10.5067/C4OENLFCYVSA) from 2024-01-01, through 2026-09-30; then preliminary forward-processing (FP) data from the OCO-2 team (product FwDaily_B11301_r01), 2026-10-01 through 2026-10-31. Method GRESO 1.x (baseline 2026-01-12, 16-day bins dated at their effective time, seasonal fit solved exactly) (Pandey et al. 2024).
           Input file OCO2_b11.3-lite_10sec_GOOD_20140906-20261031_RP+FP_2611051636.h5;
           GRESO code commit 6b2a7785 (baseline 2026-01-12) with each 16-day bin
           dated at its effective time, handoff 2026-11-07.
GOSAT:     ACOS GOSAT v11 Lite soundings (NASA GES DISC, doi:10.5067/UAY6VJYTS8OD), filtered subset acosGOSATv11_lite_20090418-20261031_filtered_tiny.h5, 2009-04-18 → 2026-10-31; same GRESO chain as OCO-2. On the main page, the annual chart and table open with GOSAT on (GOSAT alone for 2010–2014, the mean of OCO-2 and GOSAT from 2015); on the monthly chart it is off until switched on. Uncertainty = smoothing spread + 0.08 ppm/yr floor (no retrieval term). Same status rule as OCO-2.
NOAA:      NOAA GML global marine boundary layer (MBL); Lan, X., Tans, P. and Thoning, K.W., Trends in globally-averaged CO2 determined from NOAA GML measurements, doi:10.15138/9N0H-ZH07. Annual: co2_gr_gl.txt (file created 2026-10-09). Monthly ‘derived from NOAA trend’ is our derivative, not a NOAA product: 12 × the change of the co2_mm_gl.txt trend column (file created 2026-10-09) from the 1st of each month to the 1st of the next (the trend linearly interpolated to 00:00 UTC on those days, as for the annual and 12-month values), then the same 5-month running mean as the OCO-2 values (last two months unsmoothed). It covers the same dates as the OCO-2 monthly values and ends with June 2026, because NOAA’s trend ends in mid-July 2026. Redistributed with this citation and file date; NOAA revises its values, so take the current files from https://gml.noaa.gov/ccgg/trends/global.html for new work.
Emissions: Friedlingstein et al. (2026), Global Carbon Budget 2025, Earth Syst. Sci. Data 18, 3211-3288, doi:10.5194/essd-18-3211-2026; data doi:10.18160/GCP-2025 (CC BY 4.0): fossil CO₂ excluding the cement-carbonation sink, plus land-use change, through 2024. 2025 onward: low-latency estimate = Carbon Monitor, carbonmonitor.org (Liu et al. 2020, arXiv:2004.13614) × 1.020 (mean GCB/Carbon Monitor ratio 2022–24) plus linearly extrapolated land-use change (provisional; not a budget number). Monthly series: each GCB year spread over the months with Carbon Monitor's monthly pattern (2015–2018 its average pattern, 2019–2024 that year's Carbon Monitor months scaled to the GCB total), land-use change flat within each year, then a fixed seasonal cycle removed. August–September 2026: the same months a year earlier times Carbon Monitor's growth over the year, from Carbon Monitor's data of 10 November 2026 (its newer files have a different seasonal shape, so their monthly values are not joined on directly).

--------------------------------------------------------------------------------
DATA GAPS
--------------------------------------------------------------------------------
  2017-07-31 to 2017-09-19: OCO-2 safe mode: no data. The 16-day trend is linearly interpolated across the gap, so the Aug and Sep 2017 monthly values rest on the interpolation (flagged in the downloads)
  2026-07-28 to 2026-08-13: OCO-2 paused science observations 28 Jul–13 Aug 2026 (safe mode after an instrument anomaly); those days stay missing. The 16-day trend is interpolated across the gap, so the Aug 2026 monthly value rests partly on the interpolation (flagged in the downloads). This release uses OCO-2 data up to 30 Sep 2026 from the retrospective stream, which NASA expects to be of nominal quality after the gap (forward-stream data were of reduced quality until 17 Sep 2026), then preliminary forward-processing data for 1–31 Oct 2026

--------------------------------------------------------------------------------
FILES IN THIS RELEASE
--------------------------------------------------------------------------------
  greso_annual_v2026.11.csv          annual OCO-2 (2015-2025), GOSAT and NOAA MBL (2010-2025)
  greso_monthly_v2026.11.csv         monthly 2015-01 -> 2026-09 with status flags
  greso_zonal_monthly_v2026.11.csv   10-degree latitude bands, tidy
  greso_xco2_16day_v2026.11.csv      16-day global-mean XCO2 and smoothed trend
  greso_budget_annual_v2026.11.csv   PgC/yr, emissions, airborne fractions, implied sink
  greso_v2026.11.json                all of the above as one JSON file (the web-page
                                      data payload), plus the CPC ONI series
  README_v2026.11.txt, CHANGELOG.md, SHA256SUMS, greso_v2026.11.zip
  index.html                          file list for browsers (not in SHA256SUMS)
The folder data/latest/ holds the newest release with version-free names
(greso_annual_latest.csv, ..., README_latest.txt, greso_latest.zip) and its own
SHA256SUMS; link to those names to always get the newest release, and to
data/v2026.11/ to cite a frozen release.
Each CSV begins with '#' comment lines describing its columns.
Missing values are empty fields (CSV) or null (JSON).

Annual summary (OCO-2, ppm/yr, 1-sigma, PgC/yr, status):
  2015    2.99 ± 0.08    6.35   final
  2016    2.71 ± 0.08    5.76   final
  2017    2.05 ± 0.09    4.35   final
  2018    2.48 ± 0.11    5.27   final
  2019    2.74 ± 0.10    5.82   final
  2020    2.32 ± 0.11    4.93   final
  2021    2.28 ± 0.10    4.84   final
  2022    1.92 ± 0.07    4.08   final
  2023    3.10 ± 0.07    6.58   final
  2024    3.48 ± 0.08    7.39   final
  2025    1.97 ± 0.08    4.18   final

--------------------------------------------------------------------------------
KNOWN ISSUES AND CAVEATS
--------------------------------------------------------------------------------
  - The v11.2r → v11.3r splice falls on 1 Jan 2024, the anchor shared by the 2023 and 2024 annual values.
  - ‘All’ includes snapshot-area-map (SAM) soundings, so it is not exactly land ∪ ocean.
  - GOSAT uncertainty has no retrieval term (smoothing + 0.08 ppm/yr floor only); GOSAT is not fully independent of OCO-2 (shared ACOS algorithm heritage).
  - Monthly values carry a larger, unquantified error (order 0.7 ppm/yr); the newest months are revised.
  - Aug and Sep 2017 and Aug 2026 monthly values rest on the trend interpolated across OCO-2's data gaps (flagged in the monthly and latitude-band files).
  - GOSAT's 10° band values for January 2015 and January 2026, months without any GOSAT data, come from the interpolation across GOSAT's data gaps alone (flagged in the latitude-band file).
  - Since 2024 the OCO-2 − GOSAT trend difference oscillates seasonally (0.1–0.17 ppm); do not over-read month-to-month differences between the sensors.
  - Latitude-band values are the rate of change of XCO₂ over a band, not regional fluxes. The 10° bands come from a separate, closely related run of the method.
  - The 2025–26 slowdown is not falling emissions: fossil emissions were flat or up about 1%.
  - The 10° bands use complete 16-day windows only, so they use OCO-2 data to 20 Oct 2026 and GOSAT data to 25 Oct 2026, 11 and 6 days less than the global series.
  - The OCO-2 data for 1–31 Oct 2026 are preliminary forward-processing (FP) data from the OCO-2 team (product FwDaily_B11301_r01; no data on 6 Oct 2026), used before the public retrospective data for that period are released. The monthly values for Jun–Sep 2026 rest on them (flag preliminary_fp_data) and may change when the public data are used.

--------------------------------------------------------------------------------
THIRD-PARTY VALUES INCLUDED (with source, file date or version, and citation)
--------------------------------------------------------------------------------
Third-party values are included with their source, file date or version, and citation: NOAA GML marine-boundary-layer growth (annual and our monthly derivative) and NOAA-based airborne fractions (Lan, X., Tans, P. and Thoning, K.W., Trends in globally-averaged CO2 determined from NOAA GML measurements, doi:10.15138/9N0H-ZH07; files created 2026-10-09); Global Carbon Budget 2025 emissions and atmospheric growth term (Friedlingstein et al. (2026), Global Carbon Budget 2025, Earth Syst. Sci. Data 18, 3211-3288, doi:10.5194/essd-18-3211-2026; data doi:10.18160/GCP-2025 (CC BY 4.0)); and 2025 low-latency emissions derived from Carbon Monitor, carbonmonitor.org (Liu et al. 2020, arXiv:2004.13614).
NOAA GML global MBL CO2 trends and growth rates: https://gml.noaa.gov/ccgg/trends/global.html
  annual growth: https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_gr_gl.txt (file created 2026-10-09)
  monthly trend: co2_mm_gl.txt (file created 2026-10-09)
  NOAA revises its values; take the current files from NOAA for new work.
Global Carbon Budget 2025: https://doi.org/10.5194/essd-18-3211-2026 ; data https://doi.org/10.18160/GCP-2025
Carbon Monitor: https://carbonmonitor.org/
NOAA CPC Oceanic Nino Index: https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt
OCO-2 data-gap notice (Jul-Aug 2026): https://www.earthdata.nasa.gov/data/alerts-outages/oco-2-instrument-anomaly-from-july-28-august-13-2026

--------------------------------------------------------------------------------
ACKNOWLEDGEMENTS
--------------------------------------------------------------------------------
NASA OCO-2 project and GES DISC; ACOS/GOSAT teams (JAXA, NIES, MOE, NASA);
NOAA Global Monitoring Laboratory; Global Carbon Project; Carbon Monitor;
NOAA Climate Prediction Center.
