# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Nipype interfaces to calculate connectivity measures using nilearn.
Adapted from https://github.com/Neurita/pypes
"""
from os import path as op

import numpy as np
import pandas as pd

from nipype.interfaces.base import (
    BaseInterface,
    TraitedSpec,
    BaseInterfaceInputSpec,
    traits,
    File
)

from ..io import meansignals


class ConnectivityMeasureInputSpec(BaseInterfaceInputSpec):
    in_file = File(
        desc="Image file(s) from where to extract the data", exists=True, mandatory=True
    )
    mask_file = File(desc="Mask file", exists=True, mandatory=True)
    atlas_file = File(
        desc="Atlas image file defining the connectivity ROIs", exists=True, mandatory=True,
    )

    background_label = traits.Int(desc="", default=0, usedefault=True)
    min_region_coverage = traits.Float(desc="", default=0.8, usedefault=True)


class ConnectivityMeasureOutputSpec(TraitedSpec):
    time_series = File(desc="Numpy text file with the timeseries matrix")
    covariance = File(desc="Numpy text file with the connectivity matrix")
    correlation = File(desc="Numpy text file with the connectivity matrix")
    region_coverage = traits.List(traits.Float)


class ConnectivityMeasure(BaseInterface):
    input_spec = ConnectivityMeasureInputSpec
    output_spec = ConnectivityMeasureOutputSpec

    def _run_interface(self, runtime):
        self._time_series, self._region_coverage = meansignals(
            self.inputs.in_file,
            self.inputs.atlas_file,
            mask_file=self.inputs.mask_file,
            background_label=self.inputs.background_label,
            min_region_coverage=self.inputs.min_region_coverage,
            output_coverage=True
        )

        df = pd.DataFrame(self._time_series)

        self._cov_mat = np.asarray(df.cov())
        self._corr_mat = np.asarray(df.corr())

        return runtime

    def _list_outputs(self):
        outputs = self.output_spec().get()

        argdict = dict(fmt="%.10f", delimiter="\t")

        time_series_file = op.abspath("timeseries.tsv")
        np.savetxt(time_series_file, self._time_series, **argdict)

        covariance_file = op.abspath("covariance.tsv")
        np.savetxt(covariance_file, self._cov_mat, **argdict)

        correlation_file = op.abspath("correlation.tsv")
        np.savetxt(correlation_file, self._corr_mat, **argdict)

        outputs["time_series"] = time_series_file
        outputs["covariance"] = covariance_file
        outputs["correlation"] = correlation_file

        outputs["region_coverage"] = self._region_coverage

        return outputs
