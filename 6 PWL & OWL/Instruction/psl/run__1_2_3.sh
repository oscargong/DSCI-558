#!/usr/bin/env bash

readonly PSL_VERSION='2.2.1'
readonly JAR_PATH="./psl-cli-${PSL_VERSION}.jar"
readonly BASE_NAME='model'

readonly ADDITIONAL_PSL_OPTIONS=''
readonly ADDITIONAL_LEARN_OPTIONS='--learn'
readonly ADDITIONAL_EVAL_OPTIONS='--infer --eval org.linqs.psl.evaluation.statistics.DiscreteEvaluator'

echo "Running PSL Weight Learning"
java -jar "${JAR_PATH}" --model "${BASE_NAME}.psl" --data "${BASE_NAME}.data" ${ADDITIONAL_LEARN_OPTIONS} ${ADDITIONAL_PSL_OPTIONS}

echo "Running PSL Inference with new weights"
java -jar "${JAR_PATH}" --model "${BASE_NAME}-learned.psl" --data "${BASE_NAME}.data" --output inferred-predicates ${ADDITIONAL_EVAL_OPTIONS} ${ADDITIONAL_PSL_OPTIONS}