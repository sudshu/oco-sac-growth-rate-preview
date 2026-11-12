#!/usr/bin/env python3
"""Compute GRESO CO2 growth rates from a GRESO 5x5-degree, 16-day XCO2 cube.

Part of the GRESO whole-atmosphere CO2 growth-rate data of the OCO Science Applications and Partnerships Center
(OCO-SAC), Caltech. Run on the cube files of a release (greso_cube_oco2_<release>.nc, greso_cube_gosat_<release>.nc),
it gives that release's 16-day global XCO2 series and trend and its monthly and annual growth rates. The method is
GRESO (Pandey et al. 2024, AGU Advances 5, e2023AV001145, https://doi.org/10.1029/2023AV001145), in the order the GRESO
code runs it:

1. Global 16-day series. In each 16-day window, average the cell medians along each 5-degree latitude row, then take
   the area-weighted mean over the rows with data (weight = the area of a cell in that row). The window is dated at its
   effective time: the same weighted mean, taken over the cells' mean sounding times. A window without data keeps its
   midpoint as its time and has no value.
2. Seasonal cycle. Fit a cubic polynomial (in centred, scaled time) plus four annual harmonics (sin and cos of
   2*pi*k*t, k = 1..4, t in decimal years) to the windows with data, by linear least squares, and subtract the
   harmonics.
3. Trend. Interpolate the deseasonalized series linearly to every window (this fills the gaps), then take a 7-window
   running mean. The first and last 3 windows stay unsmoothed.
4. Monthly growth. Interpolate the trend linearly to 00:00 on the 1st of each month. The increment
   g = trend(1st of next month) - trend(1st of month) is in ppm/month, and 12 * g in ppm/yr. The monthly growth rate
   is the 5-month running mean of 12 * g; the first and last 2 months stay unsmoothed. The months start in January of
   the first full calendar year of the cube (2015 for OCO-2, 2010 for GOSAT; see --first-year).
5. Annual growth for each complete calendar year Y = the sum of its 12 increments
   = trend(1 Jan Y+1) - trend(1 Jan Y), in ppm/yr. It is not the mean of the monthly growth rates.

The annual uncertainties of the release come from the individual soundings (40 retrieval-parameter subsets,
6 smoothing widths, a sampling term) and are not computed here.

Usage:
  python greso_growth_from_cube.py greso_cube_oco2_v2026.11.nc [greso_cube_gosat_v2026.11.nc ...] [--out DIR]
                                   [--first-year YEAR]
For each cube it writes <cube name>_16day.csv, <cube name>_monthly.csv and <cube name>_annual.csv to DIR (default: the
current folder) and prints the annual growth rates. Needs Python 3.9 or later, numpy, and netCDF4 or h5py.

Released with the GRESO data under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/).
Contact: Sudhanshu Pandey, sudhanshu.pandey@caltech.edu
"""
from __future__ import annotations

import argparse
import math
import os
import sys
import warnings
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

NUMPOLY = 4             # polynomial terms of the seasonal fit (1, t, t^2, t^3: a cubic)
NUMHARM = 4             # annual harmonics of the seasonal fit
TREND_HALF_WIDTH = 3    # 7-window running mean of the deseasonalized series
MONTHLY_HALF_WIDTH = 2  # 5-month running mean of the monthly growth
CELL_DEG = 5.0          # cell size of the cube


# --- reading ---------------------------------------------------------------------------------------------------------
def read_cube(path: Path) -> dict:
    """The cube's variables as numpy arrays, with netCDF4 (or h5py if netCDF4 is not installed)."""
    names = ["lat", "time_bnds", "time_window_mid_decimal_year", "xco2", "sounding_time", "n_soundings"]
    reader = os.environ.get("GRESO_CUBE_READER", "")
    try:
        if reader == "h5py":
            raise ImportError
        import netCDF4
    except ImportError:
        import h5py
        with h5py.File(path, "r") as f:
            out = {k: f[k][()] for k in names}
            if "n_soundings_preliminary" in f:
                out["n_soundings_preliminary"] = f["n_soundings_preliminary"][()]
            units = f["time_bnds"].attrs["units"]
        out["time_units"] = units.decode() if isinstance(units, bytes) else str(units)
        return out
    with netCDF4.Dataset(path) as nc:
        nc.set_auto_mask(False)
        out = {k: nc[k][:] for k in names}
        if "n_soundings_preliminary" in nc.variables:
            out["n_soundings_preliminary"] = nc["n_soundings_preliminary"][:]
        out["time_units"] = nc["time_bnds"].units
    return out


# --- time ------------------------------------------------------------------------------------------------------------
def decimal_year(d: datetime) -> float:
    """Year + elapsed fraction of the calendar year (GRESO's decimal year)."""
    start, end = datetime(d.year, 1, 1), datetime(d.year + 1, 1, 1)
    return d.year + (d - start) / (end - start)


def from_decimal_year(y: float) -> datetime:
    """The inverse of decimal_year, rounded to the nearest second (as GRESO does)."""
    year = int(math.floor(y))
    start = datetime(year, 1, 1)
    d = start + timedelta(seconds=(datetime(year + 1, 1, 1) - start).total_seconds() * (y - year))
    whole = d.replace(microsecond=0)
    if d.microsecond > 500000 or (d.microsecond == 500000 and whole.second % 2 == 1):
        whole += timedelta(seconds=1)
    return whole


def next_month(d: datetime) -> datetime:
    return datetime(d.year + d.month // 12, d.month % 12 + 1, 1)


def month_starts(t_first: float, t_last: float) -> list:
    """00:00 on the 1st of each month from the first one at or after t_first to the last one at or before t_last."""
    a, b = from_decimal_year(t_first), from_decimal_year(t_last)
    m = datetime(a.year, a.month, 1)
    if m < a:
        m = next_month(m)
    out = []
    while m <= b:
        out.append(m)
        m = next_month(m)
    return out


# --- the method ------------------------------------------------------------------------------------------------------
def running_mean(a: np.ndarray, half: int) -> np.ndarray:
    """Centred running mean over 2*half + 1 points; the first and last `half` points stay as they are."""
    out = a.copy()
    for i in range(half, len(a) - half):
        out[i] = np.nanmean(a[i - half:i + half + 1])
    return out


def global_series(lat, xco2, sounding_time, time_mid):
    """Step 1: area-weighted global mean of each window and its effective time (window midpoint if no data)."""
    x = np.asarray(xco2, dtype=float)
    ts = np.where(np.isfinite(x), np.asarray(sounding_time, dtype=float), np.nan)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)       # rows without data: mean of nothing -> NaN
        row_x, row_t = np.nanmean(x, axis=2), np.nanmean(ts, axis=2)
    lat = np.asarray(lat, dtype=float)
    area = np.abs(np.sin(np.radians(lat + CELL_DEG / 2)) - np.sin(np.radians(lat - CELL_DEG / 2)))
    w = np.where(np.isfinite(row_x), area, 0.0)
    wsum = w.sum(axis=1)
    has = wsum > 0
    value = np.full(len(x), np.nan)
    time = np.asarray(time_mid, dtype=float).copy()
    value[has] = (w[has] * np.nan_to_num(row_x[has])).sum(axis=1) / wsum[has]
    time[has] = (w[has] * np.nan_to_num(row_t[has])).sum(axis=1) / wsum[has]
    return time, value


def harmonic_columns(t: np.ndarray) -> np.ndarray:
    return np.column_stack([f(2 * np.pi * k * t) for k in range(1, NUMHARM + 1) for f in (np.sin, np.cos)])


def deseasonalize(t: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Step 2: y minus the harmonic part of the least-squares fit (cubic polynomial + 4 annual harmonics)."""
    scale = t.std() or 1.0
    poly = np.vander((t - t.mean()) / scale, NUMPOLY, increasing=True)
    coef = np.linalg.lstsq(np.hstack([poly, harmonic_columns(t)]), y, rcond=None)[0]
    return y - harmonic_columns(t) @ coef[NUMPOLY:]


def growth_rates(time, value, first_year):
    """Steps 2-5. Returns the trend, the months, their decimal-year midpoints, increments [ppm/month], monthly growth
    [ppm/yr] and the annual growth {year: ppm/yr} of complete calendar years."""
    ok = np.isfinite(value)
    tv = time[ok]
    if np.any(np.diff(tv) <= 0):
        raise ValueError("window times with data are not increasing")
    trend = running_mean(np.interp(time, tv, deseasonalize(tv, value[ok])), TREND_HALF_WIDTH)
    order = np.argsort(time, kind="mergesort")
    ts, ys = time[order], trend[order]
    starts = month_starts(ts[0], ts[-1])
    edge = np.array([decimal_year(m) for m in starts])
    at = np.interp(edge, ts, ys)
    inc, mid = at[1:] - at[:-1], (edge[1:] + edge[:-1]) / 2
    keep = mid > first_year
    months = [m.strftime("%Y-%m") for m, k in zip(starts[:-1], keep) if k]
    inc, mid = inc[keep], mid[keep]
    monthly = running_mean(inc, MONTHLY_HALF_WIDTH) * 12.0
    annual = {}
    for i in range(0, len(months) - 11, 12):
        if months[i].endswith("-01") and months[i + 11].endswith("-12"):
            annual[int(months[i][:4])] = float(np.sum(inc[i:i + 12]))
    return trend, months, mid, inc, monthly, annual


# --- output ----------------------------------------------------------------------------------------------------------
def fmt(v, decimals=10) -> str:
    return "" if v is None or (isinstance(v, float) and not math.isfinite(v)) else f"{v:.{decimals}f}"


def write_csv(path: Path, comment: list, header: list, rows: list):
    with open(path, "w", newline="") as f:
        f.writelines(f"# {c}\n" for c in comment)
        f.write(",".join(header) + "\n")
        f.writelines(",".join(r) + "\n" for r in rows)


def process(path: Path, out: Path, first_year: int | None):
    c = read_cube(path)
    ref = datetime.strptime(c["time_units"].split("since", 1)[1].strip()[:19], "%Y-%m-%d %H:%M:%S")
    starts = [ref + timedelta(days=float(d)) for d in c["time_bnds"][:, 0]]
    if first_year is None:                      # the first full calendar year of the cube
        first_year = starts[0].year + (0 if (starts[0].month, starts[0].day) == (1, 1) else 1)
    time, value = global_series(c["lat"], c["xco2"], c["sounding_time"], c["time_window_mid_decimal_year"])
    trend, months, mid, inc, monthly, annual = growth_rates(time, value, first_year)

    note = [f"Computed by greso_growth_from_cube.py from {path.name}.", "GRESO method: Pandey et al. (2024), "
            "AGU Advances 5, e2023AV001145, https://doi.org/10.1029/2023AV001145."]
    n_win = np.asarray(c["n_soundings"]).sum(axis=(1, 2))
    pre = c.get("n_soundings_preliminary")
    head = ["window_start", "time_year", "time_year_window_mid", "xco2_16day_ppm", "xco2_trend_smoothed_ppm",
            "n_soundings"] + (["n_soundings_preliminary"] if pre is not None else [])
    rows = []
    for k in range(len(time)):
        r = [f"{starts[k]:%Y-%m-%d}", fmt(time[k]), fmt(float(c["time_window_mid_decimal_year"][k])),
             fmt(float(value[k])), fmt(float(trend[k])), str(int(n_win[k]))]
        rows.append(r + ([str(int(pre[k]))] if pre is not None else []))
    stem = out / path.stem
    write_csv(Path(f"{stem}_16day.csv"), note + [
        "time_year = effective time of the window (decimal year); time_year_window_mid = the window's midpoint.",
        "xco2_16day_ppm = area-weighted global mean (50S-50N) of the cell medians, blank = no data;",
        "xco2_trend_smoothed_ppm = deseasonalized, gap-filled, 7-window running mean."], head, rows)
    write_csv(Path(f"{stem}_monthly.csv"), note + [
        "growth_ppm_yr = 5-month running mean of 12 x increment; increment_ppm_month = trend(1st of next month) -",
        "trend(1st of month); time_year = midpoint of the month (decimal year)."],
        ["month", "time_year", "growth_ppm_yr", "increment_ppm_month"],
        [[m, fmt(float(t)), fmt(float(g)), fmt(float(i))] for m, t, g, i in zip(months, mid, monthly, inc)])
    write_csv(Path(f"{stem}_annual.csv"), note + [
        "growth_ppm_yr = trend(1 Jan Y+1) - trend(1 Jan Y), complete calendar years only."],
        ["year", "growth_ppm_yr"], [[str(y), fmt(g)] for y, g in annual.items()])

    print(f"{path.name}: {len(time)} windows ({int(np.isfinite(value).sum())} with data), months {months[0]} to "
          f"{months[-1]}; annual growth (ppm/yr):")
    for y, g in annual.items():
        print(f"  {y}  {g:.2f}")
    print(f"  files: {stem.name}_16day.csv, {stem.name}_monthly.csv, {stem.name}_annual.csv in {out}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("cubes", nargs="+", type=Path, help="GRESO cube file(s), e.g. greso_cube_oco2_v2026.11.nc")
    ap.add_argument("--out", type=Path, default=Path("."), help="folder for the CSV files (default: current folder)")
    ap.add_argument("--first-year", type=int, default=None,
                    help="first year of the monthly and annual series (default: the cube's first full calendar year)")
    args = ap.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    for cube in args.cubes:
        process(cube, args.out, args.first_year)


if __name__ == "__main__":
    sys.exit(main())
