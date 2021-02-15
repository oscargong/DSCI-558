#!/usr/bin/env bash

readonly PSL_VERSION='2.2.1'
readonly JAR_PATH="./psl-cli-${PSL_VERSION}.jar"
readonly BASE_NAME='model'

readonly ADDITIONAL_PSL_OPTIONS=''
readonly ADDITIONAL_EVAL_OPTIONS='--infer --eval org.linqs.psl.evaluation.statistics.DiscreteEvaluator'

echo "Running PSL Inference with original weights"
java -jar "${JAR_PATH}" --model "${BASE_NAME}.psl" --data "${BASE_NAME}.data" --output inferred-predicates ${ADDITIONAL_EVAL_OPTIONS} ${ADDITIONAL_PSL_OPTIONS}