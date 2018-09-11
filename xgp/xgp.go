package main

import "C"
import (
	"fmt"
	"math/rand"
	"time"

	"github.com/MaxHalford/xgp"
	"github.com/MaxHalford/xgp/meta"
	"github.com/MaxHalford/xgp/metrics"
)

type errUnknownFlavor struct {
	flavor string
}

func (e errUnknownFlavor) Error() string {
	return fmt.Sprintf("'%s' is not a recognized flavor, has to be one of ('vanilla', 'boosting')", e.flavor)
}

// Fit an Estimator and return the best Program.
//export Fit
func Fit(
	XTrain [][]float64,
	YTrain []float64,
	WTrain []float64,
	XVal [][]float64,
	YVal []float64,
	WVal []float64,

	flavor string,

	// GP learning parameters
	lossName string,
	evalName string,
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

	// GA parameters
	nPops uint,
	popSize uint,
	nGenerations uint,
	pHoistMut float64,
	pSubtreeMut float64,
	pPointMut float64,
	pointMutRate float64,
	pSubtreeCross float64,

	// Ensemble learning parameters
	nRounds uint,
	nEarlyStoppingRounds uint,
	learningRate float64,
	lineSearch bool,
	rowSampling float64,
	colSampling float64,
	useBestRounds bool,
	monitorEvery uint,

	// Other
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
	lossMetric, err := metrics.ParseMetric(lossName, 1)
	if err != nil {
		panic(err)
	}

	// Determine the evaluation metric
	if evalName == "" {
		evalName = lossName
	}
	evalMetric, err := metrics.ParseMetric(evalName, 1)
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

		NPopulations:      nPops,
		NIndividuals:      popSize,
		NGenerations:      nGenerations,
		PHoistMutation:    pHoistMut,
		PSubtreeMutation:  pSubtreeMut,
		PPointMutation:    pPointMut,
		PointMutationRate: pointMutRate,
		PSubtreeCrossover: pSubtreeCross,

		RNG: rng,
	}

	switch flavor {

	case "vanilla":
		gp, err := config.NewGP()
		if err != nil {
			panic(err)
		}
		err = gp.Fit(XTrain, YTrain, WTrain, XVal, YVal, WVal, verbose)
		if err != nil {
			panic(err)
		}
		best, err := gp.BestProgram()
		if err != nil {
			panic(err)
		}
		bytes, err := best.MarshalJSON()
		if err != nil {
			panic(err)
		}
		return C.CString(string(bytes))

	case "boosting":
		loss, ok := lossMetric.(metrics.DiffMetric)
		if !ok {
			panic(fmt.Errorf("The '%s' metric can't be used for gradient boosting because it is"+
				" not differentiable", lossMetric.String()))
		}
		var ls meta.LineSearcher
		if lineSearch {
			ls = meta.GoldenLineSearch{
				Min: 0,
				Max: 10,
				Tol: 1e-10,
			}
		}
		gb, err := meta.NewGradientBoosting(
			config,
			nRounds,
			nEarlyStoppingRounds,
			learningRate,
			ls,
			loss,
			rowSampling,
			colSampling,
			useBestRounds,
			monitorEvery,
			rng,
		)
		if err != nil {
			panic(err)
		}
		err = gb.Fit(XTrain, YTrain, nil, XVal, YVal, nil, verbose)
		if err != nil {
			panic(err)
		}
		bytes, err := gb.MarshalJSON()
		if err != nil {
			panic(err)
		}
		return C.CString(string(bytes))

	}

	panic(errUnknownFlavor{flavor})

	return C.CString("")
}

func main() {}
