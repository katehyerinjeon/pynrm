# pynrm
`pynrm` is a lightweight and extensible animal breeding simulation library for Python.

[![Build Status](https://github.com/katehyerinjeon/pynrm/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/katehyerinjeon/pynrm/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/katehyerinjeon/pynrm/branch/main/graph/badge.svg)](https://codecov.io/gh/katehyerinjeon/pynrm)
![GitHub](https://img.shields.io/github/license/katehyerinjeon/pynrm)
![GitHub issues](https://img.shields.io/github/issues/katehyerinjeon/pynrm)

## Overview
The numerator relationship matrix describes additive genetic relationships within a population.
Numerous evaluation-selection systems have been devised to produce populations with favorable genetic responses while maintaining moderate to low rates of inbreeding.
`pynrm` provides a simple yet powerful simulation tool to forecast the stochastic impacts of these systems.
One major bottleneck to running these simulations is that as the number of animals bred increases, the size of the matrix grows exponentially.
`pynrm` efficiently solves for the numerator relationship matrix values by tracing up the pedigree for only the relevant ancestors, thereby minimizing computational overhead.
