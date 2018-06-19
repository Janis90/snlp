#!/bin/sh
../../CRF++-0.58/crf_learn -c 10.0 template data-eng/eng.train model
../../CRF++-0.58/crf_test  -m model data-eng/eng.dev

#../../CRF++-0.58/crf_learn -a MIRA template data-eng/eng.train model
#../../CRF++-0.58/crf_test  -m model data-eng/eng.dev
