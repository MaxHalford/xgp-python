package main

import "C"
import (
	"math/rand"
	"time"

	"github.com/MaxHalford/xgp"
	"github.com/MaxHalford/xgp/metrics"
)

// Fit an Estimator and return the best Program.
//export Fit
func Fit(
	XTrain [][]float64,
	YTrain []float64,
	WTrain []float64,
	XVal [][]float64,
	YVal []float64,
	WVal []float64,

	lossMetricName string,
	evalMetricName string,
	parsimonyCoeff float64,
	polishBest bool,

	funcs string,
	constMin float64,
	constMax float64,
	pConst float64,
	pFull float64,
	pLeaf float64,
	minHeight uint,
	maxHeight uint,

	nPopulations uint,
	nIndividuals uint,
	nGenerations uint,
	pHoistMutation float64,
	pSubtreeMutation float64,
	pPointMutation float64,
	pointMutationRate float64,
	pSubtreeCrossover float64,

	seed int64,
	verbose bool,
) *C.char {
	if len(WTrain) == 0 {
		WTrain = nil
	}
	if len(XVal) == 0 {
		XVal = nil
	}
	if len(YVal) == 0 {
		YVal = nil
	}
	if len(WVal) == 0 {
		WVal = nil
	}

	// Determine the loss metric
	lossMetric, err := metrics.ParseMetric(lossMetricName, 1)
	if err != nil {
		panic(err)
	}

	// Determine the evaluation metric
	if evalMetricName == "" {
		evalMetricName = lossMetricName
	}
	evalMetric, err := metrics.ParseMetric(evalMetricName, 1)
	if err != nil {
		panic(err)
	}

	// Determine the random seed
	var rng *rand.Rand
	if seed == 0 {
		rng = rand.New(rand.NewSource(time.Now().UnixNano()))
	} else {
		rng = rand.New(rand.NewSource(seed))
	}

	// Instantiate an Estimator
	var config = xgp.GPConfig{
		LossMetric:     lossMetric,
		EvalMetric:     evalMetric,
		ParsimonyCoeff: parsimonyCoeff,
		PolishBest:     polishBest,

		Funcs:     funcs,
		ConstMin:  constMin,
		ConstMax:  constMax,
		PConst:    pConst,
		PFull:     pFull,
		PLeaf:     pLeaf,
		MinHeight: minHeight,
		MaxHeight: maxHeight,

		NPopulations:      nPopulations,
		NIndividuals:      nIndividuals,
		NGenerations:      nGenerations,
		PHoistMutation:    pHoistMutation,
		PSubtreeMutation:  pSubtreeMutation,
		PPointMutation:    pPointMutation,
		PointMutationRate: pointMutationRate,
		PSubtreeCrossover: pSubtreeCrossover,

		RNG: rng,
	}

	estimator, err := config.NewGP()
	if err != nil {
		panic(err)
	}

	// Fit the Estimator
	_, err = estimator.Fit(XTrain, YTrain, WTrain, XVal, YVal, WVal, verbose)
	if err != nil {
		panic(err)
	}

	// Return the string representation of the best Program
	return C.CString(estimator.BestProgram().String())
}

func main() {}
