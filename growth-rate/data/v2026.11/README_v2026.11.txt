GRESO WHOLE-ATMOSPHERE (COLUMN) CO2 GROWTH RATE USING SATELLITE DATA -- RELEASE v2026.11
========================================================================================
OCO Science Applications and Partnerships Center (OCO-SAC), Caltech
Creator: Sudhanshu Pandey (Caltech; Jet Propulsion Laboratory, Caltech).
Contact: Sudhanshu Pandey, sudhanshu.pandey@caltech.edu
Built: 2026-11-14T01:51:51Z   Data end: 2026-10-31 (OCO-2 and GOSAT)

HOW TO CITE
  Pandey, S., O'Dell, C. W., Frankenberg, C., Payne, V. H., & Wennberg, P. O.
    (2026). GRESO Portal: whole-atmosphere CO2 growth rates from satellite
    observations, data release v2026.11. OCO Science Applications and
    Partnerships Center, Caltech. https://doi.org/10.82941/ocosac.greso.co2
  This release on CaltechDATA:
    https://doi.org/10.82941/ocosac.greso.co2.data.v2026.11
  Method: Pandey, S., Miller, J. B., Basu, S., Liu, J., Weir, B., Byrne, B.,
    Chevallier, F., Bowman, K. W., Liu, Z., Deng, F., O'Dell, C. W., &
    Chatterjee, A. (2024). Toward low-latency estimation of atmospheric CO2
    growth rates using satellite observations: Evaluating sampling errors of
    satellite and in situ observing approaches. AGU Advances, 5, e2023AV001145.
    https://doi.org/10.1029/2023AV001145
  Licence: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/) for the
    GRESO values; third-party values keep their own terms (see SOURCES).

WHAT THE DATA ARE
  The rate at which CO2 builds up in the whole atmosphere, from the
    column-average CO2 (XCO2) measured by two satellites, NASA's OCO-2 and
    Japan's GOSAT, each processed with the GRESO method (Growth Rate from
    Satellite Observations; Pandey et al. 2024). The annual satellite series is
    GOSAT alone before 2015 and the mean of OCO-2 and GOSAT from 2015, with
    1-sigma = sqrt((s_OCO2^2 + s_GOSAT^2)/2 + ((OCO2 - GOSAT)/2)^2). Monthly and
    latitude-band values are given for each satellite. NOAA's surface values are
    included for comparison.

METHOD IN BRIEF
  Every 16 days the XCO2 soundings are binned into 5x5-degree cells (median) and
    averaged over 50S-50N with area weights. The seasonal cycle (a cubic
    polynomial plus four annual harmonics, fitted to the whole record) is
    removed, and the result is smoothed with a 7 x 16-day running mean (the
    first and last three windows unsmoothed): the trend.
  Annual growth rate = trend(1 Jan of the next year) - trend(1 Jan), in ppm/yr.
  Monthly growth rate = (trend(1st of the next month) - trend(1st)) x 12, in
    ppm/yr, shown as a 5-month running mean (the first and last two months
    unsmoothed).
  1 ppm = 2.124 PgC; 1 PgC = 3.664 GtCO2.

STATUS AND FLAGS
  status: early (0-2 months after the month ends), provisional (3-4 months) or
    final (later); recent months change as more data arrive. A year is
    provisional until data through February of the next year are in.
  flag preliminary_fp_data: rests on preliminary OCO-2 forward-processing data
    (1-31 Oct 2026): the monthly values 2026-06 to 2026-09 and the latitude
    bands 2026-05 to 2026-09 (the bands use complete 16-day windows). They may
    change when the public data are used.
  flag trend_interpolated_data_gap: rests on the trend interpolated across a
    data gap: OCO-2 2017-08, 2017-09, 2026-08; GOSAT 2015-01, 2026-01
    (latitude-band file). The monthly file's flags are OCO-2's.

FILES
  greso_monthly_v2026.11.csv        monthly growth rate, 2015-01 to 2026-09
  greso_annual_v2026.11.csv         annual growth rate with 1-sigma uncertainty
  greso_zonal_monthly_v2026.11.csv  growth rate in 10-degree latitude bands
  greso_xco2_16day_v2026.11.csv     16-day global-mean OCO-2 XCO2 and its trend
  greso_budget_annual_v2026.11.csv  OCO-2 PgC/yr, emissions, airborne fraction
  greso_cube_oco2_v2026.11.nc       OCO-2 XCO2 per 5x5-degree cell and 16 days
  greso_cube_gosat_v2026.11.nc      the same for GOSAT
  greso_growth_from_cube.py         computes the global growth rates from a cube
  greso_v2026.11.json               the web page's data in one file
  CHANGELOG.txt and greso_v2026.11.zip (all files in one ZIP).
  Script: python greso_growth_from_cube.py greso_cube_oco2_v2026.11.nc
    (Python 3.9 or later, numpy, and netCDF4 or h5py). It gives the global
    16-day series and the monthly and annual growth rates, not the
    uncertainties, the land and ocean values or the latitude bands.
  CSV files start with '#' lines describing their columns; missing values are
    empty.

ANNUAL GROWTH RATE (ppm/yr, 1-sigma)
  year   satellites      OCO-2           GOSAT           status
  2010   2.38 +/- 0.09                   2.38 +/- 0.09   final
  2011   1.77 +/- 0.11                   1.77 +/- 0.11   final
  2012   2.47 +/- 0.10                   2.47 +/- 0.10   final
  2013   2.39 +/- 0.10                   2.39 +/- 0.10   final
  2014   2.15 +/- 0.10                   2.15 +/- 0.10   final
  2015   2.88 +/- 0.15   2.99 +/- 0.08   2.77 +/- 0.12   final
  2016   2.71 +/- 0.08   2.71 +/- 0.08   2.72 +/- 0.08   final
  2017   2.12 +/- 0.11   2.05 +/- 0.09   2.18 +/- 0.08   final
  2018   2.46 +/- 0.10   2.48 +/- 0.11   2.44 +/- 0.10   final
  2019   2.75 +/- 0.10   2.74 +/- 0.10   2.76 +/- 0.09   final
  2020   2.33 +/- 0.10   2.32 +/- 0.11   2.33 +/- 0.08   final
  2021   2.29 +/- 0.09   2.28 +/- 0.10   2.29 +/- 0.09   final
  2022   1.90 +/- 0.08   1.92 +/- 0.07   1.89 +/- 0.09   final
  2023   3.12 +/- 0.08   3.10 +/- 0.07   3.13 +/- 0.08   final
  2024   3.42 +/- 0.11   3.48 +/- 0.08   3.36 +/- 0.09   final
  2025   1.98 +/- 0.09   1.97 +/- 0.08   1.98 +/- 0.10   final

SOURCES
  OCO-2: OCO-2 Lite 10-s XCO2 from NASA GES DISC, v11.2r
    (doi:10.5067/70K2B2W8MNGY) through 2023 and v11.3r
    (doi:10.5067/C4OENLFCYVSA) from 2024; for 1-31 Oct 2026 preliminary
    forward-processing data from the OCO-2 team (FwDaily_B11301_r01).
  GOSAT: ACOS GOSAT v11 Lite from NASA GES DISC (doi:10.5067/UAY6VJYTS8OD).
  NOAA: global marine boundary layer CO2, co2_gr_gl.txt and co2_mm_gl.txt (files
    created 2026-10-09), https://gml.noaa.gov/ccgg/trends/global.html; Lan, X.,
    Tans, P. and Thoning, K.W., Trends in globally-averaged CO2 determined from
    NOAA GML measurements, doi:10.15138/9N0H-ZH07.
  Emissions: Friedlingstein et al. (2026), Global Carbon Budget 2025, Earth
    Syst. Sci. Data 18, 3211-3288, doi:10.5194/essd-18-3211-2026; data
    doi:10.18160/GCP-2025 (CC BY 4.0), through 2024; from 2025 Carbon Monitor,
    carbonmonitor.org (Liu et al. 2020, arXiv:2004.13614), data of 10 November
    2026, x 1.020, plus extrapolated land-use change (provisional).
  ENSO index in the JSON: NOAA CPC Oceanic Nino Index,
    https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt
