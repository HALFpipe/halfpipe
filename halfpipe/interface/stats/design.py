# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from nipype.interfaces.base import traits, TraitedSpec, SimpleInterface, File

from ...stats.design import group_design, intercept_only_design


class GroupDesignInputSpec(TraitedSpec):
    spreadsheet = File(exist=True, mandatory=True)
    contrastdicts = traits.List(
        traits.Dict(traits.Str, traits.Any),
        mandatory=True,
    )
    variabledicts = traits.List(
        traits.Dict(traits.Str, traits.Any),
        mandatory=True,
    )
    subjects = traits.List(traits.Str, mandatory=True)


class DesignOutputSpec(TraitedSpec):
    regressors = traits.Dict(traits.Str, traits.Any)
    contrasts = traits.List()
    contrast_numbers = traits.List(traits.Str())
    contrast_names = traits.List(traits.Str())


class GroupDesign(SimpleInterface):
    """ interface to construct a group design """

    input_spec = GroupDesignInputSpec
    output_spec = DesignOutputSpec

    def _run_interface(self, runtime):
        regressors, contrasts, numbers, names = group_design(
            spreadsheet=self.inputs.spreadsheet,
            contrastdicts=self.inputs.contrastdicts,
            variabledicts=self.inputs.variabledicts,
            subjects=self.inputs.subjects,
        )
        self._results["regressors"] = regressors
        self._results["contrasts"] = contrasts
        self._results["contrast_numbers"] = numbers
        self._results["contrast_names"] = names

        return runtime


class InterceptOnlyDesignInputSpec(TraitedSpec):
    n_copes = traits.Range(low=1, desc="number of inputs")


class InterceptOnlyDesign(SimpleInterface):
    """ interface to construct a group design """

    input_spec = InterceptOnlyDesignInputSpec
    output_spec = DesignOutputSpec

    def _run_interface(self, runtime):
        regressors, contrasts, numbers, names = intercept_only_design(
            self.inputs.n_copes
        )
        self._results["regressors"] = regressors
        self._results["contrasts"] = contrasts
        self._results["contrast_numbers"] = numbers
        self._results["contrast_names"] = names

        return runtime
