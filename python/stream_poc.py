# Copyright (c) 2018, Westy Labs LLC (www.westylabs.com). All Rights Reserved.
#
# Redistribution and use in source and binary forms or copying, with or without modification
# is strictly prohibited without prior written permission. Proprietary and confidential.
#
import sys
from collections import deque
from functools import reduce

# Using generators and yield we can make a streaming data pipeline where the total collection of records is never loaded
# into memory. It utilizes a functional paradigm where the outputs of functions are chained to each other. In this way
# we could use python iterators as streams, which we apply functions on.
#
# This class shows a proof of concept for how Operators and Handlers could be rewritten to work with data streams.
# StreamOperator uses a RecordSource which could call an API and stream results as they're read (similar to
# FileReadRecordSource in the example below), without reading the entire payload into memory. The StreamHandlers can
# then be chained, where the final WriteToDiskHandler could also be a SqlInserterHandler that streams records to a file
# for bulk insert or directly to sql.
#
# See this post for a great explanation of how generators and yield work
# https://jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained
#

log_enabled = True
def log(value):
  if log_enabled:
    print("LOG - " + value)

class StreamOperator:

  def __init__(self, input_file, handlers=None, output_file=None):
    self.record_source = FileReadRecordSource(input_file)
    self.handlers = handlers
    self.output_file = output_file

  def execute(self):
    # Approach one - Manually chaining static handler list
    # records = WriteToDiskHandler(self.output_file).handle_records(
    #   PrintStreamHandler().handle_records(
    #     PrependStreamHandler().handle_records(
    #       self.record_source.generator())))

    # Approach two - Recurse over dynamic list of handlers
    # records = self.recursion_pipeline(self.record_generator.generator(), deque(self.handlers))

    # Approach three - chain generators using reduce
    records = self.reduce_pipeline([self.record_source.generator()] + list(map(lambda h: h.handle_records, self.handlers)))

    # converting to a list would cause all records to be loaded into memory, so this would be undesirable
    # list(records)

    # Instead we must iterating over records (i.e., generators) to stream them through in memory
    for record in records:
      log("execute: %s\n" % record)

  def reduce_pipeline(self, funcs):
    return reduce(lambda x, y: y(x), funcs)

  def recursion_pipeline(self, records, handler_queue):
    try:
      h = handler_queue.popleft()
      log("recursion_pipeline invoking %s" % h)
      for record in self.recursion_pipeline(h.handle_records(records), handler_queue):
        yield record
    except IndexError:
      log('recursion_pipeline processing tail')
      for record in records:
        yield record

class FileReadRecordSource:
  def __init__(self, file):
    self.file = file

  def generator(self):
    with open(self.file, 'r') as f:
      for line in f:
        record = line.rstrip()
        log("FileReadGenerator: %s" % record)
        yield record

class PrependStreamHandler:
  def handle_records(self, records):
    for record in records:
      log("PrependStreamHandler: %s" % record)
      yield "=== %s" % record

class PrintStreamHandler:
  def handle_records(self, records):
    for record in records:
      log("PrintStreamHandler: %s" % record)
      print(record)
      yield record

class WriteToDiskHandler:
  def __init__(self, output_file):
    self.output_file = output_file

  def handle_records(self, records):
    with open(self.output_file, 'w') as file:
      for record in records:
        log("WriteToDiskHandler: %s" % record)
        file.write(record + '\n')
        yield record

def main(input_file, output_file=None):
  handlers = [PrependStreamHandler(), PrintStreamHandler()]
  if output_file:
    handlers.append(WriteToDiskHandler(output_file))

  stream_operator = StreamOperator(input_file, handlers=handlers, output_file=output_file)
  stream_operator.execute()


if __name__ == '__main__':
  input_file = sys.argv[1]
  output_file = sys.argv[2] if len(sys.argv) > 2 else None
  main(input_file, output_file)
