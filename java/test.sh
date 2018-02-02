#!/bin/bash
#
# Simple script to compile and test. This would typically be a real build system
#
JARS="lib/test/junit-4.11.jar:lib/test/mockito-all-1.10.19.jar:lib/test/hamcrest-core-1.3.jar"
TEST_CP="out/.:$JARS"
DEBUG_OPTS=""
#DEBUG_OPTS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005"

rm -rf out && mkdir -p out

javac -classpath "$JARS" -Xlint:unchecked -d out/ {src,test}/billg/*.java && \
java -classpath "$TEST_CP" $DEBUG_OPTS org.junit.runner.JUnitCore billg.MainTest
