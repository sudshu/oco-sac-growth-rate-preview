# GRESO OCO-2 growth-rate data: CHANGELOG

## v2026.11 (built 2026-11-11T03:57:16Z) (DRAFT)

- Data end 2026-10-31 (public v11.3r Lite data, retrospective stream, to 30 Sep 2026, then preliminary
  forward-processing data for 1–31 Oct 2026); was 2026-07-28. OCO-2 has no data 28 Jul-13 Aug 2026 (safe mode);
  see the README's data gaps.
- Preliminary data: the OCO-2 data for 1–31 Oct 2026 are forward-processing (FP) data from the OCO-2 team
  (product FwDaily_B11301_r01; no data on 2026-10-06), used before the public retrospective data for that period
  are released. With them the monthly series reaches 2026-09. Flag preliminary_fp_data marks what rests on them:
  the monthly values 2026-06, 2026-07, 2026-08, 2026-09, the 10-degree band months 2026-05, 2026-06, 2026-07,
  2026-08, 2026-09 and the 16-day windows that hold them. A later release will use the public data.
- No experimental forecast on the web page in this release (v2026.10's page showed the outlook of 8 Oct 2026);
  the forecast will be calculated later. The climate stripes under the monthly chart stay, observed months only.
  (The forecast was never part of these files.)
- Method: each 16-day bin is now dated at its effective time, the area-weighted mean time of the soundings it
  uses (the same weights as the XCO2 mean), instead of the midpoint of its 16-day window, before the series is
  deseasonalized and interpolated to month starts. This applies to OCO-2 and GOSAT, the global series, the land
  and ocean subsets and the 10-degree bands. Bins with data spread over the window barely move (median shift of
  the global OCO-2 bins 0.1 days); bins cut by an outage or by the data end move to where their data are (up to
  5.9 days here).
- Method: GRESO's seasonal fit (a cubic polynomial plus four annual harmonics over the whole record) is now
  solved exactly, as the linear least-squares problem it is. GRESO used scipy's iterative leastsq, which stopped
  short of the optimum on this badly conditioned fit and could give slightly different answers on different
  computers. On this release's data the change moves the OCO-2 monthly values by up to 0.09 ppm/yr (median 0.03)
  and the 10-degree band values by up to 0.07 ppm/yr, and leaves the annual values unchanged at two decimals. It
  applies to OCO-2 and GOSAT, the global series, the land and ocean subsets, the 10-degree bands and the
  uncertainty ensembles.
- Method label: GRESO 1.x (baseline 2026-01-12, 16-day bins dated at their effective time, seasonal fit solved
  exactly).
- GOSAT: ACOS GOSAT v11 Lite soundings (NASA GES DISC, doi:10.5067/UAY6VJYTS8OD), filtered subset
  acosGOSATv11_lite_20090418-20261031_filtered_tiny.h5, 2009-04-18 → 2026-10-31. NOAA GML files created
  2026-10-09.
- Contents: monthly 2015-01 -> 2026-09 (was 2026-06), 10-degree latitude bands 2015-01 -> 2026-09 (was 2026-04).
  The band run now leaves its last three 16-day bins unsmoothed, as the global series does, instead of needing a
  full 7-bin window.
- File greso_xco2_16day_v2026.11.csv: time_year is now the effective time and the column date_mid is replaced by
  date (the effective date); the new columns time_year_window_mid and date_window_mid hold the window midpoints
  (the earlier times). The JSON's xco2 object has the same new fields (t_window_mid, date_window_mid).
- Months resting on the trend interpolated across a data gap (flag trend_interpolated_data_gap): 2017-08,
  2017-09, 2026-08.
- Headline 12-month value: 2025-10-01 -> 2026-10-01 (the newest 12 months with observations).
- GOSAT 10-degree bands: 2026-01 now holds the value of the band run's own interpolation across GOSAT's data gap
  (19 Dec 2025 to 3 Feb 2026), which the run used to blank. Flag trend_interpolated_data_gap on the GOSAT months
  without any GOSAT data (2015-01, 2026-01).
- Emissions extended to 2026-09 (was 2026-06); every earlier value unchanged. August–September 2026: the same
  months a year earlier times Carbon Monitor's growth over the year, from Carbon Monitor's data of 10 November
  2026.

### Changes since the previous release (v2026.10)
- Annual OCO-2 (ppm/yr): largest revision 0.01; 2015 3.00 -> 2.99, 2018 2.47 -> 2.48, 2019 2.75 -> 2.74, 2020
  2.31 -> 2.32, 2021 2.29 -> 2.28, 2023 3.11 -> 3.10, 2024 3.47 -> 3.48, 2025 1.96 -> 1.97.
- Annual GOSAT (ppm/yr): largest revision 0.04; 2011 1.78 -> 1.77, 2014 2.11 -> 2.15, 2015 2.81 -> 2.77, 2025
  1.96 -> 1.98.
- Annual NOAA MBL (ppm/yr): largest revision 0.01; 2011 1.73 -> 1.74, 2012 2.42 -> 2.41, 2020 2.33 -> 2.32, 2023
  2.70 -> 2.69.
- Monthly OCO-2 (ppm/yr): largest revision of a month final in v2026.10 0.16 (2019-11); months provisional or
  early in v2026.10: 2026-01 1.72 -> 1.62, 2026-02 1.47 -> 1.47, 2026-03 1.34 -> 1.35, 2026-04 1.28 -> 1.54,
  2026-05 1.53 -> 1.95, 2026-06 1.53 -> 2.66; new months 2026-07 -> 2026-09.
- Monthly GOSAT (ppm/yr): largest revision of a month final in v2026.10 0.12 (2019-02); of the months
  provisional or early in v2026.10, largest 1.23 (2026-06); new months 2026-07 -> 2026-09.
- Monthly NOAA-derived (ppm/yr): largest revision of a month final in v2026.10 0.13 (2024-05); of the months
  provisional or early in v2026.10, largest 0.76 (2026-05); new month 2026-06.
- 10-degree bands, OCO-2 (ppm/yr): largest revision of a month final in v2026.10 0.35 (2017-10, band centred at
  -45 degrees).
- 10-degree bands, GOSAT (ppm/yr): largest revision of a month final in v2026.10 0.22 (2025-07, band centred at
  -45 degrees).

## v2026.10 (built 2026-11-07T22:22:59Z) -- first release (DRAFT)

- First versioned release on the OCO-SAC dashboard [dashboard base URL].
- OCO-2 series: method GRESO 1.x (baseline 2026-01-12); input v11.2r through 2023, v11.3r from 2024.
- Data end 2026-07-28 (public v11.3r Lite archive end, checked 2026-10-08).
- Contents: annual (OCO-2 2015-2025, GOSAT and NOAA MBL 2010-2025, OCO-2 + GOSAT mean 2015-2025), monthly
  2015-01 -> 2026-06, 10-degree latitude bands to 2026-04, 16-day XCO2, annual budget/airborne fractions.
- Third-party values (NOAA GML, Global Carbon Budget 2025, Carbon Monitor-based emissions) are included with
  source, file date and citation.

### Notes
- Provenance: OCO-2 Lite v11.2r through 2023, v11.3r from 2024.
- Calendar-year values are published only for complete years (earlier exploratory files labelled a trailing
  12-month sum as a calendar year).

### Changes since the previous release
- None (first release). Future entries will list the maximum revision per year and per month.
