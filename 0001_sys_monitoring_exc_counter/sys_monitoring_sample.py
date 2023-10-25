import sys
from collections import Counter

TEST_TOOL_ID = 4

event_counter = Counter()  


def exception_counter(code, offset, exception):
    print(f'DEBUG: code is {code}, offset is {offset}, exception is {exception}')
    event_counter['exception'] += 1

def exception_reraise_counter(code, offset, exception):
    print(f'DEBUG: reraise: code is {code}, offset is {offset}, exception is {exception}')
    event_counter['exception_reraise'] += 1


def maybe_raise(i):
    try:
        if i % 2 == 0:
            raise ValueError('Simulate ValueError')
    except Exception as e:
        raise


def main():
    for i in range(1):
        try:
            print(f'iteration #{i}')
            maybe_raise(i)
        except Exception as e:
            print(f'DEBUG: exception #{e}')
            pass

if __name__ == '__main__':
    sys.monitoring.use_tool_id(TEST_TOOL_ID, 'test_monitoring')
    sys.monitoring.set_events(TEST_TOOL_ID, sys.monitoring.events.RAISE|sys.monitoring.events.RERAISE)
    sys.monitoring.register_callback(TEST_TOOL_ID, sys.monitoring.events.RAISE, exception_counter) 
    sys.monitoring.register_callback(TEST_TOOL_ID, sys.monitoring.events.RERAISE, exception_reraise_counter) 
    main()
    print(
        f'Profiling results:',
        f'exc_count: {event_counter["exception"]}',
        f'reraise_count: {event_counter["exception_reraise"]}'
    )
