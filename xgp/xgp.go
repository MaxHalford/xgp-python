package main

// #cgo pkg-config: python
// #define Py_LIMITED_API
// #include <Python.h>
import "C"
import (
	"math/rand"
	"time"

	"github.com/MaxHalford/xgp"
	"github.com/MaxHalford/xgp/metrics"
)

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

	funcs string,
	constMin float64,
	constMax float64,
	pConstant float64,
	pFull float64,
	pTerminal float64,
	minHeight int,
	maxHeight int,

	nPopulations int,
	nIndividuals int,
	nGenerations int,
	nPolishGenerations int,
	pHoistMutation float64,
	pSubTreeMutation float64,
	pPointMutation float64,
	pointMutationRate float64,
	pSubTreeCrossover float64,

	parsimonyCoeff float64,

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
	lossMetric, err := metrics.GetMetric(lossMetricName, 1)
	if err != nil {
		panic(err)
	}

	// Determine the evaluation metric
	if evalMetricName == "" {
		evalMetricName = lossMetricName
	}
	evalMetric, err := metrics.GetMetric(evalMetricName, 1)
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
	var config = xgp.Config{
		LossMetric: lossMetric,
		EvalMetric: evalMetric,

		Funcs:     funcs,
		ConstMin:  constMin,
		ConstMax:  constMax,
		PConstant: pConstant,
		PFull:     pFull,
		PTerminal: pTerminal,
		MinHeight: minHeight,
		MaxHeight: maxHeight,

		NPopulations:       nPopulations,
		NIndividuals:       nIndividuals,
		NGenerations:       nGenerations,
		NPolishGenerations: nPolishGenerations,
		PHoistMutation:     pHoistMutation,
		PSubTreeMutation:   pSubTreeMutation,
		PPointMutation:     pPointMutation,
		PointMutationRate:  pointMutationRate,
		PSubTreeCrossover:  pSubTreeCrossover,

		ParsimonyCoeff: parsimonyCoeff,
		RNG:            rng,
	}

	estimator, err := config.NewEstimator()
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
