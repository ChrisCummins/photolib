# Copyright 2014-2019 Chris Cummins <chrisc.101@gmail.com>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Useful function decorators."""
import functools

import contextlib
import signal
import typing

from labm8 import app

FLAGS = app.FLAGS

# A type hint that specifies a callable function with any number of arguments
# and any return type.
AnyFunction = typing.Callable[..., typing.Any]


def memoized_property(func: AnyFunction) -> AnyFunction:
  """A property decorator that memoizes the result.

  This is used to memoize the results of class properties, to be used when
  computing the property value is expensive.

  Args:
    func: The function which should be made to a property.

  Returns:
    The decorated property function.
  """
  # Based on Danijar Hafner's implementation of a lazy property, available at:
  # https://danijar.com/structuring-your-tensorflow-models/
  attribute_name = '_memoized_property_' + func.__name__

  @property
  @functools.wraps(func)
  def decorator(self):
    if not hasattr(self, attribute_name):
      setattr(self, attribute_name, func(self))
    return getattr(self, attribute_name)

  return decorator


@contextlib.contextmanager
def timeout(seconds: int):
  """A function decorator that raises TimeoutError after specified time limit.

  Args:
    seconds: The number of seconds before timing out.

  Raises:
    TimeoutError: If the number of seconds have been reached.
  """

  def _RaiseTimoutError(signum, frame):
    raise TimeoutError(f'Function failed to complete within {seconds} seconds')

  # Register a function to raise a TimeoutError on the signal.
  signal.signal(signal.SIGALRM, _RaiseTimoutError)
  signal.alarm(seconds)

  try:
    yield
  except TimeoutError as e:
    raise e
  finally:
    # Unregister the signal so it won't be triggered
    # if the timeout is not reached.
    signal.signal(signal.SIGALRM, signal.SIG_IGN)


@contextlib.contextmanager
def timeout_without_exception(seconds: int):
  """A function decorator that adds a timeout.

  Args:
    seconds: The number of seconds before timing out.
  """

  def _RaiseTimoutError(signum, frame):
    raise TimeoutError

  # Register a function to raise a TimeoutError on the signal.
  signal.signal(signal.SIGALRM, _RaiseTimoutError)
  signal.alarm(seconds)

  try:
    yield
  except TimeoutError:
    pass
  finally:
    # Unregister the signal so it won't be triggered
    # if the timeout is not reached.
    signal.signal(signal.SIGALRM, signal.SIG_IGN)


def run_once(f):
  """Runs a function (successfully) only once.

  The running can be reset by setting the `has_run` attribute to False

  Author: Jason Grout.
  From: https://gist.github.com/jasongrout/3804691
  """

  @functools.wraps(f)
  def wrapper(*args, **kwargs):
    if not wrapper.has_run:
      wrapper.result = f(*args, **kwargs)
      wrapper.has_run = True
    return wrapper.result

  wrapper.has_run = False
  return wrapper
